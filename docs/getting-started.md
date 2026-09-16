# First runs

Install using the [repository README](../README.md). Every example below is fictional and works
without live tools. Paste the prompt after invoking the named skill. Ask for inline output on your
first run; when you want files, the skills write to `./pharma-ci/` in your working directory.

Claude Code names skills `/pharma-ci:pharma-ci-watchlist`; Codex names them `$pharma-ci-watchlist`.
Each installed skill carries its own `references/first-run.md` with a longer worked example.

## Connect the API (optional)

1. Create a key at https://visualping.io/account/developer (any plan).
2. `export VISUALPING_API_KEY=...` in the shell you run Claude Code or Codex from.
3. `python3 scripts/vp_client.py whoami` prints your workspaces. Note the id you will use.

Nothing is created until you run `create` or `bulk` with `--confirm`, and the skills ask you to type
`confirm` before adding that flag.

## Update an existing installation

Claude Code, user scope:

```sh
claude plugin marketplace update pharma-ci
claude plugin update pharma-ci@pharma-ci
claude plugin list
```

Check that the listed version is `0.1.0`, then run `/reload-plugins` or start a new session. For
project or local scope add `--scope project` or `--scope local` and run from that project.

Codex: pull the latest `main`, move your existing `pharma-ci-*` skill folders out of the destination
(the installer refuses collisions and does not merge edits), rerun the two installer commands, then
restart Codex.

## Build a watchlist

```text
Fictional exercise, inline output, no browsing. We are launching in [indication] in 2027 against
two competitors, Northwind Therapeutics and Contoso Bio. Decisions this quarter: the launch
sequence and the field-force size. Propose the minimum watchlist across the five jobs and the eight
under-watched sources, name the decision each row serves, and leave owners unassigned.
```

Expect one row per page with a rule, a cadence, a recheck-by date and the decision it serves, as a
two-column import CSV and a prompt guide.

## Write a rule

```text
Fictional exercise, inline output. Page type: competitor pipeline page. I want to know when a
program is added, removed or moves phase, and I do not want layout changes. Ask for the candidate
counts by phase back so a no-change is confirmed in one line.
```

## Route an alert

```text
Fictional exercise, inline output. Alert: a regulator's published-guidance list added an appraisal
for a competitor product on 9 September, detected the same day at 17:55 UTC. Our UK access lead
owns the asset. Draft the review item and the Microsoft 365 route; leave the backup owner
unassigned.
```

## Write the weekly brief

```text
Fictional exercise, inline output. Here are this week's alerts (pasted). Keep only what the rule
flagged important, connect each to a named decision, stakeholder and timeframe, and put everything
else in a research-updates appendix.
```
