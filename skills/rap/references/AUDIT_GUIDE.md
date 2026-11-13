# RAP audit and reconciliation guide

## Minimum audit matrix

| Area | Questions |
| --- | --- |
| Presence | Are all three root files present, readable, and non-placeholder? |
| Design authority | Does roadmap conflict with accepted architecture, constraints, or prohibitions? |
| State accuracy | Do implementation, test, and Git evidence support state claims, when accessible? |
| Decision ownership | Are new architecture/scope decisions recorded in their owning documents, not solely in state? |
| Cross references | Do milestone IDs, decision references, paths, and statuses agree? |
| Validation | Are status assertions distinguished from tested/accepted evidence? |
| Handoff | Is next authorized work identifiable? Are blockers and unknowns clear? |
| Concurrency | Are there conflict markers, unreviewed competing changes, or stale revisions? |

## Required finding categories

- `PASS`: checked and supported within stated evidence scope.
- `WARNING`: incomplete, stale, unclear, or unverifiable claim.
- `CONFLICT`: incompatible accepted requirements, discrepant state, or contradicted evidence.
- `NOT_CHECKED`: inaccessible document, repository, test suite, or reference.

## Reconciliation rules

1. Prefer making PROJECT_STATE accurately describe the observed current implementation, including when it deviates from approved architecture or roadmap.
2. Keep design decisions in ARCHITECTURE and milestone decisions in ROADMAP, not merely in the decision log within PROJECT_STATE.
3. If a roadmap item conflicts with architecture, flag the conflict and request owner resolution; do not silently alter it.
4. Record any deviation as unresolved until implementation changes or the authorized owner approves a decision update.
5. For acceptance status, distinguish implementer report, verified checks, reviewer signoff, and owner acceptance.
6. Do not change documents during a read-only audit; output proposed patches when edits cannot be made.

## Suggested report template

```text
RAP AUDIT
Scope: [documents/files/revision accessible]
Evidence checked: [code, Git, tests, or none]
Summary: [N PASS / N WARNING / N CONFLICT / N NOT_CHECKED]
Findings:
- [CONFLICT] [file/heading]: [contradiction]. Evidence: [...].
  Proposed resolution: [...]. Approval: [required/not required].
Unresolved questions: [...]
Actions performed: [read-only / specific edits]
Not checked: [...]
```

## No false certification

The standalone `validate_rap.py` only checks document presence/structure and merge markers. Never present its success as semantic reconciliation, repository implementation verification, or owner acceptance.
