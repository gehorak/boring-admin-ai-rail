# Maintenance

The public repository is a generated distribution. Do not repair a public
implementation or document directly. Make the correction in the maintained
canonical source, update the versioned export classification, and generate a
new candidate from an explicit immutable commit.

Before publication, run the export verifier, the public package verifier,
public regression tests, a clean wheel build and installation check, and the
public CLI smoke check. The corresponding public GitHub Actions workflow is
also generated from the same internal source.

The public subset is MIT-licensed only within the explicit scope in
`LICENSES/PUBLIC-SUBSET-MIT.md`. Changing its version, tag, release, or
repository contents is a separate human decision and is not authorized by a
successful export.
