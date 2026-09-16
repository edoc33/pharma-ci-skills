# First run: a fictional weekly brief

Every company, product, person, job id and URL below is fictional. The `.example` domains do not
resolve and the workspace and job ids are placeholders. Use this run to learn the shape of the
brief, then replace the details with your own.

## Exercise policy

This fictional exercise selects `delivery_policy: important` for its material-change watch.
Sensitive brand/HCP projects can instead select `all`. The saved IMPORTANT value, AI Summary and
reviewer decision remain separate. Use `--delivery important` on illustrated creation previews
unless a per-row policy is present. Keep `--confirm` absent until the user explicitly confirms.
The maintenance owner is `unassigned`; the source recheck must cover failed captures, moved/new
pages and search pagination. Abbreviated tables below omit these repeated fields.

## The prompt

```text
Use pharma-ci-weekly-brief. This is a fictional practice run; do not call the API or browse.
Period: Monday 2026-09-07 to Sunday 2026-09-13, America/New_York. Audience: Tessaline Bio
dermatology launch team, internal only. Decision register: (1) field-force training start,
stakeholder field-force lead, timeframe before 2026-12-15; (2) payer objection guide update,
stakeholder parnetide asset lead, timeframe before the next field cycle briefing on 2026-10-20.
Use the pasted feed below as the week's changes and write the brief under ./pharma-ci-demo/.
```

## Fictional important-only feed (the policy selected for this exercise)

```text
2026-09-09 06:14  important job 987001  Norvane careers search AD US (fic
    Two new postings appeared: "Dermatology Sales Specialist, Northeast" and "Medical Science Liaison, Immunology, West", both dated 2026-09-08. No postings were removed.
2026-09-10 06:16  important job 987004  Norvane newsroom (fictional)
    A release dated 2026-09-10 announces a co-promotion agreement with Quillbrook Pharmaceuticals for vestrolimab in the US dermatology market.
2026-09-11 07:02  important job 987011  Harrowgate policy search vestrol
    A revised policy dated 2026-09-09 adds a step-therapy requirement: documented trial of one topical calcineurin inhibitor before vestrolimab.
2026-09-12 06:15  important job 987002  Norvane pipeline (fictional)
    Layout changed from a table to cards. Phase 1: 3 to 3. Phase 2: 4 to 4. Phase 3: 2 to 2. Filed: 0 to 0. No program was added, removed or moved.
```

Regular (not important) changes in the same week: 11, all layout or date-stamp changes, kept in
the archive and counted in the coverage line.

## Verification notes

| item_id | Verified | Publication date (from page) | Detection time (capture) | Note |
|---|---|---|---|---|
| 2026-09-13-01 | yes | 2026-09-08 | 2026-09-09 06:14 | Both postings present on the careers site; locations confirmed |
| 2026-09-13-02 | yes | 2026-09-10 | 2026-09-10 06:16 | Release present; agreement text names US dermatology field co-promotion |
| 2026-09-13-03 | yes | unknown; effective 2026-09-09 | 2026-09-11 07:02 | Policy PDF opened; step-therapy paragraph present |
| 2026-09-13-04 | yes | none printed | 2026-09-12 06:15 | Pipeline page redesigned; counts unchanged; individual programs compared in this fictional verification |

In this fictional verification, individual programs were also compared. Item 04 is flagged
important but carries no verified program change; it goes to the appendix as a rule
note, and the open questions ask whether the pipeline rule needs a tighter ignore clause.

## The brief (`./pharma-ci-demo/weekly-brief-2026-09-13.md`, abridged)

```markdown
# Weekly intelligence brief, 2026-09-07 to 2026-09-13 (America/New_York)

Audience: Tessaline Bio dermatology launch team. Handling: internal only. Draft for approval.

## Headline

Norvane's US dermatology field build-up now has two public signals in one week, a co-promotion
agreement and field hiring, which bear on when field-force training starts.

## What changed, ranked

1. Fact: a Norvane release dated 2026-09-10 announces a US dermatology co-promotion agreement
   with Quillbrook Pharmaceuticals for vestrolimab (https://norvane.example/news).
   Reading: a co-promotion partner may shorten the time Norvane needs to field a full sales
   force; the size of the Quillbrook dermatology team, if disclosed, would test this.
   Decision: field-force training start. Stakeholder: field-force lead. Timeframe: before
   2026-12-15. Published 2026-09-10; detected 2026-09-10 06:16. Verified. Item 2026-09-13-02.

2. Fact: two postings dated 2026-09-08 appeared on Norvane's US careers search for atopic
   dermatitis, a Northeast dermatology sales specialist and a West immunology MSL
   (https://careers.norvane.example/search?q=atopic%20dermatitis&country=US).
   Reading: field and MSL hiring may precede a launch; the posting count over the next four
   weeks would test this. Decision: field-force training start. Stakeholder: field-force lead.
   Timeframe: before 2026-12-15. Published 2026-09-08; detected 2026-09-09 06:14. Verified.
   Item 2026-09-13-01.

3. Fact: Harrowgate Health Plan's policy for vestrolimab, effective 2026-09-09, adds a
   step-therapy requirement of one topical calcineurin inhibitor
   (https://www.harrowgatehealth.example/providers/policies?search=vestrolimab).
   Reading: the step may narrow vestrolimab's first-line position with this payer; the parnetide
   policy at the same payer would show whether the step is class-wide. Decision: payer objection
   guide update. Stakeholder: parnetide asset lead. Timeframe: before 2026-10-20. Effective
   2026-09-09; publication date unknown; detected 2026-09-11 07:02. Verified. Item 2026-09-13-03.

## Carried over

None. This is the first brief in the series.

## Research updates (appendix)

- Fact: Norvane's pipeline page was redesigned from a table to cards; candidate counts by phase
  are unchanged (Phase 1: 3, Phase 2: 4, Phase 3: 2, Filed: 0). Reading: none; this is a layout
  change. Detected 2026-09-12 06:15; no publication date printed. Item 2026-09-13-04.

## Open questions and next checks

- Does the Quillbrook agreement disclose field size or start date? Check the release and the next
  Norvane investor presentation. Owner: CI lead. By 2026-09-20.
- Does the Harrowgate parnetide policy carry the same step? Check the parnetide policy page.
  Owner: parnetide asset lead. By 2026-09-18.
- Should the pipeline rule add "ignore a change from table to card layout"? Owner: CI lead. By
  the next rule review.

## Coverage and method

Monitors in scope: 10. Changes seen: 4 important, 11 regular. Items verified: 4. Unverified: 0.
Period: 2026-09-07 to 2026-09-13. Detection times are monitor capture times; publication times
are read from the source page. Current-awareness record; not a validated system.
```

## The review-items CSV (`./pharma-ci-demo/review-items-2026-09-13.csv`, two rows shown)

```text
item_id,source_url,source_identifier,source_event_date,source_publication_date,before_capture_date,after_capture_date,retrieved_at,evidence_reference,changed_field,old_value,new_value,team_rule,important,needs_review,owner,backup_owner,destination,due_at,review_status,reviewed_by,reviewed_at,action
2026-09-13-02,https://norvane.example/news,release 2026-09-10,2026-09-10,2026-09-10,2026-09-09 06:16,2026-09-10 06:16,2026-09-14 09:30,weekly-brief-2026-09-13.md item 1,release list,no co-promotion release,co-promotion agreement with Quillbrook (fictional),newsroom rule,true,true,CI lead,unassigned,field-force lead,2026-12-15,drafted,,,
2026-09-13-03,https://www.harrowgatehealth.example/providers/policies?search=vestrolimab,policy effective 2026-09-09,2026-09-09,unknown,2026-09-10 07:02,2026-09-11 07:02,2026-09-14 09:40,weekly-brief-2026-09-13.md item 3,step therapy,none,one topical calcineurin inhibitor trial required,payer rule,true,true,parnetide asset lead,unassigned,parnetide asset lead,2026-10-20,drafted,,,
```

## What the run returns

Headline as above; 3 main items, 1 appendix item, 0 unverified, 0 carried over; 3 open questions;
two file paths. The brief is a draft until the CI lead approves it; the skill does not send it.
