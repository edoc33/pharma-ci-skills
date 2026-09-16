#!/usr/bin/env python3
"""Thin client for the public Visualping API, used by the pharma-ci skills.

Auth: set VISUALPING_API_KEY (create a key at https://visualping.io/account/developer; keys are
available on every plan, including Free). Nothing here writes unless you call `create` or `bulk`,
and both refuse to run without --confirm.

Examples
  python3 vp_client.py whoami
  python3 vp_client.py jobs --workspace 12345
  python3 vp_client.py changes --job 987654 --workspace 12345 --since 2026-09-01
  python3 vp_client.py feed --workspace 12345 --important-only
  python3 vp_client.py create --workspace 12345 --url https://clinicaltrials.gov/study/NCT00000000 \
      --title "Competitor trial record" --rule "Alert me when the overall status ... changes." --delivery all --confirm
  python3 vp_client.py bulk --workspace 12345 --csv watchlist.csv --delivery important --confirm

The bulk CSV needs url,title,rule and may include interval (minutes as text, default 1440 = daily)
and delivery_policy (all or important). A live write requires a per-row policy or --delivery.
Standard library only.
"""
import argparse, csv, json, os, sys, time, urllib.request, urllib.error
from urllib.parse import urlsplit

JOBS = "https://job.api.visualping.io"
ACCOUNT = "https://account.api.visualping.io"


def _key():
    k = os.environ.get("VISUALPING_API_KEY")
    if not k:
        sys.exit("Set VISUALPING_API_KEY first (https://visualping.io/account/developer).")
    return k


def request(method, url, body=None, retries=3, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {_key()}")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(int(e.headers.get("Retry-After", "10")))
                continue
            sys.exit(f"HTTP {e.code} for {method} {url}: {e.read().decode()[:400]}")
    return {}


def whoami():
    return request("GET", f"{ACCOUNT}/describe-user")


def list_jobs(workspace, page_size=100):
    out, page = [], 0
    while True:
        r = request("GET", f"{JOBS}/v2/jobs?workspaceId={workspace}&pageSize={page_size}&pageIndex={page}")
        out.extend(r.get("jobs", []))
        if page + 1 >= r.get("totalPages", 1):
            return out
        page += 1


def get_job(job_id, workspace=None):
    q = f"?workspaceId={workspace}" if workspace else ""
    return request("GET", f"{JOBS}/v2/jobs/{job_id}{q}")


def changes(job_id, workspace=None, since=None):
    rows = []
    for c in get_job(job_id, workspace).get("changes", []) or []:
        created = str(c.get("created", ""))
        if since and created < since:
            continue
        rows.append({
            "created": created[:16],
            "important": c.get("analyzerAlertTriggered"),
            "summary": (c.get("englishSummary") or "").strip(),
            "process_id": c.get("process_id"),
        })
    return rows


def feed(workspace, important_only=False):
    r = request("POST", f"{JOBS}/v2/jobs/report-page", {
        "workspaceId": int(workspace), "scope": {"comboId": -int(workspace)},
        "includeErrors": False, "level": "allChecks"})
    items = []
    for it in r.get("items", []):
        lvl = it.get("changeDetectionLevel")
        if lvl not in ("important", "regular", "minor-threshold", "minor-importance"):
            continue
        if important_only and lvl != "important":
            continue
        ai = it.get("aiOutput") or {}
        items.append({
            "when": str(it.get("screenshotLogCreated", ""))[:16], "job": it.get("jobId"),
            "title": it.get("description"), "url": it.get("url"), "level": lvl,
            "important": ai.get("changeIsImportant"), "summary": (ai.get("changeSummary") or "").strip(),
        })
    return items


def job_body(workspace, url, title, rule, interval="1440", email=True, webhook=None, important_only=False):
    try:
        workspace, interval = int(workspace), int(interval)
        if workspace <= 0 or interval <= 0:
            raise ValueError
    except (TypeError, ValueError):
        sys.exit("Workspace and interval must be positive integers.")
    url, title, rule = (value.strip() if isinstance(value, str) else "" for value in (url, title, rule))
    if urlsplit(url).scheme not in ("http", "https") or not urlsplit(url).hostname:
        sys.exit("Each monitor needs a valid HTTP or HTTPS URL.")
    if not title or not rule:
        sys.exit("Each monitor needs a non-empty title and importance rule.")
    if webhook and (urlsplit(webhook).scheme not in ("http", "https") or not urlsplit(webhook).hostname):
        sys.exit("Webhook must be an HTTP or HTTPS URL.")
    body = {
        "workspaceId": workspace, "url": url, "description": title, "interval": str(interval),
        "active": True, "mode": "ALL", "target_device": "4", "trigger": "1", "wait_time": 0,
        "summalyzer": {"importantDefinitionType": "custom", "importantDefinition": rule},
        "notification": {"enableEmailAlert": bool(email), "enableSmsAlert": False,
                          "onlyImportantAlerts": bool(important_only), "config": {}},
    }
    if webhook:
        body["notification"]["config"] = {"webhook": {"url": webhook, "active": True, "notificationType": "webhook"}}
    return body


def delivery_policy(value, confirm=False):
    value = value.strip() if isinstance(value, str) else value
    if value not in (None, "", "all", "important"):
        sys.exit("Delivery policy must be all or important.")
    if not value and confirm:
        sys.exit("Choose --delivery all|important or set every CSV row's delivery_policy before using --confirm.")
    return value or "all"


def create(workspace, url, title, rule, interval="1440", confirm=False, webhook=None, delivery=None):
    policy = delivery_policy(delivery, confirm)
    body = job_body(workspace, url, title, rule, interval, webhook=webhook, important_only=policy == "important")
    if not confirm:
        if not delivery:
            print("UNCONFIRMED delivery policy: all changes shown for preview only. Choose a policy before --confirm.")
        print(json.dumps(body, indent=2)); print("\nDry run. Re-run with --confirm to create this monitor.")
        return None
    if any(j.get("url") == body["url"] for j in list_jobs(workspace)):
        print("SKIP (already monitored)", body["url"])
        return None
    return request("POST", f"{JOBS}/v2/jobs", body)


def bulk(workspace, csv_path, confirm=False, webhook=None, delivery=None):
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        need = {"url", "title", "rule"} - set(reader.fieldnames or [])
    if need:
        sys.exit(f"CSV is missing columns: {sorted(need)}")
    if not rows:
        sys.exit("CSV has no monitor rows.")
    # Validate the entire batch before any remote request or partial creation.
    delivery_policy(delivery)  # Validate a common policy even when every row overrides it.
    chosen = [(r.get("delivery_policy") or "").strip() or delivery for r in rows]
    policies = [delivery_policy(policy, confirm) for policy in chosen]
    bodies = [job_body(workspace, r.get("url"), r.get("title"), r.get("rule"),
                       r.get("interval") or "1440", webhook=webhook, important_only=policy == "important")
              for r, policy in zip(rows, policies)]
    existing = {j.get("url") for j in list_jobs(workspace)} if confirm else set()
    plan, creates, seen = [], [], set(existing)
    for body, policy, explicit in zip(bodies, policies, chosen):
        url = body["url"]
        action = "SKIP (already monitored)" if url in existing else "SKIP (duplicate CSV URL)" if url in seen else "CREATE"
        plan.append((action, url, body["description"], policy if explicit else "UNCONFIRMED (preview: all)"))
        if action == "CREATE":
            creates.append(body)
        seen.add(url)
    for a, u, t, policy in plan:
        print(f"{a:26} {u}  |  {t}  |  delivery={policy}")
    monthly = sum(1440 / int(body["interval"]) * 30 for body in creates)
    print(f"\n{len(rows)} rows; {len(creates)} CREATE rows; roughly {int(monthly)} checks per month for those rows.")
    if not confirm:
        print("Dry run. Existing workspace URLs will also be checked when run with --confirm."); return
    for body in creates:
        result = request("POST", f"{JOBS}/v2/jobs", body)
        print("created", body["url"], "jobid=" + str(result.get("jobid", "unavailable"))); time.sleep(0.4)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    a = sub.add_parser("jobs"); a.add_argument("--workspace", required=True)
    a = sub.add_parser("changes"); a.add_argument("--job", required=True); a.add_argument("--workspace"); a.add_argument("--since")
    a = sub.add_parser("feed"); a.add_argument("--workspace", required=True); a.add_argument("--important-only", action="store_true")
    a = sub.add_parser("create"); a.add_argument("--workspace", required=True); a.add_argument("--url", required=True)
    a.add_argument("--title", required=True); a.add_argument("--rule", required=True); a.add_argument("--interval", default="1440")
    a.add_argument("--delivery", required=True, choices=("all", "important"), help="Send every change or only AI-important changes")
    a.add_argument("--webhook"); a.add_argument("--confirm", action="store_true")
    a = sub.add_parser("bulk"); a.add_argument("--workspace", required=True); a.add_argument("--csv", required=True)
    a.add_argument("--delivery", choices=("all", "important"), help="Default delivery policy; a CSV row's delivery_policy overrides it")
    a.add_argument("--webhook"); a.add_argument("--confirm", action="store_true")
    args = p.parse_args()
    if args.cmd == "whoami":
        u = whoami()
        who = u.get("emailAddress") or u.get("email") or u.get("userEmail") or (u.get("user") or {}).get("email") or u.get("username")
        print(json.dumps({"user": who, "workspaces": [{"id": w.get("id"), "name": w.get("name")} for w in u.get("workspaces", [])]}, indent=2))
    elif args.cmd == "jobs":
        for j in list_jobs(args.workspace):
            print(f"{j.get('id')}\t{'active' if j.get('isActive', j.get('active')) else 'paused'}\t{j.get('interval')}\t{(j.get('description') or '')[:40]}\t{j.get('url')}")
    elif args.cmd == "changes":
        for c in changes(args.job, args.workspace, args.since):
            print(f"{c['created']}  important={c['important']}  {c['summary'][:200]}")
    elif args.cmd == "feed":
        for it in feed(args.workspace, args.important_only):
            print(f"{it['when']}  {it['level']:9} job {it['job']}  {(it['title'] or '')[:36]}\n    {it['summary'][:220]}")
    elif args.cmd == "create":
        r = create(args.workspace, args.url, args.title, args.rule, args.interval, args.confirm, args.webhook, args.delivery)
        if r is not None: print(json.dumps(r, indent=2)[:600])
    elif args.cmd == "bulk":
        bulk(args.workspace, args.csv, args.confirm, args.webhook, args.delivery)


if __name__ == "__main__":
    main()
