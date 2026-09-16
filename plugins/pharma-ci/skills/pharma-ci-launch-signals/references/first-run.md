# First run: a fictional launch-signal watchlist

Every company, person, ticker and URL below is fictional. The `.example` domains do not resolve and
the ticker `NRVN` is not a real EDGAR registrant. Use this run to learn the shape of the outputs,
then replace the details with your own.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## The prompt

```text
Use pharma-ci-launch-signals. This is a fictional practice run; do not browse or create monitors.
Decision: tell the Tessaline Bio field-force lead when to start competitor-readiness training for
Norvane Therapeutics' vestrolimab in moderate-to-severe atopic dermatitis, US launch expected
within 18 months. Competitor: Norvane Therapeutics (norvane.example, fictional ticker NRVN).
Reviewer for careers and leadership rows: unassigned. Reviewer for pipeline, newsroom, investor
and EDGAR rows: the CI lead (name withheld). Backup: unassigned. Write the watchlist and both CSVs
under ./pharma-ci-demo/ and show the dry-run plan you would run.
```

## The decision sentence

This watchlist tells the Tessaline field-force lead when to start competitor-readiness training
for vestrolimab, before the training would need to be complete: about six months ahead of a
plausible US launch.

## The monitor table (abridged)

| URL | Status | Page type | Rule (abridged) | Tell | Interval | Owner | Backup | Recheck by |
|---|---|---|---|---|---|---|---|---|
| https://norvane.example/science/pipeline | unverified (practice run) | Pipeline | Program or indication added, removed, phase moved, status changed; state candidate counts by phase before and after; ignore layout and graphics | tests: vestrolimab moves to "filed" or a new indication appears | 10080 | CI lead | unassigned | 2027-01-15 |
| https://careers.norvane.example/search?q=atopic%20dermatitis&country=US | unverified | Careers search | Posting names atopic dermatitis, MSL, medical science liaison, field sales, launch or process engineering; ignore postings outside the US and generic corporate roles | tests: field-force or MSL hiring in dermatology may precede a launch | 1440 | unassigned | unassigned | 2026-12-15 |
| https://norvane.example/about/leadership | unverified | Leadership | Name added or removed, or title changes; name the person and the title | tests: a commercial or medical head for dermatology may arrive before launch | 10080 | unassigned | unassigned | 2027-01-15 |
| https://norvane.example/news | unverified | Newsroom | Release mentions atopic dermatitis, vestrolimab, a partnership, a licensing deal, an approval or a leadership change; ignore awards and CSR | tests: a partnership or approval may reset the timeline | 1440 | CI lead | unassigned | 2026-12-15 |
| https://investors.norvane.example/events | unverified | Investor events | New presentation, transcript, webcast or event posted; give visible title, date and link; read contents separately | tests: readout-timing language may shift | 1440 | CI lead | unassigned | 2026-12-15 |
| https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=NRVN&type=8-K | unverified (fictional ticker) | EDGAR filing list | New 8-K, 10-Q or 10-K appears; name the form type and filing date | tests: a delay or discontinuation may appear first in a filing | 1440 | CI lead | unassigned | 2027-01-15 |

The 10-Q and 10-K rows are added only when the filing list shows a new document; the rule for
those pages is the "10-Q or 10-K document page" rule from `rule-grammar.md` with `[program]`
replaced by `vestrolimab`.

## What the pipeline-page rule buys you

Two weeks into this fictional run the pipeline page is redesigned. The diff is large. The summary reads:

> Layout changed from a table to cards. Phase 1: 3 to 3. Phase 2: 4 to 4. Phase 3: 2 to 2. Filed:
> 0 to 0. No program was added, removed or moved. Not important.

This is a fictional AI summary. The reviewer checks program-level evidence before accepting
its conclusion; unchanged phase totals alone do not prove unchanged programs.

## The two CSVs

`./pharma-ci-demo/launch-signals-import.csv`

```text
URL,Title
https://norvane.example/science/pipeline,Norvane pipeline (fictional)
https://careers.norvane.example/search?q=atopic%20dermatitis&country=US,Norvane careers search AD US (fictional)
https://norvane.example/about/leadership,Norvane leadership (fictional)
https://norvane.example/news,Norvane newsroom (fictional)
https://investors.norvane.example/events,Norvane investor events (fictional)
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=NRVN&type=8-K,Norvane EDGAR 8-K list (fictional ticker)
```

`./pharma-ci-demo/launch-signals-prompt-guide.csv` carries the same rows with the columns
`url,title,rule,interval,owner,backup,recheck_by,decision_served,delivery_policy,maintenance_owner,capture_scope`. The `decision_served` cell for
the careers row reads:

```text
"Field-force training start. tests: dermatology field-force or MSL hiring may precede a US launch"
```

## The dry-run plan you would see

```text
CREATE                     https://norvane.example/science/pipeline  |  Norvane pipeline (fictional)
CREATE                     https://careers.norvane.example/search?q=atopic%20dermatitis&country=US  |  Norvane careers search AD US (fictional)
CREATE                     https://norvane.example/about/leadership  |  Norvane leadership (fictional)
CREATE                     https://norvane.example/news  |  Norvane newsroom (fictional)
CREATE                     https://investors.norvane.example/events  |  Norvane investor events (fictional)
CREATE                     https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=NRVN&type=8-K  |  Norvane EDGAR 8-K list (fictional ticker)

6 rows; roughly 128 checks per month at the listed intervals.
Dry run. Re-run with --confirm to create the CREATE rows.
```

In a real run the skill stops here, shows the plan, and waits for the user to type `confirm`.

## How a first alert would be written up

Fact: on 2026-10-02 at 06:14 (capture time) the careers search returned two new postings dated
2026-10-01, "Dermatology Sales Specialist, Northeast" and "Medical Science Liaison, Immunology,
West". Publication date is the posting date on the page, 2026-10-01.

Hypothesis: dermatology field hiring may indicate launch preparation. To test: posting count over
the next four weeks; any timing language in the next Norvane investor presentation.

Decision served: field-force training start. Stakeholder: Tessaline field-force lead. Timeframe:
revisit at the 2026-12-15 recheck-by date or sooner if the count exceeds five postings.

## Blind spots named in the watchlist file

Norvane's ex-US hiring is not covered; the careers filter is US-only by design. Presentations
posted only as PDF need a separate document monitor. No private-company partner of Norvane is
watched.
