# Roadmap

## Objectives
Publish a small, useful, agent- and chat-agnostic continuity protocol with a reusable audit skill.

## Milestone Order
| ID | Milestone | Status | Dependencies |
| --- | --- | --- | --- |
| M001 | Publish draft RAP specification and templates | Accepted (2026-11-12) | None |
| M002 | Refine long-term state tracking, archival guidance, and consistency validation | Accepted (2026-11-13; closeout PR #2) | M001 (satisfied 2026-11-12) |
| M003 | Gather additional interoperability feedback | Planned | M002 |

## Active Milestone
No milestone is currently active. M003 is planned; its activation requires an authorized work decision, not an inferred consequence of M002 acceptance.

## Upcoming Milestones

### M003 — Gather additional interoperability feedback

Planned after M002 acceptance (now satisfied); improve compatibility without adding mandatory services. Not yet activated.

## Completed Milestone Index
- **M001 — Publish draft RAP specification and templates:** Owner accepted 2026-11-12. Initial deliverables are committed; acceptance was explicitly provided in the project discussion. Historical implementation details remain in Git.
- **M002 — Refine long-term state tracking, archival guidance, and consistency validation:** Accepted by the owner on 2026-11-13 through merge of the explicitly designated closeout PR #2 (`eb5efea69bfefb0b4934bd8bc3c18afe7db80b7b`). Implementation includes specification §12, templates, skill guidance, conservative archive-link checks, and tests. The six passing local tests and zero structural findings were reported before the merge; a hosted CI success is not asserted here.

## Deferred or Out-of-scope Work
No mandatory daemon, orchestration platform, online service, or agent communication protocol.

## Roadmap Change Log
- Initial draft established, subsequently accepted as M001 on 2026-11-12.
- 2026-11-12 reconciliation: M001 explicitly owner-accepted, removing its acceptance blocker; M002 becomes active. No M002 acceptance, scope change, or new verification is implied.
- 2026-11-13 closeout review: M002 implementation inspected at revision `11e293b`; verification evidence and limitations recorded in PR #2.
- 2026-11-13 acceptance: Owner merged designated M002 closeout PR #2, approving the milestone as complete. No further post-merge acceptance gate is imposed; historical execution-evidence limitations remain disclosed.

## State Tracking Refinement Scope
M002 deliverables remain specification §12, root templates, skill guidance, read-only archive reference checking, and tests. Verification and owner acceptance remain distinct from implementation presence.

## Release Infrastructure (Operational Work)
PR #1 merged into `main` on 2026-11-13 at `11e293b0201891c17a5ff1633f5d9e640436556e`, including release automation, review-documentation guidance, and M001 reconciliation. The tagged-release workflow has not been verified through a published release; no GitHub Release is claimed.

## Milestone Acceptance Workflow
Milestone closeout requires explicit owner approval **before** merge. The closeout PR must request that approval, identify its acceptance disposition, and include the corresponding root-document changes. Upon authorized approval, merging the PR carries the accepted disposition into `main`; acceptance is not a separate post-merge decision. An unapproved closeout, ordinary implementation PR, automated merge, or merge by an actor without delegated acceptance authority does not establish milestone acceptance. Later factual reconciliation of merge metadata does not add a second approval gate.
