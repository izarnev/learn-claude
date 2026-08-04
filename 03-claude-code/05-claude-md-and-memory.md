---
title: "05 · CLAUDE.md, rules, and memory"
---

# 05 · CLAUDE.md, rules, and memory

**What you'll learn:** how to give Claude persistent knowledge about your project, and why most CLAUDE.md files are too long to work.

---

## Two memory systems

| | CLAUDE.md | Auto memory |
|---|---|---|
| **Written by** | You | Claude |
| **Contains** | Instructions and rules | Learnings and patterns it discovers |
| **Scope** | Project, user, or org | Per repository, shared across worktrees |
| **Loaded** | Every session, in full | Every session (first 200 lines / 25KB of `MEMORY.md`) |
| **Use for** | Standards, workflows, architecture | Build commands, debugging insights, preferences |

Both are **context, not enforced configuration**. To make something hold regardless of what Claude decides, use a hook.

---

## CLAUDE.md locations

Listed in load order, broadest to most specific:

| Scope | Location | Shared with |
|---|---|---|
| **Managed policy** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux/WSL: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Everyone in the org |
| **User** | `~/.claude/CLAUDE.md` | Just you, all projects |
| **Project** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Your team, via git |
| **Local** | `./CLAUDE.local.md` (gitignore it) | Just you, this project |

### How they load

Claude Code walks **up** the directory tree from your working directory, collecting `CLAUDE.md` and `CLAUDE.local.md` at each level. All discovered files are **concatenated, not overridden**. Root-to-working-directory order, so more specific instructions are read last. Within a directory, `CLAUDE.local.md` comes after `CLAUDE.md`.

Files in **subdirectories** below your working directory load on demand, when Claude reads files there.

---

## Write it well: the four rules

### 1. Size — under 200 lines

This is the rule everyone breaks. Longer files consume more context **and reduce adherence**. A 600-line CLAUDE.md is worse than a 150-line one, not better.

If yours is growing, move content to [rules](#rules) or [skills](06-skills-and-commands.md).

`/doctor` proposes trims: it cuts what Claude can derive from the codebase (directory layouts, dependency lists, architecture overviews) and keeps pitfalls, rationale, and conventions that differ from tool defaults. That's the right instinct — **CLAUDE.md is for what Claude can't work out on its own.**

### 2. Specificity — write things you could verify

| Vague | Concrete |
|---|---|
| Format code properly | Use 2-space indentation |
| Test your changes | Run `npm test` before committing |
| Keep files organised | API handlers live in `src/api/handlers/` |

### 3. Structure — headers and bullets

Claude scans structure the way readers do. Organised sections beat dense paragraphs.

### 4. Consistency — no contradictions

If two rules conflict, Claude may pick one arbitrarily. Review periodically, including nested CLAUDE.md files and rules.

---

## What to actually put in it

The trigger for adding something:

- Claude made the same mistake twice
- A code review caught something Claude should have known
- You typed the same correction you typed last session
- A new teammate would need this context

A good project CLAUDE.md:

```markdown
# Ledger — payments service

## Commands
- `make dev` — run locally (needs Docker)
- `make test` — full suite; must pass before commit
- `make test-fast` — unit tests only
- `make lint` — golangci-lint; CI fails on any warning

## Architecture
- `cmd/` — entrypoints. `internal/` — everything else, not importable.
- HTTP handlers in `internal/api/`, business logic in `internal/domain/`.
  Handlers never contain business logic.
- All money is `int64` minor units. Never float. Never `decimal`.

## Conventions
- Errors wrap with `fmt.Errorf("...: %w", err)`. Never bare returns.
- Every exported function has a doc comment starting with its name.
- Migrations are append-only. Never edit a committed migration.

## Gotchas
- The `payments` table has a partial unique index that doesn't show in the
  schema dump. Check `migrations/0043` before adding constraints.
- `TestWebhookRetry` is flaky under `-race`. Known; don't "fix" it.
- We're on Go 1.22. `slices.Sorted` is not available.

## Before committing
Run `make test lint`. Both must pass.
```

Notice: no directory listing, no dependency list, no explanation of what Go is. Every line is something Claude would otherwise get wrong.

### Generate a starting point

```
/init
```

Claude analyses the codebase and writes a CLAUDE.md with build commands, test instructions and conventions it discovers. If one already exists, `/init` suggests improvements rather than overwriting.

`/init` also reads Cursor rules (`.cursor/rules/`, `.cursorrules`) and Copilot instructions (`.github/copilot-instructions.md`). Set `CLAUDE_CODE_NEW_INIT=1` for an interactive multi-phase flow that also reads `AGENTS.md`, `.devin/rules/`, `.windsurf/rules/`, and `.clinerules`, and asks which artifacts to set up.

---

## Imports

```markdown
See @README for project overview and @package.json for available commands.

# Additional instructions
- git workflow @docs/git-instructions.md
```

Relative and absolute paths both work; relative resolves against the *file containing the import*. Max depth: four hops.

**Imports don't save context** — imported files load in full at launch. They're for organisation, not economy.

To mention a path without importing it, wrap it in backticks: `` `@README` `` stays literal.

**External imports** — paths resolving outside your working directory, like `@~/.claude/my-notes.md` — trigger an approval dialog the first time. This protects you from files other people commit to a shared project. User-scope imports don't prompt.

### AGENTS.md

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repo already has one:

```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
```

Or symlink: `ln -s AGENTS.md CLAUDE.md` (needs admin or Developer Mode on Windows — use the import instead there).

---

## Rules

For larger projects, split instructions into `.claude/rules/`:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    ├── testing.md
    └── security.md
```

All `.md` files are discovered recursively. Rules without `paths` frontmatter load at launch with the same priority as `.claude/CLAUDE.md`.

### Path-scoped rules — the context saver

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---

# API development rules

- All endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments
```

These load **only when Claude touches a matching file.** This is the main tool for keeping a large instruction set from consuming context on every session.

Patterns:

| Pattern | Matches |
|---|---|
| `**/*.ts` | All TypeScript files anywhere |
| `src/**/*` | Everything under `src/` |
| `*.md` | Markdown in the project root |
| `src/**/*.{ts,tsx}` | Brace expansion works |

Brace expansion is bounded: a rule's whole `paths` list shares a budget of 1,000 expanded patterns and 4 MiB. Patterns exceeding it are used unexpanded and match nothing.

Glob treats `[` as a bracket expression — escape a literal one as `photos \[2024/**`.

### Sharing rules

`.claude/rules/` supports symlinks, so you can maintain one shared set:

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

User-level rules live in `~/.claude/rules/` and load before project rules, giving project rules higher priority.

---

## Auto memory

Claude writes notes to itself as it works — build commands, debugging insights, architecture notes, preferences. It decides what's worth remembering.

On by default. Toggle via `/memory`, or:

```json
{ "autoMemoryEnabled": false }
```

Or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Where it lives

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # concise index, loaded every session
├── debugging.md       # detail, loaded on demand
└── api-conventions.md
```

`<project>` derives from the git repository, so all worktrees and subdirectories share one memory directory. Machine-local; not shared across machines.

Change the location with `autoMemoryDirectory` in settings (absolute path or `~/`-prefixed; requires accepting the workspace trust dialog when set at project scope).

### How it works

Only the first **200 lines or 25KB** of `MEMORY.md` loads at session start. Claude Code enforces this actively — if the file gets near a limit it reminds Claude to shorten it; if it goes over, the write succeeds but Claude Code returns an error telling Claude to rewrite the index, because everything past the limit is dropped on the next load.

Topic files aren't loaded at startup. Claude reads them on demand.

Frontmatter and block-level HTML comments are stripped before loading, so they don't count toward the limits. Claude Code records a `modified` ISO 8601 timestamp in frontmatter when it writes a memory file that has frontmatter.

Subagents don't inherit the main conversation's auto memory (except forks). A subagent can have its own, via the `memory` field.

### Auditing it

Run `/memory` and open the auto memory folder. It's plain markdown — read it, edit it, delete it. Do this occasionally; stale learnings are actively harmful.

---

## `/memory` and `/context`

- **`/memory`** lists CLAUDE.md, CLAUDE.local.md and other memory locations across scopes (including files that don't exist yet — selecting one creates it). Toggles auto memory. Opens files in your editor.
- **`/context`** shows what actually loaded **into this session**. This is the one you use to debug.

---

## Troubleshooting

**"Claude isn't following my CLAUDE.md."**

CLAUDE.md is delivered as a user message after the system prompt, not as part of it. There's no strict compliance guarantee.

1. Run `/context` and check **Memory files**. If it's not listed, Claude can't see it.
2. Check the file is in a loaded location.
3. Make instructions more specific.
4. Look for conflicting instructions across files.
5. If it must happen at a specific point, make it a [hook](08-hooks.md).

For system-prompt-level instructions, `--append-system-prompt` works but must be passed every invocation — better for scripts than interactive use.

`InstructionsLoaded` hooks log exactly which instruction files loaded, when, and why. Useful for debugging path-scoped rules.

**"Instructions disappeared after `/compact`."**

Project-root CLAUDE.md is re-read from disk and re-injected after compaction. Nested subdirectory CLAUDE.md files are not — they reload next time Claude reads a file there. If something vanished, it was conversation-only. Write it down.

**Monorepos.** Use `claudeMdExcludes` to skip other teams' files:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Patterns match absolute paths. Arrays merge across settings layers. Managed policy CLAUDE.md cannot be excluded.

---

## Org-wide CLAUDE.md

Deploy a file at the managed policy path via MDM, Group Policy or Ansible. Or put the content inline in `managed-settings.json`:

```json
{ "claudeMd": "Always run `make lint` before committing.\nNever push directly to main." }
```

Honoured only in managed and policy settings. Loads before user and project CLAUDE.md, and can't be excluded.

**Use managed settings for enforcement, managed CLAUDE.md for guidance.** Settings are enforced by the client; CLAUDE.md shapes behaviour.

---

## Try it

**Exercise 1 — `/init` then edit.**
Run `/init` on a real project. Then delete everything Claude could work out by reading the code. What's left is the real CLAUDE.md. Count the lines — it should be well under 200.

**Exercise 2 — The gotchas section.**
Add a `## Gotchas` section listing three things about your codebase that are genuinely surprising. This is usually the highest-value part of the file.

**Exercise 3 — Path-scoped rule.**
Move your language-specific or directory-specific instructions into a rule with `paths` frontmatter. Verify with `/context` that it doesn't load until Claude touches a matching file.

**Exercise 4 — Audit auto memory.**
`/memory` → auto memory folder. Read every line. Delete what's wrong or stale. Note what Claude learned that you'd never have thought to write down.

**Exercise 5 — Prove the load order.**
Put a distinctive instruction in `~/.claude/CLAUDE.md` and a contradicting one in your project's. See which wins. Then use `/context` to confirm both loaded.

---

## Checkpoint

- Your main project's CLAUDE.md is under 200 lines and contains nothing derivable from the code
- You've moved at least one thing into a path-scoped rule
- You've read your auto memory at least once

---

## Going deeper

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview) — when to use CLAUDE.md vs rules vs skills
- [Set up Claude Code in a monorepo](https://code.claude.com/docs/en/large-codebases)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
