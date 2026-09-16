# Route a source alert to an owned review queue

This recipe uses a shared Outlook mailbox, Power Automate, and a SharePoint list. Teams is an optional notification step. It is a workshop configuration guide; it has not been deployed or run in your tenant.

The first version preserves the incoming message and gives it an owner. The reviewer then checks the linked source and completes the evidence fields. Add AI extraction only after testing the exact alert format and an AI connection approved by your organization.

```text
Source alert email → Shared mailbox → Power Automate → SharePoint review item
                                                          ↓
                                                    Assigned reviewer
                                                          ↓
                                               Decision + evidence archive
```

## Prepare the tenant before building

Use an authorized M365 user connection with access to the shared mailbox, a test SharePoint site, and the chosen team. Confirm the environment's license entitlements, connector policy, and conditional-access rules with its owner. Add a backup flow owner and document whose connections it uses. Ownership of a flow and ownership of its connections are separate concerns. [Microsoft flow ownership](https://learn.microsoft.com/en-us/power-automate/create-team-flows)

Create a list named `CI review queue` in the test site. For the first build, add these columns using the exact internal names below. Add the remaining evidence fields from the schema when the route works.

| Column | Type | Initial mapping |
|---|---|---|
| Title | Existing text field | Email subject |
| MessageKey | Single line of text, unique values enabled | Incoming message identifier |
| ReceivedAt | Date and time | Mailbox received timestamp |
| SourceURL | Hyperlink | Reviewer adds the primary-source URL |
| EvidenceText | Multiple lines of plain text | Incoming body retained as raw text, which may include HTML markup; keep the original email in the mailbox |
| ReviewOwner | Person, single value | Chosen reviewer, supplied as a fixed person for this first route |
| ReviewStatus | Choice: Unreviewed, Reviewed, Needs source, No action | Unreviewed |
| DueAt | Date and time | Optional; apply the team's reviewed deadline rule |

Use `ReceivedAt` for mail arrival. The source event, publication, and capture dates stay in separate fields. A mail timestamp cannot substitute for any of them. SharePoint's list connector supports item creation and retrieval. [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepointonline/)

## Configure the flow

1. Create an automated cloud flow. Choose Office 365 Outlook's **When a new email arrives in a shared mailbox (V2)** trigger. Select the authorized shared mailbox and the folder that actually receives the alerts. For an individual mailbox, use the V3 new-mail trigger instead. Leave attachment content disabled for this first route. Use a known sender and optional subject filter to narrow the source. Keep the Outlook email-importance filter at Any. A sender's high/normal email priority is different from an AI relevance flag. [Outlook connector](https://learn.microsoft.com/en-us/connectors/office365/)
2. Add SharePoint's **Get items** action for the same site and list. In Filter Query, set `MessageKey eq '<incoming message identifier>'`, inserting the trigger's message identifier with dynamic content. Set Top Count to 1. Preserve the identifier exactly; validate its length against the list field and escape any single quote in an OData value before use. In the trigger settings, enable concurrency control with degree 1 during the pilot, and keep the list's uniqueness check. If the same event arrives through several routes, a source-event identifier is a better later deduplication key than an email ID.
3. If the lookup finds no item, add **Create item** and map the fields above. If it finds one, end the duplicate path. A failed creation must remain visible in run history; do not label every creation failure a duplicate.
4. For the first run, stop at the queue. The reviewer opens the email, follows the primary-source link, and records the exact changed field, old and new values, source date, capture date, decision, and next action. Keep unreadable messages in `Needs source`.
5. Optional: after successful item creation, add Teams' **Post message in a chat or channel** action. Select the actual test team and channel. Send the subject, reviewer, and link to the review item. Keep source text in the evidence record so long messages and private interpretations do not spread through chat. The tenant must allow the Teams Workflows app. Use a sender option supported by that tenant. [Teams connector](https://learn.microsoft.com/en-us/connectors/teams/)

Use the current Teams action through Power Automate. Legacy Office 365 Connectors in Teams were retired in May 2026. This recipe does not use their Incoming Webhook setup. [Microsoft retirement notice](https://devblogs.microsoft.com/microsoft365dev/retirement-of-office-365-connectors-within-microsoft-teams/)

## Test the route before enabling it

With the tenant owner's authorization, send a new, clearly labeled test email to the test mailbox. Record the flow run ID, resulting list-item URL, and the reviewer who checked it. Replaying an old email by moving it between folders is not a dependable test of a new-mail trigger. Microsoft documents missed-message, protected-message, and duplicate-trigger limits. Reconcile the pilot mailbox against the queue before relying on it. [Outlook trigger behavior](https://learn.microsoft.com/en-us/connectors/office365/)

Test one repeat message, one irrelevant message, and one message without readable evidence. Verify that duplicates are visible but create no second review item, that routine changes remain retrievable, and that missing evidence stays in the review queue. Confirm the source link works for the reviewer.

If the Teams action fails after the list item exists, retain that item and inspect the failed step. Retry the notification without creating another item. Test connection expiry, owner absence, and failure handling before expanding beyond the pilot.

## Apply the project policy and maintain the route

Every event has a saved IMPORTANT flag and AI Summary. Preserve every captured edit for sensitive
projects, or apply an explicitly chosen important-only notification policy. Unknown importance
stays visible for review. A classification, configured route or generated report does not prove
receipt, review or action. Keep source facts, AI summaries and proposed classifications separate.

Name the reviewer, backup, flow/connection owner and source-maintenance owner. The maintenance
owner checks failed captures, changed URLs, new pages, expired access and pagination. A new-page
process is separate from the importance rule. Record the last check and next recheck date.

The current workshop uses a saved FDA input for the proposed build. Read the
[starter-pack workflow](../../../docs/starter-pack/m365-workflow.md) for its event mapping and
fallback. This recipe establishes no completed flow in the attendee's tenant.

## Add AI after the routing test

Use `triage-prompt.txt` with the preserved source evidence. Its result is a proposed classification. It keeps a separate `needs_review` value so an uncertain summary remains visible. For automatic extraction, map a documented input schema and validate it against representative messages. Leave fields empty when the alert lacks a date or earlier version.

For a weekly digest, select reviewed items for the period and group them by asset or therapy area. Include source links and open actions. A calendar schedule can prepare a draft for the reviewer. Automatic distribution needs the team's agreed recipients and approval rule.
