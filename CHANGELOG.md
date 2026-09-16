# Changelog

## 0.1.1 - 2026-09-16

- Restore all nine plugin skills, shared references and examples to the published repository. An unanchored ignore rule had excluded the plugin directory from the earlier commit.
- Align the skills and starter pack with the revised Pharma CI workshop: discovery and record monitoring, six rule families, commercial/provider edits, explicit delivery policy and source-maintenance ownership.
- Add a five-page guide, offline HTML handout, 23 starter URLs, review templates and five authentic saved public-page examples. Keep source observations, saved AI output and proposed actions distinct.
- Add stable release download links for the guide and ZIP, with a starter-pack QR.
- Fix API creation payloads, user identity output, repeated CSV URLs, prevalidation and creation estimates. Require an explicit delivery policy before a live write and preserve minor changes in the unfiltered feed.
- Make standalone Codex installs self-contained, including shared references, examples and starter-pack documents, with working resource paths.
- Add client, installation and packaging regression checks. Twenty repository tests pass; all nine skills are discovered by the installer dry run.

The M365 route remains a configuration recipe. This release does not include a verified tenant execution or recording. Source reachability results and capture-preview requirements are documented in the pack.

## Rebuild the attendee downloads

Install the build-only packages `markdown` and `reportlab`, then run:

```sh
python3 scripts/build_starter_pack.py
```

The tracked Markdown, CSV and evidence files in `docs/starter-pack/` are the content source. The command regenerates the HTML, PDF, API CSV, synchronized skill examples and `dist/pharma-ci-starter-pack.zip`. Review the rendered PDF and local handout before publishing release assets.
