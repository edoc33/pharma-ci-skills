# First run: one registry alert, one owned route

Everything below is invented for practice. Companies, drugs, people, tenants, domains and
identifiers are fictional; `NCT00000000` and `.example` are placeholders. No real alert, flow or
account is described, and no flow was built or run.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## Prompt

```text
Use pharma-ci-review-route. This is a fictional practice run; do not send mail or build flows.
Alert (pasted from the monitor's change history, detected 2026-09-15 06:12 UTC):
"Primary completion date changed from June 2027 (estimated) to November 2027 (estimated).
Last-update posted date on the record: 2026-09-12. No other fields changed."
Monitor: Corrimel tavrelimab Phase 3 record (IgAN), https://clinicaltrials.gov/study/NCT00000000.
Rule: alert on status, completion dates by more than 90 days, arms, enrollment, primary endpoint.
Decision served: decide whether to move the orvasertib readout communication earlier.
Owner ri.lead@halvane.example, backup ci.analyst@halvane.example.
Queue: SharePoint site "RI pilot" at halvane.example, list "CI review queue".
Flow owner: ops.flow@halvane.example. No backup flow owner yet.
```

## Step 1 and 2: fact, inference, times

Source fact: the primary completion date field moved from June 2027 (estimated) to November 2027
(estimated), a move of roughly five months, above the 90-day threshold. Inference, kept separate:
"the competitor trial has slipped" is a hypothesis; a sponsor can change an estimated date for
reasons other than enrollment. Times: detected 2026-09-15 06:12 UTC; the record states a
last-update posted date of 2026-09-12; publication and detection differ by three days, and the
item records both.

## `./pharma-ci/review-queue.csv`

```csv
item_id,source_url,source_identifier,source_event_date,source_publication_date,before_capture_date,after_capture_date,retrieved_at,evidence_reference,changed_field,old_value,new_value,team_rule,important,needs_review,owner,backup_owner,destination,due_at,review_status,reviewed_by,reviewed_at,action
RI-2026-0001,https://clinicaltrials.gov/study/NCT00000000,NCT00000000,unknown,2026-09-12,2026-09-14,2026-09-15,2026-09-15T06:40:00Z,monitor change history 2026-09-15 06:12 UTC (fictional),primary completion date,June 2027 (estimated),November 2027 (estimated),"completion date moves by more than 90 days",true,false,ri.lead@halvane.example,ci.analyst@halvane.example,RI pilot / CI review queue,2026-09-17T17:00:00Z,unreviewed,,,"Open the record, confirm the field and the last-update date, check the sponsor newsroom for a stated reason, then decide whether the readout-communication question goes to the 2026-09-22 meeting"
```

`source_event_date` stays `unknown`: the record shows when it was last updated, not when the
sponsor decided. `important` is the platform flag, recorded as a routing decision.

## `./pharma-ci/route-ci-review-queue.md` (abridged)

**Route chosen:** email, per `m365-route.md`. Monitor alerts go to the shared mailbox
`ri-alerts@halvane.example`. Flow "RI alert to CI review queue" uses the trigger "When a new email
arrives in a shared mailbox (V2)" on that mailbox, folder Inbox, sender filter set to the monitor's
sending address once one real alert has been received. "Get items" filters
`MessageKey eq '<message id>'`, top count 1, concurrency 1 during the pilot. "Create item" writes
Title, MessageKey, ReceivedAt, EvidenceText (raw body), ReviewOwner (fixed person for the pilot),
ReviewStatus Unreviewed, DueAt received plus two business days. Teams step deferred until the list
route passes its test.

**Owners:** flow owner `ops.flow@halvane.example`; backup flow owner `owner: unassigned`;
connections owned by `ops.flow@halvane.example`; list owner `ri.lead@halvane.example`; item
reviewer `ri.lead@halvane.example`, backup `ci.analyst@halvane.example`.

The skill said in its reply: "The flow has no backup owner. If ops.flow@halvane.example is absent
when a connection expires, alerts will queue in the mailbox and no item will be created. This is
an unassigned route step."

**Webhook alternative, recorded for later:** set the monitor's webhook to a Power Automate
"When an HTTP request is received" trigger, using
`python3 scripts/vp_client.py create ... --webhook <trigger-url> --delivery important` (dry run first; `--confirm`
only after the user types `confirm`). Send one real alert, copy the payload from the flow's run
history into the "captured payload" section below, generate the schema from that payload, then map
fields. Until then the field map marks webhook sources as `unknown until payload captured`. The
trigger URL is not stored in this file.

**Captured payload:** none yet.

**Test plan (results blank):** one labeled test email; one repeat of the same message; one
unrelated message; one message with an empty body. Expected outcomes: one item created; duplicate
visible in run history with no second item; unrelated message filtered or set to No action; empty
body parked in Needs source. Record run ID, item URL, checker.

## `./pharma-ci/route-ci-review-queue-field-map.csv` (excerpt)

```csv
template_column,source,list_column,filled_by,notes
source_url,alert body link,SourceURL,reviewer,reviewer pastes the primary-source URL in the pilot
after_capture_date,alert detection timestamp,ReceivedAt,flow,mail arrival is not the capture time; reviewer corrects if they differ
source_publication_date,date shown on the record,(add after test),reviewer,never derived from ReceivedAt
changed_field,alert summary,(add after test),reviewer,triage-prompt.txt can propose it once the route works
old_value,alert summary,(add after test),reviewer,keep estimated or actual qualifiers
new_value,alert summary,(add after test),reviewer,keep estimated or actual qualifiers
important,platform flag,(add after test),flow,routing decision only
owner,prompt guide row,ReviewOwner,flow,fixed person in the pilot
backup_owner,prompt guide row,(add after test),reviewer,
review_status,constant,ReviewStatus,flow,Unreviewed
```

## What this run did not establish

No mail was sent and no flow exists. The review item is a plan for one person's next two days,
not a finding about any real trial. The one thing that must change before the pilot starts is the
missing backup flow owner.
