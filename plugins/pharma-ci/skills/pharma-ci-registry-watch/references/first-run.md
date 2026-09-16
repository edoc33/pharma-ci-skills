# First run: a fictional registry watchlist

Everything below is invented for practice. The sponsor, molecule, owners and identifiers do not
exist. `NCT00000000` and `2024-000000-00-00` are placeholders and resolve to nothing.

## Exercise policy

This fictional exercise selects `delivery_policy: important` and a completion-date threshold
of more than 90 days. These are exercise choices, not default requirements.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt to paste

```text
Use pharma-ci-registry-watch. This is a fictional practice run; do not browse or create monitors.
Decision: know at least a quarter ahead if the Ordell Biosciences Phase 3 in moderate-to-severe
atopic dermatitis will read out before ours, and whether Ordell opens sites in Germany or Poland.
Program: ORD-2210, Ordell Biosciences (fictional). Records: NCT00000000 (Phase 3, global) and
CTIS 2024-000000-00-00 (EU). Milestone watch on the NCT record; country-site watch on the CTIS
record for Germany and Poland. One discovery search on sponsor "Ordell".
Owner: ci.lead@example.com, backup unassigned. Capacity: ten alerts a week.
Use the absolute path of ./pharma-ci in this workspace. Draft the files only.
```

## What the skill drafts

### registry-watch.md (table excerpt)

| URL | Registry | Row type | Watchlist type | Decision served | Interval | Owner | Recheck-by | URL status |
|---|---|---|---|---|---|---|---|---|
| https://clinicaltrials.gov/study/NCT00000000 | ClinicalTrials.gov | record | milestone | Readout timing vs ours | 1440 | ci.lead@example.com | 2026-12-14 | unverified (fictional) |
| https://euclinicaltrials.eu/ctis-public/view/2024-000000-00-00 | CTIS | record | country-site | Site competition DE/PL | 1440 | ci.lead@example.com | 2026-12-14 | unverified (fictional) |
| https://clinicaltrials.gov/search?spons=Ordell&sort=StudyFirstPostDate | ClinicalTrials.gov | search | discovery | New Ordell records | 1440 | ci.lead@example.com | 2026-12-14 | unverified (fictional) |

Check volume: 3 rows at daily checks, 90 checks in a 30-day month. This does not predict alert
volume or show that the reviewer's ten-alert weekly capacity will be sufficient. Blind spots named: results posting after
completion, records registered only on a national registry, and any change the sponsor makes
without amending the public record.

### registry-import.csv

```csv
URL,Title
https://clinicaltrials.gov/study/NCT00000000,ORD-2210 Phase 3 AD record (fictional)
https://euclinicaltrials.eu/ctis-public/view/2024-000000-00-00,ORD-2210 CTIS record DE/PL (fictional)
https://clinicaltrials.gov/search?spons=Ordell&sort=StudyFirstPostDate,Ordell new records search (fictional)
```

### registry-prompt-guide.csv (one row shown, wrapped for reading)

```csv
url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope
https://clinicaltrials.gov/study/NCT00000000,ORD-2210 Phase 3 AD record (fictional),"Alert me when the overall status, primary completion date (by more than 90 days), number of arms, enrollment target, or a primary endpoint changes. Ignore version labels, last-update dates and all site-list edits.",1440,ci.lead@example.com,unassigned,2026-12-14,Readout timing vs ours,important,unassigned,known page/record
```

The CTIS row keeps the site clause: "... unless a site is added or removed in Germany or Poland.
Name the site, city and country in the summary."

### registry-amendment-log.md (first row, fictional)

| Detected (UTC) | Published | Record | Field | Before | After | Source fact | Hypothesis | Verified by | Next action |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 06:14 | Last Update Posted 2026-10-01 | NCT00000000 | Primary completion date | 2027-03 (estimated) | 2027-09 (estimated) | Date moved from March to September (month-level dates); status unchanged; arms unchanged | Enrollment slower than planned; test against the sponsor's next quarterly update | ci.lead@example.com | Note in the readout-timing brief; recheck record 2026-12-14 |

## What the dry run would show

```text
CREATE                     https://clinicaltrials.gov/study/NCT00000000  |  ORD-2210 Phase 3 AD record (fictional)
CREATE                     https://euclinicaltrials.eu/ctis-public/view/2024-000000-00-00  |  ORD-2210 CTIS record DE/PL (fictional)
CREATE                     https://clinicaltrials.gov/search?spons=Ordell&sort=StudyFirstPostDate  |  Ordell new records search (fictional)

3 rows; roughly 90 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

In a practice run the skill stops here. Nothing is created until a real workspace id is supplied
and the user types `confirm`.
