# RAP — Repository-native, Agent-agnostic Development Continuity Protocol

**RAP** is a small, Markdown-first standard for preserving development continuity across chats, coding agents, IDEs, and human contributors. Its authority resides in the repository's documentation, **not** in a skill, model, agent, session, or orchestration tool.

A RAP project contains exactly three required authoritative documents at its repository root:

| Document | Authority |
| --- | --- |
| `ARCHITECTURE.md` | Accepted architecture, design constraints, system contracts, security, compliance, and technical decisions. Governs implementation and limits planned work. |
| `ROADMAP.md` | Accepted objectives, ordered milestones, scope, dependencies, and acceptance criteria. Must comply with architecture. |
| `PROJECT_STATE.md` | Authoritative record of **current actual state**, recorded actions, decision outcomes, verification, and open discrepancies. Current-state observations take precedence over contrary progress claims elsewhere, but **do not override decisions** in architecture or roadmap. Must be reconciled to both. |

`/rap` is an **optional, reusable skill** for checking, maintaining, and auditing the documents. The standard works without the skill, in single- and multi-agent setups, and in chats with or without filesystem access.

## Get started

1. Copy `templates/ARCHITECTURE.md`, `templates/ROADMAP.md`, and `templates/PROJECT_STATE.md` into your project root, removing the `templates/` prefix. Fill in actual information; do not treat placeholders as facts.
2. Read [the specification](spec/RAP_SPECIFICATION.md), especially authority and reconciliation rules.
3. Optionally install the skill into your project from the RAP distribution:

   ```powershell
   python scripts/install_skill.py --platform cline --dest C:\development\my-project
   python scripts/install_skill.py --platform copilot --dest C:\development\my-project
   ```

   Other supported values: `codex`, `claude`, `cursor`. Use `--dry-run` to preview; use `--force` only when intentionally replacing an existing RAP skill.
4. Run the optional, read-only structural validator from within your project:

   ```powershell
   python C:\path\to\RAP\scripts\validate_rap.py --root C:\development\my-project
   ```

5. Ask your assistant to **“Use RAP to audit these documents”** or invoke `/rap` if its platform supports slash-command skill invocation.

## Skill operations

| Request | Behavior |
| --- | --- |
| `/rap audit` | Read-only report of completeness, contradictions, stale assertions, and evidence gaps |
| `/rap status` | Summarize documented current state, scope, and audit coverage; do not invent observations |
| `/rap reconcile` | Compare the three documents, and optionally implementation; propose corrections before substantive changes |
| `/rap sync` | Maintain documentation from **verified** accepted changes, subject to approval and available write access |
| `/rap init` | Offer missing document templates without overwriting existing material |
| `/rap handoff` | Audit whether another chat or agent can continue from the documents; propose missing context |

These operations are **natural-language skill instructions**, not guaranteed standalone CLI commands. A platform can expose `/rap` directly or users can request an operation conversationally.

## Authority in one sentence

**Architecture governs design; Roadmap governs approved work; Project State governs what is currently true, while remaining consistent with decisions in the other two.** When a contradiction exists, RAP reports it rather than secretly changing a decision or rewriting observed facts.

## Design properties

- One or many agents; one or many chat sessions; human contributors are equally welcome.
- Documents are canonical; the skill is a helper, never a competing authority.
- No proprietary APIs, runtime, orchestration framework, or programming language required.
- Read-only audits by default. Material decision or scope changes require owner authorization.
- Evidence provenance and audit scope must be disclosed; code, tests, and Git history provide *evidence*, not automatic authorization to change the design.
- Multi-agent concurrent writes rely on existing Git merge/review mechanisms, not a RAP lock service.

See [Chat usage](docs/CHAT_USAGE.md), [Installations](docs/INTEGRATIONS.md), and [Contributing](CONTRIBUTING.md).

## Release status

**Draft v0.1.0** — initial public proposal; feedback and improvements welcome. Markdown documents and the skill are normative only to the extent specified in `spec/RAP_SPECIFICATION.md`. The Python validator checks structure, not semantic correctness.

## License

MIT; see [LICENSE](LICENSE).
