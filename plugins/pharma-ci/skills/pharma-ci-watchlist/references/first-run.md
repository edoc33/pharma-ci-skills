# First run: a fictional competitor launch watchlist

Everything below is invented for practice. Companies, drugs, people, domains and identifiers are
fictional; `NCT00000000` and `.example` domains are placeholders. Nothing here describes a real
account or a real monitor.

## Exercise policy

This fictional exercise selects `delivery_policy: important` and a completion-date threshold
of more than 90 days. These are exercise choices, not default requirements.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt

```text
Use pharma-ci-watchlist. This is a fictional practice run; do not browse or create monitors.
Scope: Corrimel Bio is expected to launch tavrelimab in IgA nephropathy in the US and Germany.
We are Halvane Therapeutics; our own program is orvasertib, Phase 3, readout expected 2027.
Decisions: (1) decide by Q1 2027 whether to change our US launch sequence if tavrelimab gains
reimbursement first; (2) decide whether to move our readout communication earlier if the
competitor trial slips. Owner for both: ri.lead@halvane.example, backup ci.analyst@halvane.example.
Market access rows: ma.lead@halvane.example, no backup yet. One analyst reads alerts daily.
Supplied URLs: https://clinicaltrials.gov/study/NCT00000000 (competitor Phase 3 record),
https://corrimel.example/pipeline, https://corrimel.example/news.
```

## What the skill produced

### `./pharma-ci/watchlist-import.csv`

```csv
URL,Title
https://clinicaltrials.gov/study/NCT00000000,Corrimel tavrelimab Phase 3 record (IgAN)
https://clinicaltrials.gov/search?cond=IgA%20Nephropathy&aggFilters=phase%3A3,Phase 3 IgAN studies search
https://corrimel.example/pipeline,Corrimel pipeline
https://corrimel.example/news,Corrimel newsroom
https://corrimel.example/careers?function=medical,Corrimel careers (medical and field)
https://corrimel.example/about/leadership,Corrimel leadership
https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026,FDA novel drug approvals 2026
https://www.fda.gov/advisory-committees/advisory-committee-calendar,FDA advisory committee calendar
https://www.g-ba.de/themen/arzneimittel/arzneimittel-richtlinie-anlagen/nutzenbewertung-35a/,G-BA benefit assessments
https://www.nice.org.uk/guidance/published,NICE published guidance
https://vellmark.example/providers/policies/specialty-drugs,Vellmark Health specialty drug policy index
```

Eleven rows written; two rows omitted because the URL is `unknown` (Corrimel SEC filing list, no
ticker supplied; the 2027 nephrology congress portal, not yet published).

### `./pharma-ci/watchlist-prompt-guide.csv` (three of thirteen rows shown)

```csv
url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope
https://clinicaltrials.gov/study/NCT00000000,Corrimel tavrelimab Phase 3 record (IgAN),"Alert me when the overall status, primary completion date (by more than 90 days), number of arms, enrollment target, or a primary endpoint changes. Ignore version labels, last-update dates and site-list edits unless a site is added or removed in the US or Germany.",1440,ri.lead@halvane.example,ci.analyst@halvane.example,2027-03-31,Decide whether to move the orvasertib readout communication earlier if the tavrelimab trial slips,important,unassigned,known page/record
https://corrimel.example/careers?function=medical,Corrimel careers (medical and field),"Alert me when a posting names IgA nephropathy, nephrology, MSL, medical science liaison, field sales, or launch. Ignore postings outside the US and Germany and generic corporate roles.",1440,ri.lead@halvane.example,ci.analyst@halvane.example,2026-12-15,Decide by Q1 2027 whether to change the US launch sequence if tavrelimab gains reimbursement first,important,unassigned,scoped discovery list/search
https://vellmark.example/providers/policies/specialty-drugs,Vellmark Health specialty drug policy index,"Alert me when tavrelimab coverage criteria, step therapy, prior authorization, quantity limits or tier change. Ignore chat widgets, search hints and layout.",10080,ma.lead@halvane.example,owner: unassigned,2026-12-15,Decide by Q1 2027 whether to change the US launch sequence if tavrelimab gains reimbursement first,important,unassigned,known page/record
```

### `./pharma-ci/watchlist-notes.md` (summary)

- Decisions: two, both owned by `ri.lead@halvane.example`. Market access rows owned by
  `ma.lead@halvane.example` with `owner: unassigned` in the backup column (3 rows).
- Eight-source coverage: careers, leadership, pipeline and payer bulletin included. Investor
  events, SEC filings excluded until a ticker or investor page is supplied (`unknown`). Orange
  Book excluded: tavrelimab is a biologic, no Orange Book listing expected. TV-ad archive
  excluded until launch; recheck 2027-01-15. The source choices follow the fictional decisions; no adoption claim is implied.
- URL status: 3 `supplied`, 8 `unverified` (fictional run, nothing was opened), 2 `unknown`.
- Checks per month: 10 daily rows and 3 weekly rows, roughly 312 checks.
- Blind spots: private payer contracts, unannounced label negotiations, German regional
  prescribing data, any congress whose portal is not yet live.

## The dry-run exchange

The user later supplied workspace `12345` and asked for creation.

```text
$ python3 scripts/vp_client.py bulk --workspace 12345 --csv ./pharma-ci/watchlist-prompt-guide.csv --delivery important
CREATE                     https://clinicaltrials.gov/study/NCT00000000  |  Corrimel tavrelimab Phase 3 record (IgAN)
CREATE                     https://corrimel.example/pipeline  |  Corrimel pipeline
...
13 rows; roughly 312 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

The skill then said: "This will create 13 monitors in workspace 12345. Type `confirm` to proceed,
or edit the CSV first." Only after the user typed `confirm` did it run the same command with
`--confirm` appended. Rows already monitored at the same URL would have printed `SKIP`.

## What this run did not establish

No URL was verified. No alert has fired, so no rule has a score yet. The watchlist is a plan with
a named owner for ten of thirteen rows; the three unassigned backups are the first thing to fix.
