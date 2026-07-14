# Changelog

All notable changes to this public adoption kit are recorded here.

## v0.1.3

### Changed

- Clarified template ownership, contract lifecycle status, and project state as
  separate fields in template schema v0.3.1.
- Made optional specialized contracts explicitly conditional in `PROJECT.md`
  and clarified that this kit does not prescribe a module catalog.
- Rejected symbolic links and Windows junctions during package integrity
  verification.

## v0.1.2

### Changed

- Relicensed the public adoption reference kit from Business Source License
  1.1 to the MIT License.
- Synchronized the fictional example with the v0.3.0 template metadata and
  contract lifecycle.
- Hash-verified repository-control workflow files and pinned their action
  dependencies.
- Made the integrity verifier validate manifest version formats instead of a
  single hard-coded kit version.

## v0.1.1

### Added

- GitHub Actions verification for the public package integrity check.
- A minimum adoption profile, completion criteria, contract lifecycle, and
  minimum safety boundary.
- A descriptive practical license boundary and maintenance policy.

### Changed

- Public manifests now distinguish hashed distribution files from repository
  control paths.
- Template metadata now identifies the v0.3.0 template schema separately from
  the kit version.
- `PROJECT.md` is a top-level index; specialized contracts are canonical for
  their respective topics.

## v0.1.0

- Initial public adoption reference kit.
