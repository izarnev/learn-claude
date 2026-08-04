# 06 · Skills and slash commands

**What you'll learn:** how to package repeatable workflows so you stop retyping them, and how to control who can trigger what.

---

## Skills and commands are the same thing now

Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Existing `commands/` files keep working.

Skills add: a directory for supporting files, frontmatter to control invocation, and the ability for Claude to load them automatically when relevant.

Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, extended with invocation control, subagent execution, and dynamic context injection.

---

## When to write one

**The trigger:** you've pasted the same instructions, checklist, or multi-step procedure into chat three times. Or a section of CLAUDE.md has turned into a procedure rather than a fact.

Unlike CLAUDE.md, a skill's body loads **only when used** — so long reference material costs almost nothing until you need it.

---

## Where skills live

| Location | Scope |
|---|---|
| `.claude/skills/<name>/SKILL.md` | This project; commit it, share with the team |
| `~/.claude/skills/<name>/SKILL.md` | You, every project |
| Plugin `skills/` | Wherever the plugin is enabled; namespaced as `/plugin:skill` |
| Managed | Org-wide |

Precedence when names collide: **managed > user > project.**

---

## Minimal skill

```
.claude/skills/release/
└── SKILL.md
```

```markdown
---
name: release
description: Cut a release for this service. Use when the user asks to release, ship, cut a version, or deploy to production.
---

# Release

## Steps

1. Confirm the target version with me. Never guess.
2. Verify `main` is green: `make test lint`. If anything fails, stop and report.
3. Generate the changelog from merged PRs since the last tag. Group into
   Breaking / Added / Fixed. Breaking always first, always with a migration note.
4. Update `CHANGELOG.md`. Follow the format of the existing entries exactly.
5. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`. Do not push the tag.
6. Show me the diff and the tag. I push.

## Rules

- Never push a tag. Never deploy. Those are my actions.
- If any PR since the last tag has no changelog-worthy description, list it and
  ask rather than inventing one.
```

Notice: the boundaries (`never push`, `stop and report`, `ask rather than inventing`) do as much work as the steps.

---

## Frontmatter

| Field | What |
|---|---|
| `name` | Required. Lowercase, numbers, hyphens. Max 64 chars. Can't contain "anthropic" or "claude". |
| `description` | Required. What it does **and when to use it**. Max 1024 chars. |
| `disable-model-invocation` | `true` = only you can invoke it. Zero context cost until used. |
| `context` | `fork` runs the skill in an isolated context |
| `allowed-tools` | Restrict which tools the skill can use |
| `model` | Run this skill on a specific model |

### Control who invokes

By default, Claude sees every skill's name and description in every request and can load one when relevant.

```yaml
disable-model-invocation: true
```

Makes the skill invisible to Claude until you type `/name`. **Use this for anything with side effects** — deploys, sends, deletes. It also drops the context cost to zero.

To do the same for a skill you didn't write, set `skillOverrides` in settings rather than editing its file.

### Run in a subagent

```yaml
context: fork
```

The skill runs in isolated context and returns a summary. Use when the skill reads a lot of material you don't want in your main conversation.

---

## Bundled files and scripts

```
.claude/skills/db-migrations/
├── SKILL.md
├── SCHEMA.md              # reference, read only when needed
├── ROLLBACK.md
└── scripts/
    └── validate_migration.py
```

Reference these from SKILL.md:

```markdown
For the current schema, see SCHEMA.md.
Before finalising, run `python scripts/validate_migration.py <file>`.
```

**Scripts are cheaper and more reliable than prose.** When Claude runs `validate_migration.py`, the script's code never enters context — only its output. Compare with describing the validation logic in the skill body, which enters context *and* is executed by a model rather than deterministically.

In Claude Code, skills have **full network access** and can install packages — but should install locally, not globally, to avoid interfering with the user's machine.

---

## Built-in commands and bundled skills

Claude Code ships with a lot. The essentials:

| Command | What |
|---|---|
| `/help` | Everything available |
| `/init` | Generate a CLAUDE.md |
| `/context` | What's loaded, and its cost |
| `/memory` | View and edit memory files |
| `/clear` | Clear history |
| `/compact` | Compact manually |
| `/rewind` | Resume from before a `/clear` |
| `/resume` | Switch conversations |
| `/rename` | Rename the session |
| `/usage` | What's driving plan limits |
| `/doctor` | Diagnose configuration |
| `/config` | Set any setting from the prompt |
| `/hooks` | Browse registered hooks |
| `/mcp` | MCP server status and token cost |
| `/plugin list` | Installed plugins |
| `/login` `/logout` | Auth |
| `/desktop` | Continue this session in the Desktop app |
| `/schedule` | Create a routine |
| `/goal` | Set a completion condition |
| `/loop` | Repeat a prompt |
| `/cd` | Move the session to a new directory |
| `/debug` | Enable debug logging mid-session |

Bundled skills:

| Skill | What |
|---|---|
| `/code-review` | Review your working diff (`ultra` for the deep cloud version) |
| `/review` | Review a GitHub PR |
| `/security-review` | Security review of pending changes |
| `/debug` | Debugging workflow |
| `/batch` | Batch operations |

Full list: [Commands](https://code.claude.com/docs/en/commands).

---

## Output styles

Beyond skills, **output styles** adapt Claude Code for uses other than software engineering — changing the persona and default behaviour for a whole session. Shareable across a project.

See [Output styles](https://code.claude.com/docs/en/output-styles).

---

## Skill vs. subagent vs. CLAUDE.md

| | Skill | Subagent | CLAUDE.md |
|---|---|---|---|
| **Is** | Reusable instructions/knowledge | Isolated worker with own context | Always-on facts |
| **Loads** | On demand | On spawn | Every session |
| **Context** | Adds to your main window | Separate window; only summary returns | Every request |
| **Best for** | Reference material, invocable workflows | Tasks reading many files, parallel work | "Always do X" rules |

They compose: a subagent can preload skills via its `skills:` field; a skill can run in a subagent via `context: fork`.

---

## Try it

**Exercise 1 — Your first skill.**
Take a procedure you type regularly. Write it as `.claude/skills/<name>/SKILL.md`. Invoke it with `/<name>`. Refine over a week of use.

**Exercise 2 — Description testing.**
Write a deliberately vague description. Try five natural requests that should trigger it. Count hits. Rewrite with explicit trigger words. Retest.

**Exercise 3 — Side-effect protection.**
Write a skill that does something destructive. Add `disable-model-invocation: true`. Verify Claude won't fire it on its own.

**Exercise 4 — Script vs prose.**
Write the same validation logic two ways: described in the skill body, and as a bundled Python script. Compare reliability across ten runs.

**Exercise 5 — Fork a heavy skill.**
Write a skill that reads a lot of reference material. Run it normally, check `/context`. Add `context: fork`. Check `/context` again.

---

## Checkpoint

- You have at least one skill you actually use
- Anything with side effects has `disable-model-invocation: true`
- You know when to reach for a script instead of instructions

---

## Going deeper

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Commands](https://code.claude.com/docs/en/commands)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Output styles](https://code.claude.com/docs/en/output-styles)
- [Agent Skills open standard](https://agentskills.io)
