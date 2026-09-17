# Pharma CI Skills

Nine skills for pharma and biotech intelligence teams working with public-page changes. Use them
to build a watchlist, choose which edits reach a reviewer, prepare a review item and write a brief
with evidence and a next action. They accompany the Pharma CI USA 2026 workshop, “A page changed
between reviews. Who needs to know?”

The skills run in Claude Code or Codex. They work from pasted evidence and produce files. Creating
monitors through the Visualping API is optional, always dry-run first, and needs your own API key
(available on every plan, including Free).

## Workshop starter pack

Open the [starter-pack guide](docs/starter-pack/README.md), or download the
[PDF guide](https://github.com/edoc33/pharma-ci-skills/releases/latest/download/pharma-ci-starter-guide.pdf)
and [complete ZIP](https://github.com/edoc33/pharma-ci-skills/releases/latest/download/pharma-ci-starter-pack.zip).
The pack includes 22 public sources across 23 starter URLs, saved evidence and proposed review
tasks. The session uses saved-alert discussions; setup recipes are for use after the session.
Start with the [saved-alert walkthrough](docs/starter-pack/workflow-walkthrough.md). The M365 route
is a configuration recipe with no verified tenant execution. See [third-party asset notices](THIRD_PARTY_NOTICES.md)
for the source screenshots and marks.

## Install

In Claude Code:

```text
/plugin marketplace add edoc33/pharma-ci-skills
/plugin install pharma-ci@pharma-ci
```

Follow the install summary and run `/reload-plugins` if it asks you to. Skills are namespaced
`/pharma-ci:<name>`.

For Codex, clone this repository and run from its root:

```sh
python3 scripts/install_codex.py --dest "$HOME/.agents/skills" --dry-run
python3 scripts/install_codex.py --dest "$HOME/.agents/skills"
```

The installer copies all nine skills with shared references, examples, starter-pack documents and the API helper. It
refuses to replace an existing skill. Python 3.10 or later is needed for the installer, helper and
repository checks.

## Choose a skill

| Your question | Skill | What you get |
|---|---|---|
| What should we watch, and for which decision? | `pharma-ci-watchlist` | A source list with capture policy, reviewer, cadence and maintenance owner; a two-column import CSV and prompt guide |
| Which captured changes should reach the reviewer? | `pharma-ci-rule-writer` | An “Alert me when” rule and delivery-policy recommendation, with the proposed `summalyzer` JSON |
| Which trials should we follow or discover? | `pharma-ci-registry-watch` | Known-record amendment monitoring and scoped list/search discovery, with input and pagination checks |
| Which regulator pages should we follow? | `pharma-ci-regulatory-watch` | Page-specific rules, review ownership and a schedule tied to the team's verified requirements |
| What changed in a competitor's launch or commercial presence? | `pharma-ci-launch-signals` | Brand/HCP, provider, pipeline, careers, newsroom and investor sources, with source facts separated from interpretation |
| What changed in coverage or HTA? | `pharma-ci-access-watch` | Payer, formulary, HTA and guideline monitoring by asset, geography or indication |
| What will competitors present at the congress? | `pharma-ci-congress-watch` | Program and abstract monitoring, source-specific timing and a proposed coverage queue |
| Who owns this alert? | `pharma-ci-review-route` | A review item with owner, backup and status, plus a proposed Microsoft 365 route |
| What should the team know this week? | `pharma-ci-weekly-brief` | A brief separating verified facts, AI summaries, interpretations and proposed actions |

A new program usually starts with watchlist and rule-writer, then a relevant monitoring skill,
review-route and weekly-brief. You can also start with an alert or source list you already have.

## Run your first skill

In Claude Code use `/pharma-ci:pharma-ci-rule-writer`; in Codex use `$pharma-ci-rule-writer`. Paste:

```text
Fictional exercise, inline output, no live tools. We follow a competitor's Phase 3 trial in
[indication]. The input is its ClinicalTrials.gov study record. We need status, completion-date,
eligibility, arm, endpoint and results-disclosure changes. Write the rule and identify any
thresholds that need my decision. Compare every-captured-edit delivery with IMPORTANT-only
delivery. Leave the owner unassigned. Show proposed JSON without applying it.
```

Expect a rule scoped to the captured record, an explicit delivery choice and proposed JSON.
A list-page rule can identify a new link; assessing the linked document requires its contents.

## What the skills know

- [Source selection](plugins/pharma-ci/reference/sources.md) across trial/pipeline, regulatory,
  congress, access and commercial work, including known records and discovery lists.
- [Rule grammar](plugins/pharma-ci/reference/rule-grammar.md) for the six workshop rule families:
  trial record, pipeline, brand/provider, congress program, guideline/access and approval list.
- [The API subset](plugins/pharma-ci/reference/visualping-api.md) and
  [helper script](scripts/vp_client.py): `whoami`, `jobs`, `changes`, `feed`, `create` and `bulk`.
- [The Microsoft 365 route](plugins/pharma-ci/reference/m365-route.md) from captured evidence to
  a proposed review item.
- [Examples](plugins/pharma-ci/examples/) for source imports, rules, review items and triage.
- [First runs](docs/getting-started.md) you can complete with pasted inputs and no live tools.

## Principles the skills enforce

- Match the captured input to the watch question. Known records reveal amendments; scoped
  lists and searches support discovery. Check search criteria and pagination.
- Choose delivery explicitly: every captured edit, or changes flagged IMPORTANT. Sensitive
  brand/HCP work may require single-word, punctuation and image edits.
- Every change event has a binary IMPORTANT flag and an AI Summary. Delivery filtering is a
  configuration choice; a classification alone does not prove receipt or human review.
- Keep source facts, AI summaries, interpretations and proposed actions separate. Stable
  aggregate counts alone do not establish that individual records stayed unchanged.
- Record detection time and source dates separately. Establish a publication time only when
  the source supports it.
- Name the reviewer and backup. Also name who checks failed monitors, moved pages and newly
  published pages. Leave unknown assignments explicitly unassigned.
- Set cadence for the decision and the review deadline. Verify any legal duty or deadline for
  the applicable jurisdiction and event before treating it as a requirement.
- Monitoring history supports current awareness. Regulated record requirements need separate
  validation.
- Creating, changing or deleting monitors is shown first and waits for the word `confirm`.

## Check the package

```sh
python3 -m unittest discover -s tests
```

## License

MIT. Visualping is a trademark of its owner. This community skill set uses its public API and is
not an official Visualping product.
