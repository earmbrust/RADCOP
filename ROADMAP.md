# Roadmap

## Objectives
Publish a small, useful, agent- and chat-agnostic continuity protocol with a reusable audit skill.

## Milestone Order
| ID | Milestone | Status | Dependencies |
| --- | --- | --- | --- |
| M001 | Publish draft RAP specification and templates | Implemented (awaiting owner acceptance) | None |
| M002 | Refine long-term state tracking, archival guidance, and consistency validation | In Progress (draft) | M001 |
| M003 | Gather additional interoperability feedback | Planned | M002 |

## Active Milestone
### M001 — Publish draft RAP specification and templates

**Objective:** Provide a publicly reviewable draft package.

**Scope:** Specification, templates, skill, installation instructions, structural checker, and tests.

**Architectural references:** See `ARCHITECTURE.md` and the specification's ownership/authority rules.

**Dependencies:** None.

**Deliverables:** Portable ZIP and repository source tree.

**Acceptance criteria:** Files complete; tests runnable; owner reviews and accepts scope/wording.

**Verification:** Execute Python unit tests and script smoke checks. Owner acceptance is separate.

## Upcoming Milestones
M002 — Define bounded active state, optional traceable archives, and archive-reference audits without introducing retrieval infrastructure.
M003 — Gather further interoperability feedback and improve compatibility without adding mandatory services.

## Completed Milestone Index
None confirmed as owner-accepted from the available repository record; M001 is marked implemented, awaiting acceptance.

## Deferred or Out-of-scope Work
No mandatory daemon, orchestration platform, online service, or agent communication protocol.

## Roadmap Change Log
Initial draft established, pending owner approval.

## State Tracking Refinement Scope
M002 draft deliverables: specification §12, root templates, skill guidance, read-only archive reference checking, and tests. Acceptance requires owner review and successful relevant checks; no acceptance is claimed here.
