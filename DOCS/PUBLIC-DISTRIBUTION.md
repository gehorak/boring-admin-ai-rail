# Public Distribution Boundary

This package is intentionally limited to adoption guidance, neutral
templates, and a package-integrity check.

It is suitable for evaluation, documentation-first adoption, and adaptation
inside another repository. It does not represent a complete implementation
or confer support, operational readiness, or deployment authorization.

An adopting team must establish its own local rules, implementation controls,
and evidence appropriate to its environment.

`PUBLIC-MANIFEST.json` distinguishes `distribution_files`, whose hashes are
verified as the adoption kit, from `repository_control_paths`, which are
repository metadata needed to keep that verification running. Any file outside
those declared sets is rejected by the integrity check.
