# Maintenance Policy

This repository is a small adoption reference kit. It does not provide a
hosted service, implementation support, or a service-level commitment.

## Change and release rules

- A change to the public package must keep `tests/verify_public_package.py`
  passing and update `PUBLIC-MANIFEST.json` through the package build process.
- Pull requests and changes to `main` run the public integrity workflow.
- Each published kit version records user-visible changes in `CHANGELOG.md`.
- A release steward may create an immutable `vMAJOR.MINOR.PATCH` tag only after
  the integrity workflow has passed for the intended `main` commit.

## Versioning

`Kit-Version` identifies the public distribution. `Template-Schema-Version`
identifies the independent contract format used by the templates. A schema
change does not by itself imply a kit release, and a kit release does not by
itself imply a schema change.

## Maintenance boundary

The kit maintains documentation, templates, the manifest, and its integrity
check. Adopting projects remain responsible for their own runtime, security,
access controls, testing, deployment, and release decisions.
