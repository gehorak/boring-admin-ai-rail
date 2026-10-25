# BORING-ADMIN-AI-RAIL Public Reference Distribution

This repository tree is a generated, read-only mirror of approved
components from one privately maintained canonical source. Its implementation, package
resources, templates, and regression test are not maintained here.

## Source identity

- Source baseline identity: `v0.5.0`
- Recorded export source commit: `10d3f2e77dc36049621ddb05b870858818f184cd`
- Public distribution version: `0.3.0rc1`
- Public API compatibility identity: `0.2.2`

`PUBLIC-MANIFEST.json` records every generated or copied path and its
SHA-256 digest. `PUBLIC-EXPORT-REPORT.json` records the completed
source-identity, licensing, private-content, and inventory checks.

Do not manually edit this tree or synchronize changes back to the
maintained source. Make a change in that source, update the
versioned export classification, and generate a new candidate from an
explicit source commit.

Public documentation navigation is in DOCS/INDEX.md, including a
Czech quickstart, adoption boundary, security boundary, and maintenance
guidance generated from the same internal source commit.

## Local use

```bash
python -m pip install --no-deps .
python -m public_rail --help
python -m unittest discover -s tests -v
```

The profile is offline and structural. A validation result does not
create an approval, execution capability, model invocation, or tool call.

## License

This distribution is licensed under MIT; see `LICENSE`.
The scope of the MIT public-subset exception is documented in
`LICENSES/PUBLIC-SUBSET-MIT.md`. Historical public releases retain
their existing grants.
