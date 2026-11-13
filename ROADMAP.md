# Roadmap

## Objectives
Publish a small, useful, agent- and chat-agnostic continuity protocol with a reusable audit skill.

## Milestone Order
| ID | Milestone | Status | Dependencies |
| --- | --- | --- | --- |
| M001 | Publish draft RAP specification and templates | Accepted (2026-11-12) | None |
| M002 | Refine long-term state tracking, archival guidance, and consistency validation | Active; draft implementation present, verification and acceptance pending | M001 (satisfied 2026-11-12) |
| M003 | Gather additional interoperability feedback | Planned | M002 |

## Active Milestone
### M002 — Refine long-term state tracking, archival guidance, and consistency validation

**Status:** Active; implementation present on `main`, pending verification and owner acceptance.

**M001 prerequisite:** Satisfied by explicit owner acceptance on 2026-11-12.

**Objective:** Preserve durable continuity for long-running projects without introducing mandatory indexing or retrieval infrastructure.

**Scope:** Bounded active state, optional traceable archives, specification §12, root templates, skill guidance, read-only archive-reference checking, and tests.

**Architectural references:** `ARCHITECTURE.md` and `spec/RAP_SPECIFICATION.md` §12.

**Dependencies:** M001 (accepted 2026-11-12).

**Acceptance criteria:** Owner review and successful relevant checks at an identifiable revision, with no contradictory authority or new mandatory orchestration requirements.

**Current disposition:** M002 is the active milestone; draft implementation is present on `main`. Verify the current revision and obtain separate owner acceptance before marking M002 accepted.

## Upcoming Milestones

### M003 — Gather additional interoperability feedback

Planned after M002 acceptance; improve compatibility without adding mandatory services.

## Completed Milestone Index
- **M001 — Publish draft RAP specification and templates:** Owner accepted 2026-11-12. Initial deliverables are committed; acceptance was explicitly provided in the project discussion. Historical implementation details remain in Git.

## Deferred or Out-of-scope Work
No mandatory daemon, orchestration platform, online service, or agent communication protocol.

## Roadmap Change Log
- Initial draft established, subsequently accepted as M001 on 2026-11-12.
- 2026-11-12 reconciliation: M001 explicitly owner-accepted, removing its acceptance blocker; M002 becomes active. No M002 acceptance, scope change, or new verification is implied.

## State Tracking Refinement Scope
M002 deliverables remain specification §12, root templates, skill guidance, read-only archive reference checking, and tests. Verification and owner acceptance remain distinct from implementation presence.

## Release Infrastructure (Operational Work)
Release automation and M001 reconciliation were consolidated in `f4732cc` on `chore/release-automation`; later review-documentation changes are also pushed to that branch. At the 2026-11-13 inspection, the branch was two commits ahead of `main` and not merged. No GitHub Release or hosted workflow result is claimed.
