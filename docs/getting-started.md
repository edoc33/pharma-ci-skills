# First runs

Install using the [repository README](../README.md). Every exercise below is fictional and works
without live tools. Paste a prompt after invoking the named skill. Ask for inline output on your
first run; file output goes in `./pharma-ci/` in your working directory.

Claude Code names skills `/pharma-ci:pharma-ci-watchlist`; Codex names them `$pharma-ci-watchlist`.
Each installed skill carries `references/first-run.md` with a worked example.

## Connect the API (optional)

1. Create a key in the [Visualping developer settings](https://visualping.io/account/developer), available on every plan.
2. Set `VISUALPING_API_KEY` in the shell that runs Claude Code or Codex. Keep the value out of prompts and files committed to this repository.
3. Run `python3 scripts/vp_client.py whoami` and select the workspace you intend to use.

The helper previews `create` and `bulk` requests by default. The skills ask for `confirm` before
adding `--confirm`. A preview or file output does not establish a live monitor, successful check
or delivered message.

## Update an existing installation

Claude Code, user scope:

```sh
claude plugin marketplace update pharma-ci
claude plugin update pharma-ci@pharma-ci
claude plugin list
```

Check that the listed version matches the repository release, then run `/reload-plugins` or start
a new session. For project or local scope add `--scope project` or `--scope local` and run from
that project.

Codex: pull the latest `main`, move your existing `pharma-ci-*` skill folders out of the destination
(the installer refuses collisions and does not merge edits), rerun the two installer commands,
then restart Codex.

## Build a watchlist

Invoke `pharma-ci-watchlist` and paste:

```text
Fictional exercise, inline output, no browsing. We are launching in [indication] in 2027 against
two fictional competitors, Northwind Therapeutics and Contoso Bio. Decisions this quarter are
launch sequence and field coverage. Propose a minimum watchlist across the five workshop jobs.
For each row, say whether it monitors a known record, discovers new entries, or reads a document.
Include capture policy, reviewer/backup and someone to check new/moved pages and failed monitors.
Leave unknown URLs, assignments and dates unresolved rather than inventing them.
```

Expect a two-column import CSV and a separate prompt guide. The guide should include the captured
input, the decision served, delivery choice, cadence, ownership and a source recheck plan. Review
newly discovered pages before adding them to ongoing monitoring.

## Choose the capture policy and write a rule

Invoke `pharma-ci-rule-writer` and paste:

```text
Fictional exercise, inline output, no live tools. We have two projects. The first needs every
captured change to a competitor HCP claim, including punctuation and small images. The second
needs notification when a pipeline program is added, removed, changes phase or changes status.
Recommend a delivery policy for each, write rules scoped to the captured page, and show the
proposed settings without applying them. Leave unsupported settings unresolved.
```

Every event carries an IMPORTANT flag and an AI Summary. Important-only delivery is optional.
Choose the project policy before filtering. Inspect before/after evidence when an AI summary
omits a detail the project needs.

## Pick a workshop rule family

These are starting rules to adapt to the actual captured input and review policy.

| Input | Starting rule |
|---|---|
| Trial record | Alert me when status, dates, eligibility, arms, endpoints or results disclosures change. |
| Pipeline page | Alert me when a program is added, removed, changes phase or changes status. |
| Brand/provider page | Alert me when product claims, wording, imagery, price, availability or prominence change. |
| Congress program | Alert me when a relevant session is added or its time changes. |
| Guideline/access page | Alert me when this guideline's version or [drug] coverage criteria change. |
| Regulatory approval list | Alert me when [drug] is added to this approval list. |

A known study record supports amendment monitoring. A scoped registry search supports discovery.
Check the results view and pagination, then separately monitor newly found records when their
later changes matter. To assess a linked label PDF, filing or presentation, open or monitor the
document itself.

## Review a commercial change

Invoke `pharma-ci-launch-signals` and paste:

```text
Fictional exercise, inline output. Pasted comparison: a provider treatment page changes a
product's price, relative prominence and availability text. Separate the observed changes from
possible commercial implications. Propose a brand or commercial reviewer, a backup and the next
source check. Do not infer market-share change, launch status or a completed customer action.
```

## Route an alert

Invoke `pharma-ci-review-route` and paste:

```text
Fictional exercise, inline output. A published-guidance list added an appraisal for a competitor
product on 9 September. The saved event was detected that day at 17:55 UTC. Our UK access lead
owns the asset. Draft the review item and a proposed Microsoft 365 route. Leave the backup
unassigned. Keep recommendation and eligible population unverified until the source is read.
Use the project delivery policy; preserve an unknown IMPORTANT value for review.
```

A route design remains proposed until a permitted test succeeds. Retain its run identifier and
open the result to verify the evidence link and recipient.

## Write the weekly brief

Invoke `pharma-ci-weekly-brief` and paste:

```text
Fictional exercise, inline output. Use these pasted alerts and our capture policy. Separate
source facts, AI summaries, interpretations and proposed actions. For the sensitive HCP project,
keep small edits available for review. For the milestone project, use our agreed material-change
rule. Name the reviewer and next action; preserve unresolved questions and the evidence links.
```

## Maintain coverage

Before the first run, agree who checks failed captures, expired sign-ins, moved URLs and newly
published pages. Record the last review and next planned source check. Compare the captured view
with the intended page area, query and pagination. Document how new pages are discovered and
approved for monitoring; an importance prompt alone does not crawl a domain or read linked files.
