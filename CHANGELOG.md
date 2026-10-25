# Changelog

All notable changes to the generated public distribution are recorded here.

## [0.3.0-rc.1] - candidate

### Added

- Deterministic export provenance through `PUBLIC-MANIFEST.json` and
  `PUBLIC-EXPORT-REPORT.json`.
- Independently executable public integrity verifier and GitHub Actions
  workflow.
- Public English and Czech navigation, adoption, security, and maintenance
  documentation.

### Changed

- `public_rail` implementation, resources, templates, and regression tests
  are copied byte-identically from one recorded internal source commit.

### Licensing and release boundary

- The classified public subset is distributed under MIT under the explicit
  scoped exception in `LICENSES/PUBLIC-SUBSET-MIT.md`.
- This remains a candidate only. Publication requires separate human approval
  of the exact source commit and disclosure review; it is never implied by a
  passing export or test suite.
