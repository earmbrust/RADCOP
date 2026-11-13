# Roadmap

## Objectives
Publish a small, useful, agent- and chat-agnostic continuity protocol with a reusable audit skill.

## Milestone Order
| ID | Milestone | Status | Dependencies |
| --- | --- | --- | --- |
| M001 | Publish draft RAP specification and templates | Accepted (2026-11-12) | None |
| M002 | Refine long-term state tracking, archival guidance, and consistency validation | Implemented; source review complete, current-revision CI and owner acceptance pending | M001 (satisfied 2026-11-12) |
| M003 | Gather additional interoperability feedback | Planned | M002 |

## Active Milestone
### M002 — Refine long-term state tracking, archival guidance, and consistency validation

**Status:** Implemented and reviewed against acceptance criteria; pending verified CI evidence at the merged revision and separate owner acceptance.

**M001 prerequisite:** Satisfied by explicit owner acceptance on 2026-11-12.

**Objective:** Preserve durable continuity for long-running projects without introducing mandatory indexing or retrieval infrastructure.

**Scope:** Bounded active state, optional traceable archives, specification §12, root templates, skill guidance, read-only archive-reference checking, and tests.

**Architectural references:** `ARCHITECTURE.md` and `spec/RAP_SPECIFICATION.md` §12.

**Dependencies:** M001 (accepted 2026-11-12).

**Acceptance criteria:** Owner review and successful relevant checks at an identifiable revision, with no contradictory authority or new mandatory orchestration requirements.

**Verification disposition:** Source review at merged `main` revision `11e293b0201891c17a5ff1633f5d9e640436556e` found the specified deliverables present and no conflicting design authority or mandatory services. Six local Python tests and zero structural findings were reported before merge; GitHub CI at the merged revision has not been independently confirmed in this closeout review. M002 is not yet owner-accepted.

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
- 2026-11-13 closeout review: M002 implementation inspected at merged revision `11e293b`; outstanding requirements are current-revision execution evidence and explicit owner acceptance.

## State Tracking Refinement Scope
M002 deliverables remain specification §12, root templates, skill guidance, read-only archive reference checking, and tests. Verification and owner acceptance remain distinct from implementation presence.

## Release Infrastructure (Operational Work)
PR #1 merged into `main` on 2026-11-13 at `11e293b0201891c17a5ff1633f5d9e640436556e`, including release automation, review-documentation guidance, and M001 reconciliation. The tagged-release workflow has not been verified through a published release; no GitHub Release is claimed.
