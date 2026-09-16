# First run: a fictional congress watchlist and coverage queue

Everything below is invented for practice. The molecule, sponsor, abstracts, dates and owners do
not exist. `LBA0000` and `0000P` are placeholder identifiers.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt to paste

```text
Use pharma-ci-congress-watch. This is a fictional practice run; do not browse or create monitors.
Meeting: a fictional oncology congress, "Northfield Oncology Congress 2027", 12 to 15 June 2027.
Portal (fictional): https://northfield-congress.example/2027/abstracts
Milestones (fictional): titles 3 May, abstracts 2 June, late-breakers embargo lift 13 June 08:00 CEST.
Name in the rule: ORD-2210 (fictional), second-line urothelial carcinoma, competitor Ordell
Biosciences (fictional). Owner: med.affairs@example.com, backup unassigned.
Use the absolute path of ./pharma-ci in this workspace. Draft the files only.
```

## What the skill drafts

### congress-watch.md (table excerpt)

| URL | Congress | Cycle | Page type | Current interval | Season boundaries | Owner | Recheck-by | URL status |
|---|---|---|---|---|---|---|---|---|
| https://northfield-congress.example/2027/abstracts | Northfield Oncology (fictional) | 2027 | abstract search | 10080 (off-season) | 2027-05-01 to 1440; 2027-06-02 to 60; 2027-06-03 to 1440; 2027-06-13 to 60; 2027-06-14 to 1440; 2027-06-16 to 10080 | med.affairs@example.com | 2027-06-16 (retire or repoint) | unverified (fictional) |

Rule for the row: "Alert me when a session, abstract or late-breaker title names ORD-2210,
urothelial carcinoma or Ordell Biosciences. Give the abstract or session identifier, the title and
the posted date if shown. Ignore schedule formatting."

Check volume by season: about 4 checks a week off-season, 7 a week from 1 May, 24 on each of the
two hourly days. Blind spots named: embargoed abstract text, encore presentations at other
meetings, and a portal that lists titles only behind registration.

### congress-import.csv

```csv
URL,Title
https://northfield-congress.example/2027/abstracts,Northfield Oncology 2027 abstracts (fictional)
```

### congress-prompt-guide.csv (current season, wrapped for reading)

```csv
url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope
https://northfield-congress.example/2027/abstracts,Northfield Oncology 2027 abstracts (fictional),"Alert me when a session, abstract or late-breaker title names ORD-2210, urothelial carcinoma or Ordell Biosciences. Give the abstract or session identifier, the title and the posted date if shown. Ignore schedule formatting.",10080,med.affairs@example.com,unassigned,2027-05-01,Congress coverage plan; move to daily on 2027-05-01,important,unassigned,known page/record
```

## Alerts, triaged (fictional)

| Detected (UTC) | Posted | Entry | Paper type | Trial type | Patients | Focus | Competitor named |
|---|---|---|---|---|---|---|---|
| 2027-05-03 09:04 | 2027-05-03 | 0000P: ORD-2210 real-world dosing patterns | poster | real-world | unknown | safety | yes |
| 2027-05-03 09:04 | 2027-05-03 | Session: second-line urothelial carcinoma, new agents | program session | n/a | n/a | n/a | no |
| 2027-06-13 06:02 | 2027-06-13 06:00 | LBA0000: ORD-2210 vs standard of care, randomised Phase 3 | late-breaking oral | randomised controlled | 612 (title) | efficacy | yes |

### congress-coverage-queue.csv

```csv
abstract_id,title,portal_url,paper_type,trial_type,patient_count,focus,competitor_named,session_time,owner,next_action,recheck_by
"LBA0000","ORD-2210 vs standard of care, randomised Phase 3 (fictional)","https://northfield-congress.example/2027/abstracts","late-breaking oral","randomised controlled","612","efficacy","yes","2027-06-13 10:30 CEST","med.affairs@example.com","attend session; brief medical same day","2027-06-16"
"0000P","ORD-2210 real-world dosing patterns (fictional)","https://northfield-congress.example/2027/abstracts","poster","real-world","unknown","safety","yes","2027-06-14 poster hall","unassigned","request poster","2027-06-16"
"session-ULC-2L","Second-line urothelial carcinoma, new agents (fictional)","https://northfield-congress.example/2027/abstracts","program session","n/a","n/a","n/a","no","2027-06-12 14:00 CEST","unassigned","no action; note in coverage plan","2027-06-16"
```

The change log records, for LBA0000, the source fact ("late-breaker title names ORD-2210 versus
standard of care, 612 patients in the title") and the hypothesis separately ("likely the Phase 3
readout registered as NCT00000000; confirm against the registry record after the session").

## What the dry run would show

```text
CREATE                     https://northfield-congress.example/2027/abstracts  |  Northfield Oncology 2027 abstracts (fictional)

1 rows; roughly 4 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

In a practice run the skill stops here. Nothing is created until a real workspace id is supplied
and the user types `confirm`. At the 1 May boundary the owner regenerates the prompt guide with
`"1440"` and changes the interval in the web app; `vp_client.py` does not update existing rows.
