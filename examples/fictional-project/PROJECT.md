# Example Project: Lantern Notes

Project: lantern-notes
Component: project-example
Contract-Status: ACTIVE
Template-Schema-Version: v0.4.1
Date: 2026-07-14
Review-Date: 2026-10-14
Owner: fictional product maintainer
Document-Conflict: NONE

This example is fictional. It demonstrates how an adopting team can fill the
public templates without exposing credentials, production data, or private
implementation details.

## Project Identity

- repository: `lantern-notes`
- decision owner: product maintainer
- project state: bootstrap

## Project Purpose

Lantern Notes is a small service for collecting and reviewing team notes.
The first goal is a clear, searchable record of decisions made during a
project week.

## System Boundaries

- in scope: note capture, note review, and local project documentation
- out of scope: billing, user analytics, and production deployment policy

## Architectural Canon

Canonical source: `./ARCHITECTURE-CANON.md`

Summary:

- user-facing code calls the application layer through named use cases;
- persistence is accessed through one documented storage boundary.

## Codebase Voice

Canonical source when adopted: `./CODEBASE-VOICE.md`

Summary:

- naming uses explicit nouns for domain concepts and verbs for actions;
- tests cover each use case and its important failure path.

## Approved Integration Points

Canonical source when adopted: `./INTEGRATION-POINTS.md`

Summary:

- note submission and review interfaces;
- storage boundary.

## Do-Not-Touch Areas

- credentials and environment configuration;
- deployment configuration owned by the operations team.

## Local Exceptions

- none.

## Selected Modules

N/A. Lantern Notes has not defined a local module ownership model.

## Review Focus

- accidental exposure of note content or credentials;
- changes that bypass the storage boundary.

## Contract Precedence

- this document is the top-level index and project contract;
- an active specialized contract overrides its summary when that contract is
  adopted;
- a disagreement between documents is a validation failure and must be
  resolved by the human decision owner before implementation.
