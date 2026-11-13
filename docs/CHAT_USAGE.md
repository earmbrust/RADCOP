# RADCOP in ordinary chats

RADCOP does not require an autonomous coding agent. The skill can operate through a native `/radcop` command when supported, or as a file uploaded to any conversational assistant.

## Chat without a repository connector

Provide `skills/radcop/SKILL.md` (and `references/AUDIT_GUIDE.md` if necessary) and whichever of the three documents you want audited. Example:

> Follow the attached RADCOP skill. Audit the attached ARCHITECTURE.md, ROADMAP.md, and PROJECT_STATE.md for inconsistencies. Do not claim to have inspected the implementation. Produce proposed corrections, not silent decision changes.

In this mode the assistant may perform a document-level consistency audit and draft updates; it cannot verify local source, builds, Git history, or tests without those materials.

## Chat with repository/file access

Ask for a RADCOP audit of the repository's three authoritative root documents. A capable assistant can optionally reconcile claims to code or Git evidence, report coverage, and make *authorized* documentation edits if file-write functionality exists.

## Conversation-to-agent handoff

A chat can propose an architecture or roadmap change. Only an approved change becomes authoritative in the corresponding document. Implementation agents consume those documents, and PROJECT_STATE records actual implementation and test evidence. A handoff is still possible when one participant has no memory of previous messages.

## Example prompts

- “Use RADCOP to audit these three documents. Report discrepancies without editing.”
- “Use RADCOP to reconcile PROJECT_STATE against approved architecture and roadmap; suggest patches.”
- “Use RADCOP to check whether the documents provide enough continuity for a new chat.”
- “Use RADCOP to update state for this verified commit, but do not change design decisions.”

`/radcop` is a naming convention supported as a direct slash command only on platforms that expose skills that way.

## Long-term project state

For long-running projects, ask “Use RADCOP to audit the current-state snapshot and historical references” or “Propose an archive plan without editing.” Chat assistants with only the three roots can check internal consistency, but MUST mark file existence, Git revisions, and repository evidence `NOT_CHECKED` unless independently accessible. Archive proposals must preserve accepted requirements and active blockers in their owning roots.
