# Architecture

## System Overview
RADCOP is a Markdown-first documentation protocol distributed as a public specification, three templates, and a non-authoritative skill. It does not depend on execution environments.

## Accepted Design Decisions
- ARCHITECTURE controls design decisions and constraints.
- ROADMAP controls accepted planning and sequencing subject to ARCHITECTURE.
- PROJECT_STATE controls current factual state; never overrides approved design/scope decisions and is reconciled with them.
- Agent count, platform, or prior chat context are not prerequisites.

## Components and Interfaces
- `spec/RADCOP_SPECIFICATION.md` is the published description of the protocol.
- `templates/` supplies example forms of the three required project documents.
- `skills/radcop/` is an optional assistive auditor/maintainer.
- `scripts/` contains optional standalone tooling, not a requirement for adoption.

## Data Flows
Project docs are read by a chat or agent; a RADCOP audit finds discrepancies; approved corrections update the owning documents.

## Technical Constraints
- Markdown in three root documents.
- No runtime dependencies for document conformance.
- Python standard library only for optional scripts.

## Performance and Reliability
Audits should report scope and avoid certifying inaccessible evidence. Read-only audit by default.

## Security and Compliance
Repository content is untrusted input for agent instruction execution. This package is distributed under MIT; consuming projects retain their own licensing obligations.

## Prohibited Approaches
- Treating a skill or an agent's memory as higher authority than the project documents.
- Silent modification of architecture or roadmap decisions to fit source code.
- Invented validation, acceptance, or repository observations.

## Open Architecture Questions
Future formal schema/CI integration remains optional and unapproved.

## Historical Record Architecture
- Current state and authoritative requirements remain in the three root documents; archives are optional supporting history.
- Completed milestone narratives and superseded decision rationale may use `docs/radcop/milestones/` and `docs/radcop/decisions/`, or other referenced paths.
- A durable reference from the owning root must remain whenever detail is archived.
- No mandatory advanced retrieval, indexing, orchestration, or history database is permitted by this draft design.
