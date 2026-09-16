# Source-link checks

Checked September 12, 2026. Direct GET requests returned HTTP 200 for 20 of the 21 URLs. Lilly timed out in that path, then opened with the web reader. These results establish limited reachability. They do not prove that a page monitor can load the required content, capture the chosen region, or detect the intended changes.

ClinicalTrials.gov and CTIS returned application shells. The FDA calendar returned JSON in the tested request path. ASCO redirected to search. NICE and NCCN behaved differently across fetch methods. None of these is evidence that the URL is dead. Use the presenter browser and monitor preview for the final test.

Recheck selected sources before enabling them and on the session morning. Test content, pagination, authentication, and output before enabling a monitor.

| Row | Source | Request result | Follow-up |
|---|---|---|---|
| 1 | [New Phase 3 obesity studies (ClinicalTrials.gov)](https://clinicaltrials.gov/search?cond=Obesity&aggFilters=phase%3A3&sort=StudyFirstPostDate&limit=100) | 200 | App shell in direct GET; test loaded results, sort, and pagination in browser. Search discovers records; add relevant record URLs separately. |
| 2 | [Trial record example (replace with your NCT)](https://clinicaltrials.gov/study/NCT07311850) | 200 | App shell in direct GET; indexed record identified VESPER-4. Replace the NCT and check the current live record. No historical comparison was verified. |
| 3 | [Pfizer pipeline](https://www.pfizer.com/science/drug-product-pipeline) | 200 | HTTP response only; browser and monitor preview still required. |
| 4 | [Novartis pipeline p1](https://www.novartis.com/research-development/novartis-pipeline?page=0) | 200 | Test that page 0 loads its own results and the intended region is captured. |
| 5 | [Novartis pipeline p2](https://www.novartis.com/research-development/novartis-pipeline?page=1) | 200 | Test that page 1 has different results and is captured separately; prompt is complete in this row. |
| 6 | [CTIS trial record (example)](https://euclinicaltrials.eu/ctis-public/view/2025-523657-34-00) | 200 | App shell in direct GET; test the specific record in browser. Public visibility varies by field and document. |
| 7 | [FDA novel drug approvals 2026](https://www.fda.gov/drugs/novel-drug-approvals-fda/novel-drug-approvals-2026) | 200 | HTTP response only; browser and monitor preview still required. |
| 8 | [FDA advisory committee calendar](https://www.fda.gov/advisory-committees/advisory-committee-calendar) | 200 | HTTP 200 returned application/json in this request path. Confirm the meeting list and individual notice in the stage browser. |
| 9 | [FDA warning letters](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters) | 200 | HTTP response only; browser and monitor preview still required. |
| 10 | [EMA news / CHMP outcomes](https://www.ema.europa.eu/en/news) | 200 | HTTP response only; browser and monitor preview still required. |
| 11 | [FDA OPDP untitled letters](https://www.fda.gov/drugs/warning-letters-and-notice-violation-letters-pharmaceutical-companies/untitled-letters) | 200 | HTTP response only; browser and monitor preview still required. |
| 12 | [ASCO abstracts & presentations](https://meetings.asco.org/abstracts-presentations) | 200 | Redirected to ASCO search. Test the selected congress/year/topic view and what is publicly accessible. |
| 13 | [ESMO Congress 2026 programme](https://www.esmo.org/meeting-calendar/esmo-congress-2026/programme) | 200 | Verify the loaded programme and any linked abstract surface; the page shell alone is insufficient. |
| 14 | [AACR Annual Meeting 2027](https://www.aacr.org/meeting/aacr-annual-meeting-2027/) | 200 | HTTP response only; browser and monitor preview still required. |
| 15 | [NICE appraisal example (replace with your GID)](https://www.nice.org.uk/guidance/indevelopment/gid-ta11221) | 200 | Direct GET loaded the project title; web reader returned 403. Confirm the live project status and documents in browser. |
| 16 | [CDA-AMC reimbursement reviews](https://www.cda-amc.ca/reimbursement-review-reports) | 200 | HTTP response only; browser and monitor preview still required. |
| 17 | [G-BA §35a benefit assessments](https://www.g-ba.de/themen/arzneimittel/arzneimittel-richtlinie-anlagen/nutzenbewertung-35a/) | 200 | HTTP response only; browser and monitor preview still required. |
| 18 | [ICER assessments](https://icer.org/explore-our-research/assessments/) | 200 | HTTP response only; browser and monitor preview still required. |
| 19 | [NCCN guideline updates](https://www.nccn.org/updates) | 200 | Direct GET loaded the page title; web reader failed. Test access and the actual guideline update content in browser. |
| 20 | [Pfizer press releases](https://www.pfizer.com/newsroom/press-releases) | 200 | HTTP response only; browser and monitor preview still required. |
| 21 | [Lilly webcasts & presentations](https://investor.lilly.com/webcasts-and-presentations) | Timeout | Direct GET timed out; web reader retrieved the current event listing. Retry in the presenter browser. A timeout does not establish a dead link. |

Machine-readable timestamps, redirects, and response metadata are in `link-checks.json`. No full-page historical captures were created by this check.


## September 16 additions

Pfizer homepage and CVS Health services were readable through a primary-source web request on September 16. Both still require a monitor preview. These additions do not change the dated September 12 check results above. The current directory has 22 source entries across 23 URLs.


## September 16 full-directory reachability check

A fresh GET check reached 19 of 23 URLs with HTTP 200. AACR returned 406; CDA-AMC and ICER returned 403; Lilly timed out. These responses can reflect request-path restrictions and do not by themselves establish dead links. See `link-checks-2026-09-16.json` for timestamps and final URLs. Browser access and capture-preview suitability still need checking before enabling each source.

A separate primary-source web reader loaded AACR, ICER and Lilly on September 16. CDA-AMC still returned 403 and remains pending a browser/capture-preview check. These follow-ups do not establish monitor suitability.
