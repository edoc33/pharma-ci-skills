# Discuss a saved alert and choose the next action

The Pharma CI USA session on September 17, 2026 uses saved source comparisons and guided discussion. No account setup, live build or message sending is required during the session.

Open the [FDA Isembyld fixture](evidence/fixtures/fda-approval.json), [earlier capture](evidence/assets/fda-isembyld-before.jpg) and [highlighted comparison](evidence/assets/fda-isembyld-comparison.jpg). These are saved source evidence. The reviewer, routing and next action below are proposed. A successful Microsoft 365 execution remains unverified.

## Work through the alert

| Question | Expected answer or decision |
|---|---|
| What changed? | The highlighted FDA list adds an Isembyld row. Retain the source link and saved comparison. |
| What do the dates tell us? | The row gives an approval date of 11 September 2026. The saved event records detection at 22:30:54 UTC that day. The page's publication time is unknown. |
| How was the alert classified? | The saved rule asks for new approvals and the event has IMPORTANT=true. Choose every-edit or IMPORTANT-only delivery for your own watch question. The saved flag alone does not establish delivery. |
| Who checks it, and by when? | Choose the asset or therapy-area reviewer and backup. Set the deadline from the decision the team needs to make. The example leaves these assignments proposed. |
| What happens next? | The reviewer opens the FDA detail, checks asset and indication scope, and decides whether the briefing needs an update. Record the source check, remaining questions and next action. |

The listing and saved AI Summary do not establish launch availability, price or positioning. Keep the observed change separate from a proposed implication.

## Map the evidence to a review item

Use [review-item-template.csv](review-item-template.csv) and its [field dictionary](review-item-schema.json). Map detection to `observed_at`, the saved platform value to `saved_important`, and the saved summary to `ai_summary`. Preserve the source URL and evidence-file reference. Keep the approval date separate from detection. Leave unavailable publication and capture dates empty or null, as the output format requires.

Use the local fixture ID for the offline exercise. A real email route supplies its own trigger message ID. Keep `owner`, `backup_owner`, `destination`, `due_at` and `action` proposed until the team chooses them. Record execution only after a verified run.

Finish by completing this sentence:

> We will watch ___ for ___, have ___ review it by ___, and use the checked result to ___.

Then name the backup reviewer and the person who checks failed monitors, changed URLs and new pages.

## Try the workflow after the session

Start with [first-run.md](first-run.md) and a spreadsheet or an approved AI tool. The manual exercise needs no monitoring subscription, API key or Microsoft 365 connection.

For an automated route, follow [m365-workflow.md](m365-workflow.md) in an authorized test environment. Test a relevant event, a repeat and an item with missing evidence. Verify the queue item and reviewer access. Add notifications after the queue works, and test notification failures separately.

Record the run ID, queue-item URL and checked result in [saved-event-manifest.json](saved-event-manifest.json) only after observing the run. The bundled source comparisons establish the page changes; the manifest keeps workflow execution status separate.
