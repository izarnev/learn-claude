---
title: "01 · Install and first session"
---

# 01 · Install and first session

**What you'll learn:** get Claude Code running and complete a real task with it.

---

## Install

### Terminal CLI (recommended starting point)

**macOS, Linux, WSL:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` in PowerShell.

Native installs **auto-update in the background**.

**Alternatives:**

```bash
brew install --cask claude-code          # stable channel, ~1 week behind
brew install --cask claude-code@latest   # latest channel
winget install Anthropic.ClaudeCode      # Windows
```

Homebrew and WinGet installs do **not** auto-update — run `brew upgrade claude-code` / `winget upgrade Anthropic.ClaudeCode` periodically. `apt`, `dnf` and `apk` are also supported.

On native Windows, [Git for Windows](https://git-scm.com/downloads/win) is recommended so Claude Code can use the Bash tool; without it, PowerShell is used as the shell. WSL doesn't need it.

Verify:

```bash
claude --version
```

### Other surfaces

| Surface | How |
|---|---|
| **VS Code / Cursor** | Search "Claude Code" in Extensions, or install from the marketplace |
| **JetBrains** | Install the Claude Code plugin; requires the CLI installed separately |
| **Desktop app** | [claude.com/download](https://claude.com/download), then the **Code** tab |
| **Web** | [claude.ai/code](https://claude.ai/code) — no local setup |
| **Mobile** | The Claude app for iOS and Android |

All surfaces share the same engine — your CLAUDE.md, settings, and MCP servers work across every one.

---

## Log in

```bash
claude
```

You'll be prompted on first use. Options:

- **Claude Pro / Max / Team / Enterprise** (recommended)
- **Claude Console** — API access with prepaid credits. A "Claude Code" workspace is created automatically for cost tracking.
- **Amazon Bedrock, Google Cloud Agent Platform, Microsoft Foundry** — enterprise cloud providers
- **A self-hosted Claude apps gateway**, if your org runs one

Later: `/login` inside a session to switch accounts, or from the shell:

```bash
claude auth login            # sign in
claude auth login --console  # use Console billing instead of a subscription
claude auth status           # check; exits 0 if logged in
claude auth logout
```

If `ANTHROPIC_API_KEY` is set, Claude Code skips the login prompt and asks you to approve the key.

---

## Your first session

```bash
cd /path/to/your/project
claude
```

You'll see the prompt with version, current model, and working directory above it.

### Start by asking, not doing

Before you let it change anything, spend five minutes getting a feel:

```
what does this project do?
what technologies does this project use?
where is the main entry point?
explain the folder structure
```

Claude reads files as needed. **You don't have to add context manually.**

You can also ask about Claude Code itself:

```
what can Claude Code do?
how do I create custom skills in Claude Code?
```

### Your first change

```
add a hello world function to the main file
```

Claude will find the file, show you the change, ask for approval (depending on your permission mode), and apply it.

### Git, conversationally

```
what files have I changed?
commit my changes with a descriptive message
create a new branch called feature/quickstart
help me resolve merge conflicts
```

---

## Permission modes — set this before you go further

Press **`Shift+Tab`** to cycle modes. This is the most important control in the product.

| Mode | Behaviour |
|---|---|
| `default` (Manual) | Asks before each change |
| `acceptEdits` | Auto-approves file edits, still asks about commands |
| `plan` | Claude proposes without editing anything |
| `auto` | Runs a background safety classifier and blocks risky actions; returns to prompting after repeated blocks |
| `dontAsk` | Fewer prompts |
| `bypassPermissions` | No prompts at all |

Start in `default`. Move to `acceptEdits` once you trust it on a given repo. Use `plan` for anything you want to review before it happens. Covered in depth in [module 04](04-permissions-and-safety.md).

---

## The commands you'll use every day

**From the shell:**

| Command | What |
|---|---|
| `claude` | Start interactive |
| `claude "task"` | Start with an initial prompt |
| `claude -p "query"` | One-off query, print, exit |
| `claude -c` | Continue the most recent conversation here |
| `claude -r` | Resume — picker, or by ID/name |
| `claude -n "name"` | Name the session |
| `claude --model opus` | Set the model |
| `claude -w feature-x` | Start in an isolated git worktree |

**Inside a session:**

| Command | What |
|---|---|
| `/help` | All commands |
| `/clear` | Clear conversation history |
| `/context` | See what's loaded and what it costs |
| `/init` | Generate a CLAUDE.md for this project |
| `/memory` | View and edit memory files |
| `/usage` | What's driving your plan limits |
| `/doctor` | Diagnose configuration problems |
| `/resume` | Switch conversations |
| `/exit` | Quit (or Ctrl+D twice) |

Type `/` to see everything. Tab completes. `↑` gives history. `Ctrl+R` searches command history across every project.

---

## Six habits worth forming immediately

1. **Be specific.** "Fix the login bug where users see a blank screen after entering wrong credentials" beats "fix the bug."
2. **Break big tasks into numbered steps.** Claude follows explicit sequences reliably.
3. **Let it explore first.** "Analyse the database schema" before "add a migration."
4. **Use plan mode for anything risky.** Read the plan, then approve.
5. **Run `/context` when things feel off.** Usually the answer is visible there.
6. **Start a new session per task.** `/clear` is cheap; a polluted context is not.

---

## Try it

**Exercise 1 — Orientation.**
Point Claude Code at a codebase you know well. Ask it to explain the architecture. Grade the answer. This calibrates how much to trust it on a codebase you *don't* know.

**Exercise 2 — Plan mode.**
`Shift+Tab` to plan mode. Ask for a non-trivial feature. Read the plan. Note what it got wrong before writing any code — this is the mode's entire value.

**Exercise 3 — Full loop.**
Have Claude write a small feature, write tests for it, run the tests, fix failures, and commit. One task, one session.

**Exercise 4 — Pipe something in.**
```bash
tail -200 app.log | claude -p "summarise any errors and their likely causes"
```

**Exercise 5 — Name and resume.**
Start a named session (`claude -n auth-work`), do some work, exit, and resume it (`claude -r auth-work`).

---

## Checkpoint

- Claude Code is installed and you're logged in
- You know how to cycle permission modes and which one you're in
- You've completed a change → test → commit loop
- You know `/context`, `/clear`, and `/init`

---

## Going deeper

- [Quickstart](https://code.claude.com/docs/en/quickstart)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Commands](https://code.claude.com/docs/en/commands)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [Advanced setup](https://code.claude.com/docs/en/setup)
- [Troubleshoot installation and login](https://code.claude.com/docs/en/troubleshoot-install)
