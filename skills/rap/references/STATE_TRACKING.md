# RAP state tracking and archival guide

This guide supports [RAP Specification §12](../../../spec/RAP_SPECIFICATION.md) when working from the source distribution. An installed skill might not include that specification; the rules below remain a portable summary.

## Root document obligations

| Root file | Keep current and authoritative | Condense/archive supporting detail |
| --- | --- | --- |
| `PROJECT_STATE.md` | Current snapshot, active/blocked work, verified evidence, deviations, next work, current accepted decision outcomes | Detailed completed actions, historical tests, superseded observations |
| `ROADMAP.md` | Approved objectives, active and upcoming ordered milestones, dependencies and acceptance criteria, completed milestone index | Detailed execution narratives for completed milestones |
| `ARCHITECTURE.md` | All currently binding constraints, contracts, compliance and accepted design decisions | Superseded rationale, decision discussions, historical alternatives |

## Audit procedure

1. Read all available authoritative root documents and record source revision/coverage.
2. Identify active state and decisions that remain binding; do **not** move them to archives exclusively.
3. Identify long-form history, duplicates, stale handoffs, superseded decisions and completed milestone detail that could be condensed.
4. Verify each proposed or existing archive reference, if repository access permits. Report missing targets, unsupported Git revisions, and misleading supersession status.
5. Check cross-document consistency: ARCHITECTURE governs design, ROADMAP governs approved sequence/scope, PROJECT_STATE governs actual current status, never other documents' decisions.
6. For an archival proposal, show: retained active summary; proposed archival record path; source content to preserve; stable references; approvals required; verification available.
7. Never make edits during audit. For sync, edit only with authorization and permissions, then recheck root links.

## Archive record recommendations (non-normative)

Completed milestone record: stable ID; objective; approved scope and criteria reference; actual deliverables; verification evidence and revision; acceptance if authorized; unresolved follow-ups; superseded-by reference when applicable.

Historical decision record: stable ID; accepted/proposed/superseded status; rationale; date/revision if known; owner or approval evidence if known; owning root document and successor decision reference. The accepted binding decision remains in the authoritative root.

## Common defects to flag

- Historical milestone text displaces active state or active plan.
- `PROJECT_STATE.md` claims acceptance without authorization or verification without evidence.
- Archived constraints disappear from ARCHITECTURE although still binding.
- ROADMAP drops all indication that completed milestones existed.
- A link points to a missing local file or a revision which was not checked.
- A historical record is silently rewritten to remove a deviation.
- The assistant assumes a retrieval/indexing platform is required.

## Report vocabulary

`PASS`, `WARNING`, `CONFLICT`, `NOT_CHECKED`. Always distinguish structural checks from semantic checks. Missing access is `NOT_CHECKED`, not `PASS`.
