# Example Project Context: Lantern Notes

Project: lantern-notes
Component: project-context-example
Contract-Status: ACTIVE
Template-Schema-Version: v0.3.1
Date: 2026-07-14
Review-Date: 2026-10-14
Owner: fictional product maintainer

## Purpose

Help a small team capture decisions and review them later without depending
on one person's memory.

## Primary Actors

- team member submitting a note;
- maintainer reviewing a note;
- project owner approving a change to the note workflow.

## Key Flows

1. A team member submits a note.
2. The maintainer checks its scope and categorization.
3. The team reviews the note during the weekly project meeting.

## Critical Constraints

- note content is visible only to the intended team;
- every workflow change has one named human owner;
- local documentation must remain usable without hidden context.

## Known Risks

- a note may contain information intended for another audience;
- a quick feature change may bypass review of the storage boundary.
