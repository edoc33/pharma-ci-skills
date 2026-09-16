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
      --title "Competitor trial record" --rule "Alert me when the overall status ... changes." --confirm
  python3 vp_client.py bulk --workspace 12345 --csv watchlist.csv --confirm

The bulk CSV needs the columns url,title,rule and may include interval (minutes as text, default
1440 = daily). Standard library only.
"""
import argparse, csv, json, os, sys, time, urllib.request, urllib.error

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
        if lvl not in ("important", "regular"):
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


def job_body(workspace, url, title, rule, interval="1440", email=True, webhook=None, important_only=True):
    body = {
        "workspaceId": int(workspace), "url": url, "description": title, "interval": str(interval),
        "summalyzer": {"importantDefinitionType": "custom", "importantDefinition": rule},
        "notification": {"enableEmailAlert": bool(email), "enableSmsAlert": False,
                          "onlyImportantAlerts": bool(important_only)},
    }
    if webhook:
        body["notification"]["config"] = {"webhook": {"url": webhook, "active": True, "notificationType": "webhook"}}
    return body


def create(workspace, url, title, rule, interval="1440", confirm=False, webhook=None):
    body = job_body(workspace, url, title, rule, interval, webhook=webhook)
    if not confirm:
        print(json.dumps(body, indent=2)); print("\nDry run. Re-run with --confirm to create this monitor.")
        return None
    return request("POST", f"{JOBS}/v2/jobs", body)


def bulk(workspace, csv_path, confirm=False, webhook=None):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    need = {"url", "title", "rule"} - set(rows[0].keys() if rows else [])
    if need:
        sys.exit(f"CSV is missing columns: {sorted(need)}")
    existing = {j.get("url") for j in list_jobs(workspace)} if confirm else set()
    plan = []
    for r in rows:
        action = "SKIP (already monitored)" if r["url"] in existing else "CREATE"
        plan.append((action, r["url"], r["title"]))
    for a, u, t in plan:
        print(f"{a:26} {u}  |  {t}")
    monthly = sum(1440 / int(r.get("interval") or 1440) * 30 for r in rows)
    print(f"\n{len(rows)} rows; roughly {int(monthly)} checks per month at the listed intervals.")
    if not confirm:
        print("Dry run. Re-run with --confirm to create the CREATE rows."); return
    for r in rows:
        if r["url"] in existing:
            continue
        request("POST", f"{JOBS}/v2/jobs", job_body(workspace, r["url"], r["title"], r["rule"], r.get("interval") or "1440", webhook=webhook))
        print("created", r["url"]); time.sleep(0.4)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    a = sub.add_parser("jobs"); a.add_argument("--workspace", required=True)
    a = sub.add_parser("changes"); a.add_argument("--job", required=True); a.add_argument("--workspace"); a.add_argument("--since")
    a = sub.add_parser("feed"); a.add_argument("--workspace", required=True); a.add_argument("--important-only", action="store_true")
    a = sub.add_parser("create"); a.add_argument("--workspace", required=True); a.add_argument("--url", required=True)
    a.add_argument("--title", required=True); a.add_argument("--rule", required=True); a.add_argument("--interval", default="1440")
    a.add_argument("--webhook"); a.add_argument("--confirm", action="store_true")
    a = sub.add_parser("bulk"); a.add_argument("--workspace", required=True); a.add_argument("--csv", required=True)
    a.add_argument("--webhook"); a.add_argument("--confirm", action="store_true")
    args = p.parse_args()
    if args.cmd == "whoami":
        u = whoami()
        who = u.get("email") or u.get("userEmail") or (u.get("user") or {}).get("email") or u.get("username")
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
        r = create(args.workspace, args.url, args.title, args.rule, args.interval, args.confirm, args.webhook)
        if r is not None: print(json.dumps(r, indent=2)[:600])
    elif args.cmd == "bulk":
        bulk(args.workspace, args.csv, args.confirm, args.webhook)


if __name__ == "__main__":
    main()
