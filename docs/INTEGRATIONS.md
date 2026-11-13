# Install RAP skill across platforms

The distribution's **canonical** skill is `skills/rap/`. The installer **copies** it to a platform-specific project skills folder so you don't need several separately maintained skill definitions. Commit the installed folder in your consuming repository if you want it available to collaborators.

| Platform | Project install location |
| --- | --- |
| Cline | `.cline/skills/rap/` |
| GitHub Copilot / VS Code | `.github/skills/rap/` |
| OpenAI Codex | `.agents/skills/rap/` |
| Claude Code | `.claude/skills/rap/` |
| Cursor | `.cursor/skills/rap/` |

```powershell
python scripts/install_skill.py --platform cline --dest C:\development\my-project --dry-run
python scripts/install_skill.py --platform cline --dest C:\development\my-project
```

The installer refuses to overwrite an existing skill directory unless `--force` is supplied. It does not install or modify the three authoritative project documents.

Some tools also support a compatible common skills location; check each platform's current documentation rather than assuming slash commands are universal. For plain chats or unsupported platforms, upload the skill Markdown and docs and ask the assistant to follow it. See `CHAT_USAGE.md`.

Platform documentation checked when drafting:
- Cline: https://github.com/cline/cline/blob/main/docs/customization/skills.mdx
- Copilot / VS Code: https://code.visualstudio.com/docs/agent-customization/agent-skills
- GitHub Copilot: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
