# Write a rule for the captured input

Every Visualping change event has a binary IMPORTANT flag and an AI Summary. A custom rule uses
`summalyzer.importantDefinition` with `importantDefinitionType: "custom"` to describe which
captured changes matter. The flag is a classification. Delivery and human review are separate.

## Choose capture and delivery policy first

- **Every captured edit (`all`):** preserve detected changes for analyst review. Sensitive brand/HCP
  projects may need a single word, punctuation mark or small-image edit. Avoid blanket image,
  text or layout exclusions for these projects.
- **IMPORTANT-only (`important`):** filter notifications using a defined material-change rule.
  Sample unflagged events and owner-reported misses when assessing the rule.

Specify captured page area and content as well as delivery. Every-captured-edit delivery concerns
detected events; it does not promise every change anywhere on a site. Inspect settings before
creation and verify them after setup. The helper requires `--delivery all|important` on `create`;
`bulk` takes that option or a per-row `delivery_policy` column. A preview with an unconfirmed policy
is not ready for `--confirm`.

## Write the rule

1. Name fields visible in the captured input that answer the watch question.
2. Ask the owner to choose any needed threshold. A completion-date threshold is a project decision,
   not a universal 90-day rule. Leave unresolved thresholds incomplete.
3. Exclude only content agreed to be irrelevant. Site removals matter to a country-site watch;
   punctuation and images may matter to a claim review.
4. Request old/new values and identifiers. Equal aggregate counts do not establish that the same
   candidates or records remain in the set.
5. Scope each rule to one page/document type. A list link does not supply the document's contents;
   retrieve or monitor it separately.
6. Replace all bracketed variables before live setup. Keep unknowns explicit in drafts.

## Six workshop rule families

Starting rules must match fields actually present in the captured view.

| Input | Starting rule |
|---|---|
| Trial record | Alert me when status, dates, eligibility, arms, endpoints or results disclosures change. State changed fields and old/new values. Include sites when the country-site question requires them. |
| Pipeline page | Alert me when a program is added, removed, changes phase or changes status. Identify the program and old/new value. |
| Brand/provider page | Alert me when product claims, wording, imagery, price, availability or prominence change. Retain the edit's context. |
| Congress program | Alert me when a session for [scope] is added or its time changes. Give its identifier, title and posted time with time zone when shown. |
| Guideline/access page | Alert me when this guideline's version or [drug] coverage criteria change. Name the version, policy stage or changed criterion visible in the input. |
| Regulatory approval list | Alert me when [drug] is added to this approval list. Give name, ingredient, approval date and indication when shown. |

## Other page-specific rules

| Input | Starting rule |
|---|---|
| Registry search | Alert me when a new study appears in captured results for [scope]. Give identifier and title. Check search coverage separately. |
| Careers search | Alert me when a posting for [function] in [country] is added or removed. State title and location. |
| Leadership page | Alert me when a name is added or removed, or a title changes. |
| SEC filing list | Alert me when a new 8-K, 10-Q or 10-K appears. Name the form and filing date shown. |
| Filing document | Alert me when captured text changes [program] status, risk wording or expected timing. State the exact wording and section. |
| Investor events list | Alert me when a presentation, transcript, webcast or event is posted. Give the visible title, date and link. Assess contents separately. |
| Newsroom list | Alert me when visible release text names [product], [indication] or [topic]. Open the release for its full content. |
| Drugs@FDA record | Alert me when a supplement, label, letter or approval date is added or changed. Open or monitor linked documents for their text changes. |
| Orange Book record | Alert me when a patent or exclusivity entry is added, removed or changes. State identifier and date shown. |
| EMA medicine record | Alert me when authorisation status, indication text or visible document list changes. Read a new document separately. |
| NICE published list | Alert me when an entry for [scope] appears or is marked terminated or withdrawn. Give reference and listed date. |
| HTA decision page | Alert me when a decision, recommendation or status for [drug] is published or changed. State whether draft or final. |
| Payer bulletin/formulary | Alert me when captured [drug] coverage criteria, step therapy, prior authorisation, quantity limits or tier change. |
| TV-ad archive/app listing | Alert me when an ad, campaign or version for [brand] appears, or description or screenshots change. |

## Review classifications and evidence

Record the saved IMPORTANT value separately from reviewer decisions. Preserve unknown flags for
review. Identify the AI Summary as AI-generated and verify its facts against before/after evidence
and the primary source. Keep source-event dates, publication dates and capture times separate.
An approval or last-update date is not automatically a publication timestamp.

Track delivered events, flagged events, reviewed items and useful items as separate counts. Also
inspect unflagged events and owner-reported misses. Revise the capture, rule or route that caused
a failure and retain the reason.

## Cadence and maintenance

Choose cadence for the decision, source behavior, review deadline and check budget. Daily or weekly
is a proposed starting schedule, not an industry-wide practice claim. Use faster feasible checks
when the project needs them. Verify any legal deadline for its jurisdiction, event, rule and
clock-start condition. Congress dates come from that meeting's current timetable.

Record a reviewer, backup and maintenance owner, marking unknown assignments unassigned. Set a
source recheck date. Check failed captures, moved URLs, new pages, filters and pagination. A prompt
alone does not discover every page or repair failed monitoring.
