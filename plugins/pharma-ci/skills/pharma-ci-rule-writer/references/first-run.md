# First run: "tell me when a competitor's trial slips"

Everything below is invented for practice. Companies, drugs, people, domains and identifiers are
fictional; `NCT00000000` is a placeholder. No real monitor, alert or account is described.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt

```text
Use pharma-ci-rule-writer. This is a fictional practice run; do not create monitors.
Question: tell me when Corrimel Bio's tavrelimab Phase 3 trial in IgA nephropathy slips.
Page: https://clinicaltrials.gov/study/NCT00000000 (registry record).
Threshold: a completion-date move of more than 90 days matters; smaller moves do not.
Countries that matter: US and Germany.
Decision served: decide whether to move the orvasertib readout communication earlier.
Owner: ri.lead@halvane.example. Backup: ci.analyst@halvane.example.
```

## Step results

**Classify.** Job: trial and pipeline. Page type: registry record (ClinicalTrials.gov). One page
type, one rule. A second question hidden in "slips" is whether new sites open in Germany; that is
the same page type, so it stays in this rule as a conditional ignore.

**Fields.** Overall status, primary completion date, study completion date, enrollment target,
number of arms, primary endpoint. Rejected: "any material change to the trial".

**Thresholds.** Primary and study completion dates: more than 90 days, from the user. Enrollment
target: the user gave none, so the rule reports any change and asks for old and new values rather
than inventing a percentage.

**Ignores.** Version labels, last-update dates, record-verification dates, layout, and site-list
edits unless a site is added or removed in the US or Germany.

**Values back.** Old and new value for every changed field; the date shown on the record.

## `./pharma-ci/rules/corrimel-nct00000000-record.rule.txt`

```text
Alert me when the overall status, the primary completion date or study completion date (by more
than 90 days), the number of arms, the enrollment target, or a primary endpoint changes on this
record. State the old and new value for each changed field and the last-update date shown on the
record. Ignore version labels, last-update dates on their own, record-verification dates, layout,
and site-list edits unless a site is added or removed in the US or Germany.
```

## `./pharma-ci/rules/corrimel-nct00000000-record.summalyzer.json`

```json
{
  "importantDefinitionType": "custom",
  "importantDefinition": "Alert me when the overall status, the primary completion date or study completion date (by more than 90 days), the number of arms, the enrollment target, or a primary endpoint changes on this record. State the old and new value for each changed field and the last-update date shown on the record. Ignore version labels, last-update dates on their own, record-verification dates, layout, and site-list edits unless a site is added or removed in the US or Germany."
}
```

The user also asked for the dry-run command. The skill printed it without `--confirm`:

```text
python3 scripts/vp_client.py create --workspace 12345 --delivery important \
  --url https://clinicaltrials.gov/study/NCT00000000 \
  --title "Corrimel tavrelimab Phase 3 record (IgAN)" \
  --rule "$(cat ./pharma-ci/rules/corrimel-nct00000000-record.rule.txt)"
```

The script printed the job body with `"interval": "1440"` and the line "Dry run. Re-run with
--confirm to create this monitor." The skill stopped there because the user had not typed `confirm`.

## `./pharma-ci/rules/corrimel-nct00000000-record.checklist.md` (abridged)

| Check | Result |
|---|---|
| Names a specific field | yes |
| No "important", "significant", "major" or "relevant" as the test | yes |
| Threshold on every drifting number | partial: enrollment target has none; owner chose to see any change and values |
| Ignore clause names known noise | yes |
| Asks for values back | yes |
| One page type | yes |
| No literal bracket | yes |
| No inference of reason, intent, efficacy or safety | yes |
| Does not depend on minutes-level detection | yes |
| Reviewer can decide from the summary alone | yes |

Owner `ri.lead@halvane.example`, backup `ci.analyst@halvane.example`. Decision served: move the
orvasertib readout communication earlier or not.

## `./pharma-ci/rules/rule-scorecard.csv`

```csv
slug,url,page_type,rule_version,owner,backup,start_date,score_by,total_alerts,useful_alerts,ratio,next_edit
corrimel-nct00000000-record,https://clinicaltrials.gov/study/NCT00000000,registry record,1,ri.lead@halvane.example,ci.analyst@halvane.example,2026-09-15,2026-10-15,,,,
```

## The 30-day step, as it played out in the fiction

On 2026-10-15 the owner ran `python3 scripts/vp_client.py changes --job 987654 --workspace 12345
--since 2026-09-15` and counted the entries with `analyzerAlertTriggered` true. Four alerts had
fired. Two reported a changed "study record verification" date only, which the owner judged not
useful. One reported a new site in Munich, useful. One reported the primary completion date moving
from 2027-06 to 2027-11, useful and the reason the decision meeting was called.

Score: 2 useful / 4 total. Edit the rule, not the page: the verification-date wording was already
an ignore, so the owner tightened it to "ignore any change whose only effect is a date in the
record's version, verification or last-update fields". Version 2, `start_date` 2026-10-15,
`score_by` 2026-11-14, appended as a new scorecard row.

## What this run did not establish

Nothing about the real record at any NCT number. The completion-date move is a source fact in the
fiction; whether it means a slip in the competitor's plan is a hypothesis the owner tests against
the sponsor's next filing or newsroom item, not a conclusion the rule can reach.
