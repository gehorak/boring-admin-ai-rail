# Example Project: Lantern Notes

This example is fictional. It demonstrates how an adopting team can fill the
public templates without exposing credentials, production data, or private
implementation details.

## Project Identity

- repository: `lantern-notes`
- owner: product maintainer
- status: bootstrap

## Project Purpose

Lantern Notes is a small service for collecting and reviewing team notes.
The first goal is a clear, searchable record of decisions made during a
project week.

## System Boundaries

- in scope: note capture, note review, and local project documentation
- out of scope: billing, user analytics, and production deployment policy

## Architectural Canon

- user-facing code calls the application layer through named use cases;
- persistence is accessed through one documented storage boundary;
- project documentation describes intent and boundaries, not credentials.

## Codebase Voice

- naming: use explicit nouns for domain concepts and verbs for actions;
- tests: cover each use case and its important failure path;
- comments: explain constraints and decisions, not syntax.

## Approved Integration Points

- note submission interface;
- note review interface;
- storage boundary.

## Do-Not-Touch Areas

- credentials and environment configuration;
- deployment configuration owned by the operations team.

## Local Exceptions

- none.

## Selected Modules

- development;
- security.

## Review Focus

- accidental exposure of note content or credentials;
- changes that bypass the storage boundary.
