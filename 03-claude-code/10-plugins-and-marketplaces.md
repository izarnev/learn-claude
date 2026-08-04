# 10 · Plugins and marketplaces

**What you'll learn:** how to package your Claude Code setup so it travels — to another repo, another teammate, or the world.

---

## What a plugin bundles

| Component | Directory |
|---|---|
| **Skills** | `skills/<name>/SKILL.md` |
| **Subagents** | `agents/<name>.md` |
| **Hooks** | `hooks/hooks.json` |
| **MCP servers** | `.mcp.json` |
| **Commands** | `commands/` |
| **Colour themes** | Theme files |

One install, everything configured.

---

## Installing

```bash
claude plugin install code-review@claude-plugins-official
claude plugin list                # or /plugin list in a session
```

Session-scoped loads, without installing:

```bash
claude --plugin-dir ./my-plugin
claude --plugin-dir ./a --plugin-dir ./b.zip
claude --plugin-url https://example.com/plugin.zip
```

Plugins can be loaded from directories, `.zip` archives, and URLs.

---

## Namespacing

Plugin skills are namespaced: `/my-plugin:review` rather than `/review`. Multiple plugins coexist without collision.

Precedence for subagents: managed > CLI flag > project > user > **plugin** (plugins lose to your own definitions).

---

## Plugins worth installing

**security-guidance** — Claude reviews its own code changes for vulnerabilities and fixes them in the same session. It works by running a separate model review via hooks and feeding findings back. If you ship code written with Claude, install this. See [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance).

**Code intelligence plugins** — connect a language server for your language, giving symbol-level navigation and live type errors instead of grep. Substantially better on large typed codebases and often *reduces* net context use, because a symbol lookup replaces reading three files. See [Discover plugins](https://code.claude.com/docs/en/discover-plugins#code-intelligence).

Browse the rest with `/plugin` or via [marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

---

## Building one

### Structure

```
my-team-plugin/
├── plugin.json
├── skills/
│   ├── deploy/SKILL.md
│   └── incident/SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
└── .mcp.json
```

`plugin.json` carries the metadata — name, version, description, and any dependency constraints.

### When to build

Only after the pieces have proven themselves individually:

```
correct Claude in chat
  → twice → CLAUDE.md
  → a repeated procedure → Skill
  → a second repo needs it → Plugin
  → a second team needs it → Marketplace
```

A plugin built before the skills inside it have been used for real is a plugin full of guesses.

### Dependency constraints

Declare version constraints on plugin dependencies so your plugin keeps working when an upstream plugin ships a breaking change. See [Constrain plugin dependency versions](https://code.claude.com/docs/en/plugin-dependencies).

### Recommending your plugin

Two mechanisms:

- **Plugin hints** — emit a one-line marker from your own CLI so Claude Code prompts users to install your official plugin. See [Recommend your plugin from your CLI](https://code.claude.com/docs/en/plugin-hints).
- **Relevance blocks** — add a relevance block to marketplace entries so Claude Code suggests the plugin when a user's work matches. See [Recommend plugins for your org](https://code.claude.com/docs/en/plugin-relevance).

---

## Marketplaces

A marketplace is a hosted collection of plugins. Build one to distribute across teams or the community.

```bash
claude plugin marketplace add <url-or-repo>
```

For self-hosted git, [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server) is supported as a marketplace host.

See [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).

---

## The team-onboarding path

If your goal is "a new engineer is productive on day one", the sequence is:

1. **`.claude/settings.json`** committed — permission rules, sandbox config
2. **`CLAUDE.md`** committed — conventions, commands, gotchas
3. **`.claude/rules/`** — path-scoped detail
4. **`.claude/skills/`** — your team's procedures
5. **`.mcp.json`** committed — the tools everyone needs
6. **`.claude/agents/`** — specialised reviewers
7. **A plugin**, once more than one repo needs the same thing

Claude Code also has `/team-onboarding` for packaging your setup, and a [Champion kit](https://code.claude.com/docs/en/champion-kit) and [Communications kit](https://code.claude.com/docs/en/communications-kit) for driving adoption in an organisation.

---

## Security

A plugin is broader than a skill: it can bundle hooks (arbitrary shell commands) and MCP servers (external system access).

**Before installing, enumerate:**

- Which skills? Read them.
- Which subagents, with which tools?
- Which hooks, running what commands?
- Which MCP servers, reaching what?

If you can't determine these, don't install it.

Admins can restrict MCP servers org-wide via [managed MCP](https://code.claude.com/docs/en/managed-mcp), and require an approved plugin version range in managed settings.

---

## Try it

**Exercise 1 — Install security-guidance.**
Install it. Write some deliberately vulnerable code with Claude (SQL string concatenation, say). Watch it catch itself.

**Exercise 2 — Code intelligence.**
Install one for your main language. Ask Claude to find every caller of a function. Compare against the grep-based answer.

**Exercise 3 — Audit before installing.**
Pick a plugin you're curious about. Enumerate its four component types before installing. Practise the habit.

**Exercise 4 — Build a minimal plugin.**
Package two skills you've already written into a plugin directory. Load it with `--plugin-dir`. Confirm the namespaced commands work.

**Exercise 5 — The onboarding checklist.**
Go through the seven-step list above for your main repository. Note which steps you've done. Do the next one.

---

## Checkpoint

- You have security-guidance or an equivalent review mechanism installed
- You can list what's inside a plugin before installing it
- Your main repo has at least four of the seven onboarding artifacts

---

## Going deeper

- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Constrain plugin dependency versions](https://code.claude.com/docs/en/plugin-dependencies)
- [Champion kit](https://code.claude.com/docs/en/champion-kit)
