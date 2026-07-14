# Example Architecture Canon: Lantern Notes

Project: lantern-notes
Component: architecture-canon-example
Status: ACTIVE
Template-Schema-Version: v0.3.0
Date: 2026-07-14
Review-Date: 2026-10-14
Owner: fictional product maintainer

## Canonical Boundaries

- the interface layer accepts user input and presents results;
- the application layer owns note use cases;
- the storage layer owns persistence details.

## Dependency Rules

- interfaces may call application use cases;
- application use cases may call the storage boundary;
- storage details must not leak into the interface layer.

## Approved Patterns

- one named use case per user-visible workflow;
- validation at the boundary before persistence.

## Forbidden Patterns

- direct persistence calls from interface code;
- hidden side effects in read-only review flows.
