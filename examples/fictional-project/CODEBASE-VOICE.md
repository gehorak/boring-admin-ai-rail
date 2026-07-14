# Example Codebase Voice: Lantern Notes

Project: lantern-notes
Component: codebase-voice-example
Contract-Status: ACTIVE
Template-Schema-Version: v0.4.1
Date: 2026-07-14
Review-Date: 2026-10-14
Owner: fictional product maintainer
Document-Conflict: NONE

## Naming Rules

Use names that describe the domain action or boundary. Avoid unexplained
abbreviations.

## Structure Rules

Keep interface, application, and storage concerns in separate directories.

## Testing Style

Every user-visible workflow has a normal-path test and a meaningful rejection
or failure-path test.

## Refactor Boundaries

Refactor one layer at a time and preserve the documented integration points.

## Forbidden Shortcuts

Do not place credentials in source files or use a global helper to bypass a
layer boundary.
