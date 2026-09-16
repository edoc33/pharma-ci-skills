# Visualping API: the subset these skills use

Verified September 16, 2026 against the [official API documentation](https://api.visualping.io/doc.html),
its [OpenAPI specification](https://api.visualping.io/data/openapi-definition.yaml), and the
[public API skill reference](https://github.com/webmonitoring/visualping-api-skill/blob/develop/reference/api-reference.md).
The official specification covers core account and monitor operations. The public skill also
documents the activity-feed endpoint, with less strict compatibility guarantees.

Keys are created at https://visualping.io/account/developer and are available on every plan,
including Free. Business workspace Admins manage keys; the key's scope and access level must
permit the selected operation. Keep the
key in the `VISUALPING_API_KEY` environment variable; never paste it into a chat or a file you
commit. The helper `scripts/vp_client.py` at the repository root wraps every call below and refuses
to create monitors without `--confirm`.

## Base URLs and auth

| Purpose | Base URL |
|---|---|
| Jobs (monitors) | `https://job.api.visualping.io` |
| Account | `https://account.api.visualping.io` |

Header on every request: `Authorization: Bearer <api key>` and `Content-Type: application/json`.

## Who am I, and which workspace

`GET https://account.api.visualping.io/describe-user` returns `emailAddress`, `userId` and a `workspaces` list
(`id`, `name`). Business accounts must pass `workspaceId` on job calls; if the user has one
workspace, use it without asking.

## List monitors

`GET https://job.api.visualping.io/v2/jobs?workspaceId=<id>&pageSize=100&pageIndex=0` returns
`jobs` and `totalPages`. Each job carries `id`, `url`, `description`, `interval`, `isActive`,
`last_run`. Check the list before creating anything so you never duplicate a URL.

## Create a monitor

`POST https://job.api.visualping.io/v2/jobs`

| Field | Type | Notes |
|---|---|---|
| `workspaceId` | integer | Required on business accounts |
| `url` | string | Required. The exact page, not the site |
| `description` | string | The monitor's title. Put the source and the decision it serves here |
| `interval` | string | Minutes as a string. `"1440"` daily (default), `"10080"` weekly, `"60"` hourly, `"360"` every six hours |
| `mode` | string | The helper explicitly sets `ALL` |
| `active` | boolean | Required by the published create schema; the helper sets `true` |
| `target_device` | string | Required by the published create schema; `"4"` means full-page desktop |
| `trigger` | string | Required by the published create schema; the helper sets `"1"` |
| `wait_time` | integer | Required by the published create schema; the helper sets `0` |
| `summalyzer` | object | `{"importantDefinitionType": "custom", "importantDefinition": "<your rule>"}` |
| `notification` | object | Enables email and supplies `config`; `onlyImportantAlerts` follows the explicitly chosen delivery policy |
| `xpath` | string | Optional CSS or XPath selector to watch one region of the page |
| `preactions` | object | Optional click and type steps run before each check (login walls, cookie banners, search boxes) |
| `retention_policy` | string | `"3"` or `"12"` months of history |

`notification.config` holds the routes; use `{}` when there are no advanced routes. The helper
explicitly enables email. A webhook route is
`{"webhook": {"url": "https://...", "active": true, "notificationType": "webhook"}}`; Slack and
Teams routes take the same shape with their own webhook URL. Capture one real payload before you
map fields in a downstream flow; do not assume the shape.

A successful create returns `jobid`, the new monitor identifier, and an internal `id` according to
the [create response schema](https://api.visualping.io/data/JobCreateResponseJsonSchema.json).
Use `jobid` for subsequent job calls. The helper checks existing exact URLs before a confirmed
create; bulk creation also skips repeated URLs within the CSV. This check is not an atomic lock
against another process creating the same URL concurrently.

The importance rule is the part that matters. `importantDefinitionType: "custom"` tells the AI to
judge every change against your `importantDefinition`; `"default"` uses a generic judgment. See
`rule-grammar.md` for how to write one.

### Choose delivery independently from the rule

`create` requires `--delivery all` or `--delivery important`. The first sets
`notification.onlyImportantAlerts=false`; the second sets it to `true`. Both retain the custom
importance rule. `all` delivers change alerts subject to the monitor's ordinary detection settings;
it does not mean every check generates an alert. Changing delivery does not reduce check consumption.

For `bulk`, supply the same `--delivery` option as a common policy, or set `delivery_policy` to `all`
or `important` in each CSV row. A non-empty row policy overrides the common policy. Missing or
invalid policy stops a confirmed batch before API access. A bulk dry run may display missing policy
as `UNCONFIRMED (preview: all)`; it remains unapproved for creation until an explicit policy is supplied.

Use `all` when the analyst needs to review each change alert, and `important` when the importance
rule has been evaluated and the user chooses filtered delivery. Record which policy was chosen in
the watchlist. A proposed rule or delivery choice is separate from the monitor's saved settings.

## Read what changed

`GET https://job.api.visualping.io/v2/jobs/<jobId>?workspaceId=<id>` returns the job with a
`changes` array. Each change has `created`, `englishSummary` (the AI summary of what changed),
`analyzerAlertTriggered` (the IMPORTANT flag), `PercentDifference`, `process_id` and screenshot
links. The array is capped at recent changes, so pull it on a schedule and keep your own record.

`POST https://job.api.visualping.io/v2/jobs/report-page` with
`{"workspaceId": <id>, "scope": {"comboId": -<id>}, "includeErrors": false, "level": "allChecks"}`
returns a workspace-wide activity feed, newest first. Each item has `jobId`, `description`, `url`,
`screenshotLogCreated`, `changeDetectionLevel` (`important`, `regular`, `minor-threshold`,
`minor-importance`, `none`, or absent on the first check), `aiOutput.changeSummary`,
`aiOutput.changeIsImportant` and `aiOutput.changeIsImportantReason`. The feed is capped at recent
checks. Per-job `changes` is also capped: neither response proves complete weekly coverage.
Collect and deduplicate events into your approved store on a suitable schedule, retain their
timestamps and identifiers, and state the captured window when generating a digest. The helper's
`--since` option filters only the returned recent changes; it does not fetch older history.
The helper's `feed` includes important, regular and minor changes; `--important-only` explicitly
filters that output. Unchanged checks and initial baselines are omitted from this changes view.

## Pause, resume, update, delete

`PUT https://job.api.visualping.io/v2/jobs/<jobId>` with the fields to change (`{"active": false}`
pauses; a new `summalyzer` object rewrites the rule). `DELETE` removes the monitor and its history.
Both are mutations: present the affected monitors and proposed change, obtain authorization for
that action, then call. Existing explicit authorization remains valid. The helper currently exposes
creation only; its `--confirm` flag is required for writes.

## Bulk import in the web app

Business plans have Bulk Import in the dashboard. It takes a CSV with exactly two columns, `URL`
and `Title`. Rules, intervals and routes are applied per monitor after the import, so keep the
prompt guide beside the import file. On other plans add monitors individually or with
`scripts/vp_client.py bulk`, which creates them one by one from a CSV with `url,title,rule` and an
optional `interval` and `delivery_policy` columns. A live bulk write requires a row policy or
the common `--delivery` option.

The helper validates every CSV row before creating anything and accepts UTF-8 files with or
without a byte-order mark. Blank titles or rules, invalid URLs and non-positive intervals stop the
batch. A dry run makes no API calls, so its plan cannot account for existing workspace URLs until
`--confirm` rechecks them. The estimated check count covers only planned CREATE rows.

## Plan limits

Monthly checks are roughly `(1440 / interval minutes) x monitors x 30`. Twenty daily monitors are
600 checks a month; one hourly monitor alone is 720. Warn before a plan creates a large share of the
account's monthly budget. Choose the cadence from the team's decision deadline, source behavior
and available plan. Verify any applicable deadline before using it to set the schedule.

## MCP alternative

Visualping also exposes an MCP server at `https://visualping.io/mcp/sse` for Claude, ChatGPT and
other agents, with tools such as `create_monitor`, `get_monitors`, `get_timeline` and
`describe_user`. These skills use the REST API so they run anywhere Python does.
