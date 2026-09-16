# Pharma CI Skills

Nine skills for pharma and biotech intelligence teams who want to stop checking pages by hand.
They come from a workshop at Pharma CI USA 2026 ("The page changed first. You heard about it
second.") and turn the playbook shown there into something you can run: build a decision-linked
watchlist, write the rule before you add the page, set up the monitors, route each alert to a named
owner, and publish a weekly brief that connects every item to a decision.

The skills run in Claude Code or Codex. They work from pasted evidence and produce files; creating
monitors through the Visualping API is optional, always dry-run first, and needs your own API key
(available on every plan, including Free).

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

The installer copies all nine skills with their shared reference files and the API helper. It
refuses to replace an existing skill. Python 3.10 or later is needed only for the installer, the
helper and the repository checks.

## Choose a skill

| Your question | Skill | What you get |
|---|---|---|
| What should we watch, and for which decision? | `pharma-ci-watchlist` | A watchlist across the five jobs and the eight under-watched sources, as a two-column import CSV plus a prompt guide with owner, cadence and recheck-by |
| How do I say what matters on this page? | `pharma-ci-rule-writer` | An "Alert me when" importance rule with named fields, thresholds and ignores, plus the JSON to send |
| Which competitor trials should we follow? | `pharma-ci-registry-watch` | Record-level monitors on ClinicalTrials.gov and CTIS with the registry rule, and the discipline for reading an amendment |
| Which regulator pages, and how often? | `pharma-ci-regulatory-watch` | FDA, EMA, NICE, Orange Book and national-agency monitors with per-page rules and statutory cadences |
| What precedes a competitor launch? | `pharma-ci-launch-signals` | Pipeline, careers, leadership, newsroom, investor and SEC-filing monitors with the tell for each |
| What changed in coverage or HTA? | `pharma-ci-access-watch` | Payer bulletin, formulary, HTA and guideline monitors organised by asset, geography or indication |
| What will competitors present at the congress? | `pharma-ci-congress-watch` | Abstract and program portal monitors with a seasonal cadence and a coverage queue |
| Who owns this alert? | `pharma-ci-review-route` | A review item with owner, backup and status, and the Microsoft 365 route (shared mailbox, Power Automate, SharePoint, Teams optional) |
| What should the team know this week? | `pharma-ci-weekly-brief` | A one-page brief where every item names a decision, a stakeholder and a timeframe |

Start with the skill that matches the input you already have. A new program usually runs
watchlist, then rule-writer, then one monitor skill, then review-route, then weekly-brief.

## Run your first skill

In Claude Code use `/pharma-ci:pharma-ci-rule-writer`; in Codex use `$pharma-ci-rule-writer`. Paste:

```text
Fictional exercise, inline output, no live tools. We follow a competitor's Phase 3 trial in
[indication]. Tell me when the trial slips or its design changes, but not when the record is
tidied. Write the rule for the ClinicalTrials.gov record page.
```

You should get a rule that names status, primary completion date with a threshold, arms,
enrollment target and primary endpoint, says what to ignore, and comes back as text and as the
`summalyzer` JSON object.

## What the skills know

- [The five jobs and the eight under-watched sources](plugins/pharma-ci/reference/sources.md),
  with platform counts from 15 September 2026 showing how rarely pharma-sector teams watch
  careers pages, leadership pages, investor materials, SEC filings, payer bulletins and patent
  registers compared with the rest of the platform.
- [Rule grammar](plugins/pharma-ci/reference/rule-grammar.md): how to write an importance rule
  for every page type, and how to score it after a month.
- [The API subset](plugins/pharma-ci/reference/visualping-api.md) the skills call, and the
  [helper script](scripts/vp_client.py) that wraps it (`whoami`, `jobs`, `changes`, `feed`,
  `create`, `bulk`).
- [The Microsoft 365 route](plugins/pharma-ci/reference/m365-route.md) from alert to owned
  review item.
- [Examples](plugins/pharma-ci/examples/): a 20-source starter import, its prompt guide, a source
  directory with recheck-by dates, a review-item template and a triage prompt.

## Principles the skills enforce

- Write the rule before you add the page. A page without a rule is noise.
- Watch the record, not the search. Nineteen of twenty registry monitors on the platform do.
- Detection time is not publication time. Record both.
- Source fact first, inference second. A registry amendment is a fact; what it means is a
  hypothesis to test.
- Every route has a named owner and a backup, or the skill writes `owner: unassigned` and says so.
- The value is coverage, a defensible record and a named owner. Speed matters only where a
  statutory or embargo clock runs, and you know which pages those are.
- The change archive is a current-awareness record, not a validated records system.
- Creating, changing or deleting monitors is always shown first and waits for the word `confirm`.

## Check the package

```sh
python3 -m unittest discover -s tests
```

## License

MIT. Visualping is a trademark of its owner; this repository is a community set of skills that use
its public API and is not an official Visualping product.
