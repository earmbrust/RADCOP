# Contributing to RAP

RAP's goal is minimal, portable documentation continuity. Changes should preserve the canonical three-file model, the authority distinction between decisions and observed state, and operation in ordinary chats as well as single- or multi-agent environments.

For proposed changes, explain the failure mode, normative behavior proposed, compatibility impact, and a concrete example. Add tests for validator or installer changes. Avoid requiring a specific platform, orchestrator, paid service, build system, or programming language. Do not add normative rules to the skill that contradict `spec/RAP_SPECIFICATION.md`.

## Branch and release workflow

`main` is the authoritative branch. Use short-lived branches and merge them into `main` through a pull request:

- `feature/<description>` for new capabilities.
- `fix/<description>` for non-urgent defect fixes.
- `hotfix/<description>` for urgent release fixes.
- `chore/<description>` for maintenance, CI, and tooling.
- `docs/<description>` for documentation-only work.

The CI workflow runs the Python unit tests and structural validator for pull requests targeting `main` and for pushes to `main`. Repository branch protection is configured separately in GitHub; this repository workflow does not itself prohibit direct pushes.

To publish a release, merge the accepted release commit into `main`, then create and push an annotated semantic-version tag such as `v0.2.0`:

```powershell
git switch main
git pull --ff-only
git tag -a v0.2.0 -m "RAP v0.2.0"
git push origin v0.2.0
```

The release workflow accepts only `vMAJOR.MINOR.PATCH` tags whose commits are in `main` history. It runs validation, packages the exact tagged tree as `RAP-vMAJOR.MINOR.PATCH.zip`, omits Git metadata and repository-only files, writes a SHA-256 checksum, and attaches both assets to the matching GitHub Release.

## Reviewing pull requests

Start with the `ARCHITECTURE.md`, `ROADMAP.md`, and `PROJECT_STATE.md` diffs when they are present. They should indicate design implications, approved scope, actual outcomes, verification and risks, so reviewers can prioritize relevant source changes. Compare those statements to the code and test diff; do not assume an unchanged document proves there is no impact, or treat the documentation as a substitute for code review. Ask for a reconciliation when material changes are omitted or contradict the authoritative documents.

## Milestone closeout approval

Prepare a milestone closeout PR identifying the milestone, deliverables, verification evidence, remaining gaps, and proposed accepted status. **Request and obtain explicit owner approval before merging.** The closeout PR is the approval gate: after approval, merge it so the approved milestone disposition flows into `main` as part of the merge, rather than requiring a second approval or corrective PR. An unapproved closeout MUST NOT be merged as accepted. Ordinary implementation PRs, automated merges, and merges by unauthorized actors do not establish milestone acceptance. The PR should include the final `ROADMAP.md` and `PROJECT_STATE.md` disposition and cite its acceptance evidence; a subsequent factual reconciliation is permitted if the merge SHA was not known in advance, but it must not be an additional acceptance gate. This is RAP repository guidance, not a requirement that every adopting project use GitHub.

## Public draft governance

This is a draft proposal, not a formal standards-body specification. Changes to decision authority and required files should be reviewed explicitly before inclusion in the public spec.
