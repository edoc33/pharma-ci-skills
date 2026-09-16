# Pharma CI starter pack

Build one source watch, one relevance rule and one review route. This pack matches the revised Pharma CI USA workshop for September 17, 2026, 11:15-11:45 EDT. Updated September 16.

Open [the offline handout](index.html), or read [the short PDF](pharma-ci-starter-guide.pdf). Download the [complete ZIP](https://github.com/edoc33/pharma-ci-skills/releases/latest/download/pharma-ci-starter-pack.zip). After download, the local material works offline; live source links need internet.

## Start with one source

Follow [first-run.md](first-run.md). The manual first run needs no monitoring subscription, API key or M365 connection. Use an available feed or API when it exposes the required fields. Test page monitoring when you need a visual or text comparison.

The directory contains **22 source entries across 23 URLs**. Novartis has two pages. These are public workshop examples selected independently of customer watchlists. Replace the trial, appraisal, therapy area and congress year with your own scope. Add sources individually before expanding.

| File | Use |
|---|---|
| [source-directory.csv](source-directory.csv) | Sources, complete prompts, cadence examples, coverage limits and maintenance owner |
| [import-tab.csv](import-tab.csv) | Two columns only: URL and Title; paste into the Business-plan Bulk Import workflow |
| [prompt-guide-tab.csv](prompt-guide-tab.csv) | Prompt and settings guidance for each row |
| [api-watchlist.csv](api-watchlist.csv) | Optional API helper format; daily example cadence, unassigned owners and delivery choice left blank |
| [core-rules.md](core-rules.md) | Six rule families and the choice between every-change and IMPORTANT-only delivery |
| [evidence/README.md](evidence/README.md) | Actual saved FDA, NICE, trial, Pfizer and CVS comparisons with provenance |
| [evidence-exercises.md](evidence-exercises.md) | Source-check and rule-scope exercises with answers |
| [triage-prompt.txt](triage-prompt.txt) | Draft a review item from supplied evidence |
| [review-item-template.csv](review-item-template.csv) | Empty evidence, classification, ownership and maintenance fields |
| [review-item-schema.json](review-item-schema.json) | Field dictionary; validate destination types before integration |
| [m365-workflow.md](m365-workflow.md) | Shared mailbox to SharePoint review queue; Teams notification optional |
| [demo-dry-run.md](demo-dry-run.md) | Eight-minute build, evidence mapping and truthful fallback |
| [saved-event-manifest.json](saved-event-manifest.json) | Source evidence is bundled; workflow run and recording remain unverified |
| [fda-public-change-example.json](fda-public-change-example.json) | Optional historical July meeting-time exercise with illustrative routing |
| [fictional-example.json](fictional-example.json) | Separate synthetic practice input |
| [link-verification.md](link-verification.md) | Dated reachability checks and capture-preview limits |

## Optional Visualping setup

Add the URL individually, inspect the preview and select the content needed by the reviewer. The first capture establishes a baseline. Every detected change has a binary IMPORTANT flag and an AI Summary. Choose whether the reviewer receives every captured edit or only changes flagged IMPORTANT. A prompt cannot recover content excluded from the capture.

For small brand, HCP, image or wording edits, test a sensitive capture and every-edit delivery when required by the brief. Test a known relevant change, a small relevant edit and a routine edit before relying on filtering. Keep the saved comparison available to the reviewer.

Bulk Import is a Business-plan feature. Paste the two columns from `import-tab.csv`, then configure selection, cadence, prompts and delivery. Other plans can add URLs individually. API keys are available on every plan. See [Visualping signup](https://visualping.io/sign-up) and the [optional skills repository](https://github.com/edoc33/pharma-ci-skills).

The optional API helper uses `api-watchlist.csv`, whose lowercase fields differ from the two-column dashboard import. Replace bracketed scope, choose the rows, owners and cadence, then set each row's `delivery_policy` to `all` or `important` before a confirmed write. The helper can also accept an explicit common `--delivery` choice. Its dry run creates nothing. See the repository's API reference before using it.

## Choose your first workflow

Record the source and exact watch question, reviewer and backup, destination, delivery choice, maintenance owner, success measure and review date. The maintenance owner checks failed monitors, changed page structure, pagination, newly published pages and annual URL rollovers.

Count whether items reached their owner and were useful. Compare known relevant edits against the archive before expanding coverage. The M365 recipe has not been executed in an attendee tenant. Saved source comparisons do not establish a successful workflow run or business outcome.

Source-comparison excerpts retain third-party rights. See [third-party notices](THIRD_PARTY_NOTICES.md).
