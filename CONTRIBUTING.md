# Contributing to RAP

RAP's goal is minimal, portable documentation continuity. Changes should preserve the canonical three-file model, the authority distinction between decisions and observed state, and operation in ordinary chats as well as single- or multi-agent environments.

For proposed changes, explain the failure mode, normative behavior proposed, compatibility impact, and a concrete example. Add tests for validator or installer changes. Avoid requiring a specific platform, orchestrator, paid service, build system, or programming language. Do not add normative rules to the skill that contradict `spec/RAP_SPECIFICATION.md`.

## Reviewing pull requests

Start with the `ARCHITECTURE.md`, `ROADMAP.md`, and `PROJECT_STATE.md` diffs when they are present. They should indicate design implications, approved scope, actual outcomes, verification and risks, so reviewers can prioritize relevant source changes. Compare those statements to the code and test diff; do not assume an unchanged document proves there is no impact, or treat the documentation as a substitute for code review. Ask for a reconciliation when material changes are omitted or contradict the authoritative documents.

## Public draft governance

This is a draft proposal, not a formal standards-body specification. Changes to decision authority and required files should be reviewed explicitly before inclusion in the public spec.
