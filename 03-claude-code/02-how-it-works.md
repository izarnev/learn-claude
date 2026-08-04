# 02 · How Claude Code works

**What you'll learn:** the agentic loop, the built-in tools, and what's actually in your context window — the mental model that makes everything else predictable.

---

## The agentic loop

```
     ┌──────────────────────────────────────────┐
     │                                          │
     ▼                                          │
 You prompt  →  Claude reasons  →  Claude calls a tool
                                          │
                                          ▼
                              Claude Code executes it
                              (subject to permissions)
                                          │
                                          ▼
                          Result goes back into context ─┘

                    ...until Claude has nothing left to do,
                    then it responds to you.
```

That's it. Everything else — hooks, subagents, permissions, MCP — is a modification to some part of that loop:

| Extension | Where it plugs in |
|---|---|
| **CLAUDE.md** | Adds to context at session start |
| **Skills** | Adds instructions to context when triggered |
| **MCP** | Adds tools to the toolbox |
| **Permissions** | Gate between "Claude calls a tool" and "Claude Code executes it" |
| **Hooks** | Fire on lifecycle events around the loop |
| **Subagents** | Run their own copy of the loop in isolated context |

Understanding this makes the whole system predictable. When something surprises you, ask: *what's in context, what tools does it have, and what gated the call?*

---

## The built-in tools

Claude Code ships with a tool suite. The main ones:

| Tool | What |
|---|---|
| `Read` | Read a file (or an image, PDF, notebook) |
| `Write` | Create or overwrite a file |
| `Edit` | Exact string replacement in a file |
| `Glob` | Find files by pattern |
| `Grep` | Content search (ripgrep-backed) |
| `Bash` | Run shell commands |
| `WebFetch` / `WebSearch` | Read a URL / search the web |
| `Task` | Spawn a subagent |
| `TaskCreate` / `TaskUpdate` | Manage the todo list |
| `Skill` | Invoke a skill |
| `LSP` | Language-server navigation (inactive until you install a code intelligence plugin) |

Two behaviours worth knowing:

**Claude must Read a file before Editing it.** This is enforced — an Edit on an unread file fails. It prevents blind edits.

**Independent tool calls run in parallel.** Reading three files happens simultaneously, not sequentially. This is why Claude Code feels fast on exploration.

Full list: [Tools reference](https://code.claude.com/docs/en/tools-reference).

---

## What's in your context window

Run `/context` to see it. Typically:

| Component | Loaded when |
|---|---|
| System prompt | Always |
| CLAUDE.md files (managed, user, project) | Session start, in full |
| `.claude/rules/*.md` without `paths` | Session start |
| `.claude/rules/*.md` with `paths` | When Claude touches a matching file |
| Auto memory `MEMORY.md` | Session start (first 200 lines / 25KB) |
| Skill names + descriptions | Session start (~100 tokens each) |
| MCP tool names | Session start; full schemas deferred |
| Git status | Session start |
| Your conversation | Accumulating |
| File contents Claude read | When read, and forever after |

The last one is where context goes to die. A session that has read forty files carries forty files.

Anthropic ships an [interactive context window simulation](https://code.claude.com/docs/en/context-window) that's worth ten minutes.

---

## Compaction

When context approaches the limit, Claude Code **compacts**: summarises the conversation so far and continues with the summary.

What you should know:

- **Project-root CLAUDE.md survives.** After `/compact`, Claude re-reads it from disk and re-injects it.
- **Nested CLAUDE.md files in subdirectories are not re-injected** automatically — they reload next time Claude reads a file there.
- **Conversation-only instructions are lost.** If you told Claude something important in chat and it disappeared after compaction, it was never written down. Put it in CLAUDE.md.
- **`/compact` costs tokens** — it's a model call over your whole transcript.
- Compaction can be intercepted with `PreCompact` / `PostCompact` hooks, and you can re-inject context with a `SessionStart` hook using the `compact` matcher.

**Often better than compacting: starting fresh.** Current models are extremely good at rediscovering state from the filesystem. A new session that reads `progress.txt` and the git log frequently beats a compacted one.

---

## Checkpointing and rewind

Claude Code tracks file changes so you can undo. `/rewind` can also resume a conversation from before a `/clear`.

See [Checkpointing](https://code.claude.com/docs/en/checkpointing).

---

## Sessions

Conversations persist. You can:

```bash
claude -c                    # continue the most recent here
claude -r                    # interactive picker
claude -r auth-refactor      # by name
claude -n "auth-refactor"    # name a new session
claude --resume abc --fork-session   # branch instead of continuing
claude --from-pr 123         # find the session that created a PR
```

Transcripts are stored locally. `claude project purge` clears local state for a project.

---

## The `.claude` directory

Where everything lives:

```
your-project/
├── CLAUDE.md                    # or .claude/CLAUDE.md
├── CLAUDE.local.md              # personal, gitignored
└── .claude/
    ├── settings.json            # project settings (committed)
    ├── settings.local.json      # personal settings (gitignored)
    ├── rules/                   # modular instructions
    │   ├── testing.md
    │   └── api-design.md
    ├── skills/
    │   └── deploy/SKILL.md
    ├── agents/                  # custom subagents
    ├── commands/                # legacy custom commands (still work)
    └── hooks/                   # hook scripts

~/.claude/                       # user scope, all projects
├── CLAUDE.md
├── settings.json
├── skills/
├── agents/
├── rules/
└── projects/<project>/memory/   # auto memory
```

See [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory).

---

## Settings precedence

When the same setting exists at several levels:

```
managed policy  >  --settings flag  >  local  >  project  >  user
```

And feature-specific layering:

- **CLAUDE.md files are additive** — all levels contribute simultaneously
- **Skills override by name** — managed > user > project
- **Subagents override by name** — managed > CLI flag > project > user > plugin
- **MCP servers override by name** — local > project > user
- **Hooks merge** — every registered hook fires

---

## Debugging your setup

Four commands, in this order:

| Command | Answers |
|---|---|
| `/context` | What actually loaded, and what it costs |
| `/doctor` | Is my configuration broken? (also proposes CLAUDE.md trims) |
| `/hooks` | Which hooks are registered, for which events |
| `/mcp` | Which servers are connected, and their token cost |

And when nothing makes sense:

```bash
claude --safe-mode    # start with all customisations disabled
claude --debug-file /tmp/claude.log
```

`--safe-mode` disables CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands and agents, output styles, themes, keybindings, LSP, and auto-memory — while leaving auth, model selection, built-in tools and permissions working. If the problem disappears, it's one of your customisations.

---

## Try it

**Exercise 1 — Read your context.**
Run `/context` in a fresh session, note the total. Have a substantial conversation involving several file reads. Run it again. Note where the growth came from.

**Exercise 2 — Force compaction.**
Deliberately fill a context window. Watch compaction happen. Then ask about something you discussed early on. Note what survived.

**Exercise 3 — Parallel tools.**
Ask Claude to read five specific files. Watch the tool calls. They fire together.

**Exercise 4 — Safe mode.**
Run `claude --safe-mode` in a project with customisations. Note the behaviour difference. This is your first move whenever something breaks.

**Exercise 5 — Map your .claude.**
Run `ls -la .claude/` and `ls -la ~/.claude/` and identify every file. Anything you can't explain is worth reading about.

---

## Checkpoint

- You can draw the agentic loop and name where each extension plugs in
- You know what survives compaction and what doesn't
- You know the four diagnostic commands and what each one answers

---

## Going deeper

- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [Explore the context window](https://code.claude.com/docs/en/context-window) — interactive
- [Tools reference](https://code.claude.com/docs/en/tools-reference)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Manage sessions](https://code.claude.com/docs/en/sessions)
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
- [Glossary](https://code.claude.com/docs/en/glossary)
