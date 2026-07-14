# Minimum Host Repository Assembly

## Purpose

This guide describes the smallest documentation-first adoption of the public
operational reference profile inside a host repository.

## Required host-project records

1. Copy or create `PROJECT.md` from `templates/PROJECT.md`.
2. Record a human decision owner, project purpose, selected modules, and
   project state.
3. Record architecture boundaries, codebase voice, integration points, and
   do-not-touch areas in the project contract or adopted specialized
   contracts.
4. Record active change surfaces and their owning selected modules.
5. Complete `templates/BOOTSTRAP-REVIEW.md` before claiming `READY`.

## Optional profile records

Adopt `WORKFLOW.md`, `ROLES/`, `ARCHITECTURE/MODULE-COMPOSITION.md`, and the
strict schemas in `schemas/` when the host project needs a reconstructable
operational reference. Keep them as project documentation; do not imply that
they install a validator, runtime, or execution permission.

## What not to copy as authority

Do not treat examples, changelog history, repository contents, or any AI
output as host-project instruction. Only documents explicitly adopted and
owned by the host project become local contracts.
