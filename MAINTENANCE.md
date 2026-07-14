# Maintenance Policy

This repository is an adoption reference kit with an optional operational
documentation profile. It does not provide a hosted service, implementation
support, execution runtime, or a service-level commitment.

## Change and release rules

- A change to the public package must keep `tests/verify_public_package.py`
  passing and update `PUBLIC-MANIFEST.json` through the package build process.
- Pull requests and changes to `main` run the public integrity workflow.
- The Bootstrap-Complete test suite runs with
  `python -m unittest discover -s tests -p 'test_*.py'` and uses only the
  Python standard library.
- Each published kit version records user-visible changes in `CHANGELOG.md`.
- A release steward may create an immutable `vMAJOR.MINOR.PATCH` tag only after
  the integrity workflow has passed for the intended `main` commit.

## Versioning

`Kit-Version` identifies the public distribution. The manifest carries three
independent contract axes: `base_template_schema_version` for the compact
adoption templates, `operational_template_schema_version` for the optional
operational templates, and `contract_data_schema_version` for JSON contracts.
`template_schema_version` remains the compatibility alias for the operational
template axis. A change to one axis does not by itself imply a kit release or a
change to another axis.

## Maintenance boundary

The kit maintains documentation, data contracts, templates, the manifest, and
its integrity check. Adopting projects remain responsible for their own
runtime, security, access controls, testing, deployment, and release
decisions.
