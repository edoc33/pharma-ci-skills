# Saved public-page alert examples

Use [FDA Isembyld](fixtures/fda-approval.json) as the primary workshop input. Four supporting examples cover guidance discovery, clinical site changes, campaign copy and a provider availability announcement. These are recorded public-page changes from presenter-owned monitors. Publisher names identify the monitored public sources; this package makes no customer-adoption claim.

## Included examples

| Public source | Recorded event, UTC | Evidence |
|---|---|---|
| [FDA novel drug approvals](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026) | `2026-09-11T22:30:54.000Z` | [Fixture](fixtures/fda-approval.json) |
| [NICE published guidance](https://www.nice.org.uk/guidance/published) | `2026-09-09T17:55:11.000Z` | [Fixture](fixtures/nice-guidance.json) |
| [ClinicalTrials.gov study NCT07311850](https://clinicaltrials.gov/study/NCT07311850) | `2026-09-04T18:40:56.000Z` | [Fixture](fixtures/trial-sites.json) |
| [Pfizer homepage](https://www.pfizer.com/) | `2026-09-09T12:10:54.000Z` | [Fixture](fixtures/pfizer-campaign.json) |
| [CVS Health services](https://www.cvshealth.com/services) | `2026-09-04T17:57:25.000Z` | [Fixture](fixtures/cvs-announcement.json) |

The assets are existing crops copied unchanged from the completed workshop deck evidence. Original Visualping highlights are preserved. The FDA example includes an authentic earlier capture. The other examples include a comparison crop only. No before image has been reconstructed.

## Read the fields correctly

- `observed_at`: the recorded Visualping change-event time. It does not establish when the source first published the content or the monitoring delay.
- `previous_capture_at`: the known earlier capture time, where available. A timestamp can be retained even when its image is outside this compact package.
- `source_dates`: dates displayed in the source, such as an approval, listing or article date. `source_published_at` remains null because a precise publication timestamp was not established.
- `crop_created_at` in the manifest: the later screenshot/crop preparation time where verified. It is separate from the source capture and event time; null means the crop preparation timestamp was not verified.
- `saved_alert`: the saved IMPORTANT flag, AI Summary and rule, reproduced verbatim where verified. FDA, NICE and the trial example retain these fields. A reproduced summary remains an AI interpretation that requires a source check.
- For Pfizer and CVS, `saved_alert` fields are null because the fields were not verified for inclusion in this package. Visualping change events have both a binary IMPORTANT flag and an AI Summary; these nulls describe the evidence export, not product behavior.
- `verified_observation`: the narrow observation supported by the bundled visual. Read `limitations` beside the saved summary.
- `proposed_review`: owner, backup, next action and decision placeholders. They are proposed workshop steps. The fixtures do not establish a completed reviewer action, delivered message or executed Microsoft 365 flow.

[fixture.schema.json](fixture.schema.json) defines this package's teaching format. It is a sanitized fixture format, separate from the Visualping API/webhook contract. Asset paths in fixtures resolve relative to each fixture file; paths in [manifest.json](manifest.json) resolve relative to this directory.

## Evidence limits to keep in the exercise

**NICE:** TA1190 and TA1191 appear in the visible first page. The saved summary's wording about older entries being removed does not establish withdrawn guidance. Open each appraisal before interpreting its recommendation, population or access implications. The monitored listing does not itself supply the linked document's full contents.

**Clinical trial:** the crop visibly shows 169 locations. The earlier count of 171 and specific site edits come from the saved AI Summary. The stored IMPORTANT=false reflects a rule about other trial fields. A country-site watch may need a different rule. Preserve all captured changes when the review mandate requires them; importance classification and human review are separate steps.

**Commercial:** separate before captures were unavailable for Pfizer and CVS. Pfizer shows highlighted vaccination campaign copy. CVS shows an announcement dated 3 September. Neither establishes exact prior copy, first publication time, local stock or business outcomes.

**FDA:** the captured approval date and full indication remain in the source crop and saved summary. The source row alone does not establish launch availability, price or positioning. Verify the underlying source before preparing a current briefing.

## Provenance and hashes

Prepared 16 September 2026 from the saved event evidence and final deck review. No new source captures were taken for this package. No private account, workspace, monitor or process identifiers, private API responses, delivery metadata or credentials are included.

Each asset below was checked against its existing source file byte-for-byte. The manifest also records fixture hashes, original capture-asset hashes, source URLs and known crop-preparation timestamps. Hashes establish file identity; they do not independently validate the source claims.

| File | SHA-256 |
|---|---|
| `assets/fda-isembyld-comparison.jpg` | `00d93d5005d83e0154f621bcfc57ea8abc078fdce219f448281eef87bccc16d3` |
| `assets/fda-isembyld-before.jpg` | `038de196c6f8abe196d3c38841b4ac73b318e7fd6d9c1bd20d0becb5d38e8529` |
| `assets/nice-guidance-comparison.jpg` | `6777a1b89f853f4e7177e91e1058c88074a3338f2946a041744c9f9e223aba09` |
| `assets/trial-sites-comparison.jpg` | `021798ce980909aa399ee912c288216215e8830e8836153c11dc1f80d797d0ad` |
| `assets/pfizer-campaign-comparison.jpg` | `7c2f9e93ef8ac9a45189c77eece2abb1571ec4c13eae96918f74fed61dd241da` |
| `assets/cvs-announcement-comparison.jpg` | `cc6be8d9a8d0a4d966ee5fb2746b116e7b922ae9698b2eda9ededf7d8df36e79` |
