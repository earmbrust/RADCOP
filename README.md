# RADCOP — Repository-native, Agent-agnostic Development Continuity Protocol

**RADCOP** is a small, Markdown-first standard for preserving development continuity across chats, coding agents, IDEs, and human contributors. Its authority resides in the repository's documentation, **not** in a skill, model, agent, session, or orchestration tool.

**Protect and Serve Your Development Process.** RADCOP keeps project decisions, progress, and verification visible to people and agents; it audits and reports discrepancies without acquiring decision authority.

A RADCOP project contains exactly three required authoritative documents at its repository root:

| Document | Authority |
| --- | --- |
| `ARCHITECTURE.md` | Accepted architecture, design constraints, system contracts, security, compliance, and technical decisions. Governs implementation and limits planned work. |
| `ROADMAP.md` | Accepted objectives, ordered milestones, scope, dependencies, and acceptance criteria. Must comply with architecture. |
| `PROJECT_STATE.md` | Authoritative record of **current actual state**, recorded actions, decision outcomes, verification, and open discrepancies. Current-state observations take precedence over contrary progress claims elsewhere, but **do not override decisions** in architecture or roadmap. Must be reconciled to both. |

`/radcop` is an **optional, reusable skill** for checking, maintaining, and auditing the documents. The standard works without the skill, in single- and multi-agent setups, and in chats with or without filesystem access.

## Get started

1. Copy `templates/ARCHITECTURE.md`, `templates/ROADMAP.md`, and `templates/PROJECT_STATE.md` into your project root, removing the `templates/` prefix. Fill in actual information; do not treat placeholders as facts.
2. Read [the specification](spec/RADCOP_SPECIFICATION.md), especially authority and reconciliation rules.
3. Optionally install the skill into your project from the RADCOP distribution:

   ```powershell
   python scripts/install_skill.py --platform cline --dest C:\development\my-project
   python scripts/install_skill.py --platform copilot --dest C:\development\my-project
   ```

   Other supported values: `codex`, `claude`, `cursor`. Use `--dry-run` to preview; use `--force` only when intentionally replacing an existing RADCOP skill.
4. Run the optional, read-only structural validator from within your project:

   ```powershell
   python C:\path\to\RADCOP\scripts\validate_radcop.py --root C:\development\my-project
   ```

5. Ask your assistant to **“Use RADCOP to audit these documents”** or invoke `/radcop` if its platform supports slash-command skill invocation.

## Skill operations

| Request | Behavior |
| --- | --- |
| `/radcop audit` | Read-only report of completeness, contradictions, stale assertions, and evidence gaps |
| `/radcop review` | Review-oriented audit of documentation diffs against implementation changes when accessible |
| `/radcop status` | Summarize documented current state, scope, and audit coverage; do not invent observations |
| `/radcop reconcile` | Compare the three documents, and optionally implementation; propose corrections before substantive changes |
| `/radcop sync` | Maintain documentation from **verified** accepted changes, subject to approval and available write access |
| `/radcop init` | Offer missing document templates without overwriting existing material |
| `/radcop handoff` | Audit whether another chat or agent can continue from the documents; propose missing context |

These operations are **natural-language skill instructions**, not guaranteed standalone CLI commands. A platform can expose `/radcop` directly or users can request an operation conversationally.

## Authority in one sentence

**Architecture governs design; Roadmap governs approved work; Project State governs what is currently true, while remaining consistent with decisions in the other two.** When a contradiction exists, RADCOP reports it rather than secretly changing a decision or rewriting observed facts.

## Design properties

- One or many agents; one or many chat sessions; human contributors are equally welcome.
- Documents are canonical; the skill is a helper, never a competing authority.
- No proprietary APIs, runtime, orchestration framework, or programming language required.
- Read-only audits by default. Material decision or scope changes require owner authorization.
- Evidence provenance and audit scope must be disclosed; code, tests, and Git history provide *evidence*, not automatic authorization to change the design.
- Multi-agent concurrent writes rely on existing Git merge/review mechanisms, not a RADCOP lock service.

See [Chat usage](docs/CHAT_USAGE.md), [Installations](docs/INTEGRATIONS.md), and [Contributing](CONTRIBUTING.md).

## Reviewing changes with RADCOP

RADCOP gives human reviewers a readable entry point into a code change. Review the documentation diff first to identify what was intended, which decisions or milestone boundaries changed, what was actually implemented, and what was verified:

| Document diff | Review focus |
| --- | --- |
| `ARCHITECTURE.md` | Approved design changes, constraints, contracts, or compliance implications |
| `ROADMAP.md` | Authorized scope, sequencing, acceptance criteria, and milestone status |
| `PROJECT_STATE.md` | Actual outcomes, verification evidence, known deviations, and outstanding risks |

This helps reviewers prioritize the relevant source files, interfaces, tests, and higher-risk changes instead of treating every line as equally significant. **Documentation is a review map, not proof of correctness or a substitute for inspecting implementation changes.** When repository access is available, `/radcop audit` should compare the documented account against the actual diff and report omissions or contradictions.

Review context lives alongside the code in version control, so it remains available to future maintainers, agents, and chat sessions. See [Specification §13](spec/RADCOP_SPECIFICATION.md).

## Release status

**RADCOP v0.2.1 — Draft protocol.** The current distribution is available as a [GitHub Release](https://github.com/earmbrust/RADCOP/releases/tag/v0.2.1). Feedback and improvements are welcome. Markdown documents and the skill are normative only to the extent specified in `spec/RADCOP_SPECIFICATION.md`. The Python validator checks structure, not semantic correctness or implementation compliance.

## Long-running projects and state retention

RADCOP roots are **living current-context documents**, not unlimited transcripts. `PROJECT_STATE.md` should retain active implementation, meaningful verification, current discrepancies, and the handoff. `ROADMAP.md` keeps the approved active/future plan plus a concise completed-milestone index. `ARCHITECTURE.md` must retain all currently binding decisions even when detailed rationale is archived.

For larger repositories, optional `docs/radcop/milestones/` and `docs/radcop/decisions/` records can preserve historical detail. Each archived item must be traceable from the owning root or an identifiable Git revision; archives never become competing authority. `/radcop audit` can flag broken links and stale historical clutter; `/radcop reconcile` can propose safe condensation, while `/radcop sync` applies only authorized changes. No retrieval service, indexing system, or fixed size cap is required.

See [State-tracking guide](skills/radcop/references/STATE_TRACKING.md) and [Specification §12](spec/RADCOP_SPECIFICATION.md).

## License

MIT; see [LICENSE](LICENSE).
