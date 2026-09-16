# First run: a fictional access watchlist organised by asset

Every company, payer, product and person below is fictional. The `.example` domains do not
resolve. Agency URLs are shown as patterns; the drug filters in them name fictional products and
return nothing on the live sites. Use this run to learn the shape of the outputs, then replace the
details with your own.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## The prompt

```text
Use pharma-ci-access-watch. This is a fictional practice run; do not browse or create monitors.
Axis: asset. Own asset: parnetide (Tessaline Bio) in chronic kidney disease anaemia, launched in
the US and UK, German benefit assessment pending. Competitor asset: vestrolimab (Norvane
Therapeutics), same indication, UK appraisal in progress, US commercial coverage live with two
national payers. Geographies: US, UK, Germany. Reviewers: parnetide asset lead (name withheld),
UK and Germany access leads (unassigned), nephrology therapy-area lead (name withheld).
Decisions: keep the payer objection guide current; re-time the German dossier assumptions.
Write the watchlist and both CSVs under ./pharma-ci-demo/ and show the dry-run plan.
```

## Group 1: parnetide (own asset)

Decision sentence: these rows tell the parnetide asset lead when to update the payer objection
guide and tell the Germany access lead when a G-BA resolution changes the dossier assumptions.

| URL | Status | Source family | Geography | Rule (abridged) | Interval | Owner | Backup | Recheck by |
|---|---|---|---|---|---|---|---|---|
| https://www.harrowgatehealth.example/providers/policies?search=parnetide | unverified | Payer policy bulletin | US | parnetide coverage criteria, step therapy, prior authorization, quantity limits or tier change; ignore chat widgets, search hints, session text and layout | 10080 | parnetide asset lead | unassigned | 2026-12-01 |
| https://www.g-ba.de/... (resolution list filtered to parnetide) | unverified | G-BA benefit assessment | Germany | resolution published or revised for parnetide; state ingredient, indication, added-benefit category, resolution date; say whether draft or final | 1440 until the resolution date, then 10080 | unassigned (Germany access lead) | unassigned | 2026-11-20 |
| https://www.nice.org.uk/guidance/published | unverified | NICE published list | UK | new TA or NG appears, or an entry is marked terminated or withdrawn; name the reference and the date; ignore pagination and reordering | 10080 | unassigned (UK access lead) | unassigned | 2026-12-15 |

## Group 2: vestrolimab (competitor asset)

Decision sentence: these rows tell the parnetide asset lead when competitor coverage terms change
so the objection guide compares like with like.

| URL | Status | Source family | Geography | Rule (abridged) | Interval | Owner | Backup | Recheck by |
|---|---|---|---|---|---|---|---|---|
| https://www.harrowgatehealth.example/providers/policies?search=vestrolimab | unverified | Payer policy bulletin | US | vestrolimab coverage criteria, step therapy, prior authorization, quantity limits or tier change; ignore chat widgets, search hints, session text and layout | 10080 | parnetide asset lead | unassigned | 2026-12-01 |
| https://formulary.cobaltriver.example/drug-list.pdf | unverified (PDF) | Formulary | US | vestrolimab or parnetide tier, step therapy or prior authorization flag changes; ignore the revision date line alone | 10080 | parnetide asset lead | unassigned | 2026-12-01 |
| https://www.nice.org.uk/guidance/indevelopment/gid-example | unverified (fictional GID) | NICE appraisal in progress | UK | status, expected dates, documents or recommendation change; say draft or final; keep document maintenance separate from a new recommendation | 10080, 1440 in the two weeks before the committee date | unassigned (UK access lead) | unassigned | 2026-11-05 |

## Group 3: guideline (indication column, therapy-area lead)

| URL | Status | Source family | Rule (abridged) | Interval | Owner | Backup | Recheck by |
|---|---|---|---|---|---|---|---|
| public guideline version page for anaemia of CKD (society site) | unverified | Clinical guideline | guideline version for anaemia of CKD is updated or a recommendation category changes; state the version before and after | 10080 | nephrology therapy-area lead | unassigned | 2027-01-15 |

## Why the payer rule says what it ignores

A payer index page in a real run changed on every daily load: the chat widget greeting rotated,
the "popular searches" box listed different drugs, and a session token sat in the footer. With
the ignore clause the summary read:

> Chat widget text and search hints changed. No policy row for vestrolimab was added, removed or
> edited. Not important.

Without it, the row fired every day and the asset lead stopped reading the alerts.

## The two CSVs

`./pharma-ci-demo/access-import.csv`

```text
URL,Title
https://www.harrowgatehealth.example/providers/policies?search=parnetide,Harrowgate policy search parnetide (fictional)
https://www.harrowgatehealth.example/providers/policies?search=vestrolimab,Harrowgate policy search vestrolimab (fictional)
https://formulary.cobaltriver.example/drug-list.pdf,Cobalt River formulary PDF (fictional)
https://www.nice.org.uk/guidance/published,NICE published guidance list
```

The G-BA, NICE appraisal and guideline rows are omitted from the import file until their URLs are
verified on the live sites; the watchlist file lists them under "omitted, unverified".

`./pharma-ci-demo/access-prompt-guide.csv` carries the verified rows with the columns
`url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope`. The `decision_served` cell for
the Harrowgate vestrolimab row reads "Payer objection guide (competitor coverage terms)".

## The dry-run plan you would see

```text
CREATE                     https://www.harrowgatehealth.example/providers/policies?search=parnetide  |  Harrowgate policy search parnetide (fictional)
CREATE                     https://www.harrowgatehealth.example/providers/policies?search=vestrolimab  |  Harrowgate policy search vestrolimab (fictional)
CREATE                     https://formulary.cobaltriver.example/drug-list.pdf  |  Cobalt River formulary PDF (fictional)
CREATE                     https://www.nice.org.uk/guidance/published  |  NICE published guidance list

4 rows; roughly 17 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

The skill stops here and waits for the user to type `confirm`.

## How a first alert would be written up

Fact: on 2026-10-09 at 07:02 (capture time) the Harrowgate policy search for vestrolimab showed a
revised policy dated 2026-10-07; step therapy now requires a documented trial of one
erythropoiesis-stimulating agent before vestrolimab. Publication date is the policy's effective
date on the page, 2026-10-07.

Hypothesis: the new step may narrow vestrolimab's first-line position with this payer. To test:
the full policy PDF; whether parnetide's policy at the same payer carries the same step.

Decision served: payer objection guide. Stakeholder: parnetide asset lead. Timeframe: update the
guide before the next field cycle briefing.

## Blind spots named in the watchlist file

Two national US payers publish bulletins only behind a provider login; they stay `blocked`. The
German procedure page is unverified until the Germany access lead confirms the URL. No French HAS
row exists because parnetide has no French launch planned in the horizon.
