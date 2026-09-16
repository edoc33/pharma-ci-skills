# First run: a fictional regulatory watchlist

Everything below is invented for practice. The product, company, application number and owners
do not exist. `000000` is a placeholder application number and resolves to nothing.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt to paste

```text
Use pharma-ci-regulatory-watch. This is a fictional practice run; do not browse or create monitors.
Decisions: (1) know within a day when a competitor in chronic kidney disease anaemia is approved
in the US or gets a CHMP opinion in the EU; (2) know when the Velmarix (fictional, Halden Pharma)
Drugs@FDA record or Orange Book page changes; (3) know if NICE terminates or publishes an
appraisal in that indication. National agency: MHRA, page to be supplied by the reviewer.
Fictional internal review target: the team wants the Velmarix row checked hourly for an
upcoming review. This is an exercise preference, not a statutory deadline. Owner: ri.lead@example.com, backup unassigned.
Use the absolute path of ./pharma-ci in this workspace. Draft the files only.
```

## What the skill drafts

### regulatory-watch.md (table excerpt)

| URL | Agency | Page type | Product | Clock | Interval | Owner | Recheck-by | URL status |
|---|---|---|---|---|---|---|---|---|
| https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026 | FDA | Novel approvals list | class | none | 1440 | ri.lead@example.com | 2027-01-05 (URL year rolls) | unverified (practice) |
| https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=000000 | FDA | Drugs@FDA record | Velmarix (fictional) | internal review target | 60 | ri.lead@example.com | 2026-12-14 | unverified (fictional) |
| https://www.fda.gov/advisory-committees/advisory-committee-calendar | FDA | AdComm calendar | class | none | 1440 | ri.lead@example.com | 2026-12-14 | unverified (practice) |
| https://www.ema.europa.eu/en/committees/chmp | EMA | CHMP highlights | class | none | 1440 | ri.lead@example.com | 2026-12-14 | unverified (practice) |
| https://www.nice.org.uk/guidance/published | NICE | Published guidance | indication | none | 1440 | ri.lead@example.com | 2026-12-14 | unverified (practice) |
| (to be supplied) | MHRA | national agency | Velmarix (fictional) | none | 1440 | ri.lead@example.com | 2026-12-14 | unknown |

The MHRA row is omitted from both CSVs until a URL exists, and the omission is reported. Check
volume: five daily rows and one hourly row, roughly 150 plus 720 checks per month; the hourly row
is shown separately so the reviewer sees the check cost of the chosen schedule.

### regulatory-import.csv (excerpt)

```csv
URL,Title
https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026,FDA novel drug approvals 2026 (practice)
https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=000000,Velmarix Drugs@FDA record (fictional)
https://www.nice.org.uk/guidance/published,NICE published guidance (practice)
```

### regulatory-prompt-guide.csv (one row shown, wrapped for reading)

```csv
url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope
https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026,FDA novel drug approvals 2026 (practice),"Alert me when a new approval is added; give the drug name, active ingredient, approval date and indication. Ignore the ""content current as of"" date and site notices.",1440,ri.lead@example.com,unassigned,2027-01-05,Competitor US approval timing; URL year rolls in January,important,unassigned,known page/record
```

## The three-week alert mix, fictional

| Detected (UTC) | Published | Page | Change | Flagged IMPORTANT | Log note |
|---|---|---|---|---|---|
| 2026-10-02 06:10 | 2026-10-01 | Approvals list | New entry: fictional drug A, indication X | yes | Source fact logged; competitor status hypothesis to test |
| 2026-10-06 06:11 | (none) | Approvals list | "Content current as of" date advanced | no | Stays in change history; nothing to do |
| 2026-10-09 06:09 | 2026-10-08 | Approvals list | New entry: fictional drug B | yes | Logged |
| 2026-10-14 06:12 | 2026-10-13 | Approvals list | New entry: fictional drug C | yes | Logged |
| 2026-10-17 06:10 | (none) | Approvals list | Footer link text edited | no | Stays in change history |
| 2026-10-21 06:11 | 2026-10-20 | Approvals list | New entry: fictional drug D | yes | Logged |

Four fictional events are flagged important and two are unflagged. This establishes
classification only. Receipt and completed review would require separate records. Evaluate any
unwanted classification against the agreed project policy.

## What the dry run would show

```text
CREATE                     https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026  |  FDA novel drug approvals 2026 (practice)
CREATE                     https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=000000  |  Velmarix Drugs@FDA record (fictional)
...
6 rows; roughly 870 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

In a practice run the skill stops here. Nothing is created until a real workspace id is supplied
and the user types `confirm`.
