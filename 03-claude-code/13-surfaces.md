---
title: "13 · Surfaces: desktop, web, IDE, Slack"
---

# 13 · Surfaces: desktop, web, IDE, Slack

**What you'll learn:** where else Claude Code runs, and how to move a session between surfaces mid-task.

---

## Every surface shares one engine

Your `CLAUDE.md`, settings, skills and MCP servers work identically on all of them. Picking a surface is about ergonomics, not capability.

| Surface | Strength | Weakness |
|---|---|---|
| **Terminal CLI** | Full-featured, scriptable, composable | Text-only diffs |
| **VS Code / Cursor** | Inline diffs, @-mentions, plan review, history in the editor | Tied to the editor |
| **JetBrains** | Interactive diffs, selection context | Requires the CLI installed too |
| **Desktop app** | Visual diff review, parallel sessions with git isolation, integrated terminal and editor, side chats, PR monitoring, computer use | Heavier |
| **Web** (`claude.ai/code`) | No local setup, long-running cloud tasks, repos you don't have locally | Sandbox constraints |
| **Mobile** | Kick off and check in from anywhere | Not for real editing |
| **Slack** | Bug report in, PR out | Async |
| **CI** (GitHub Actions, GitLab) | Automation | No interactivity |
| **Chrome** | Debugging live web apps | Browser only |

---

## Desktop app

Beyond the basics:

- **Parallel sessions with git isolation** — several tasks at once, each in its own worktree
- **Drag-and-drop pane layout** — arrange sessions how you want
- **Integrated terminal and file editor**
- **Side chats** — ask a question without polluting the main session
- **Visual diff review** — the main reason people switch from the terminal
- **App previews** — see the thing you're building
- **PR monitoring**
- **Computer use** — Claude can control your desktop
- **Connectors**
- **Dispatch** — message Claude a task from your phone, open the session it creates on desktop
- **Scheduled tasks** — run on your machine with local file access

Linux is available in beta.

---

## Claude Code on the web

Runs in Anthropic's cloud sandbox. Configure setup scripts, network access, and Docker.

Good for: long-running tasks you kick off and check later, repos you don't have cloned, parallel tasks, working from a machine that isn't yours.

```bash
claude --cloud "Fix the login bug"   # start a web session from your terminal
claude --teleport                     # pull a web session into your terminal
```

Teleport requires a claude.ai subscription.

---

## Moving between surfaces

This is the part people don't know exists.

| Want | Do |
|---|---|
| Continue a local session from your phone or any browser | [Remote Control](https://code.claude.com/docs/en/remote-control) — `claude --remote-control` |
| Continue the current terminal session in Desktop | `/desktop` (needs a claude.ai subscription; macOS and x64 Windows) |
| Start locally, continue on mobile | `claude --cloud`, then the Claude mobile app |
| Pull a web or mobile session into your terminal | `claude --teleport` |
| Message Claude a task from your phone | Dispatch, then open the Desktop session it creates |
| Push events from Telegram, Discord, iMessage or webhooks into a session | [Channels](https://code.claude.com/docs/en/channels) |

The pattern: **start where it's convenient, finish where it's appropriate.** Kick off a long refactor from your phone on the train, review the diff on desktop when you're at your machine.

---

## VS Code

Inline diffs, `@`-mentions to reference files, plan review, and conversation history in the editor.

Install: search "Claude Code" in Extensions, or the direct links for [VS Code](vscode:extension/anthropic.claude-code) and [Cursor](cursor:extension/anthropic.claude-code). Then Command Palette → "Claude Code" → **Open in New Tab**.

Connect the CLI to a running IDE with `claude --ide`.

VS Code also supports third-party providers.

---

## JetBrains

IntelliJ, PyCharm, WebStorm and others. Install the plugin from the Marketplace and restart. **Requires the Claude Code CLI installed separately.**

---

## Slack

Mention `@Claude` with a bug report and get a pull request back. Setup via `/install-slack-app`.

The value: non-engineers can file work that turns into code without leaving Slack, and the thread context comes along automatically.

---

## Chrome

```bash
claude --chrome
claude --no-chrome
```

Test web apps, debug with console logs, automate form filling, extract data. The debugging use is the strongest — Claude can read the console and network tab while changing the code.

---

## Terminal configuration

Worth ten minutes if you live in the CLI:

- **`Shift+Enter` for newlines** — needs terminal-specific setup
- **Terminal bell** when Claude finishes
- **tmux** configuration
- **Colour theme** matching, plus custom themes shippable in plugins
- **Vim mode**
- **Fullscreen rendering** — flicker-free, mouse support, stable memory in long conversations
- **Custom keybindings** via a keybindings file
- **Custom status line** — context usage, cost, git status
- **Voice dictation** — hold-to-record or tap-to-record

See [Configure your terminal](https://code.claude.com/docs/en/terminal-config), [Keybindings](https://code.claude.com/docs/en/keybindings), [Statusline](https://code.claude.com/docs/en/statusline), [Fullscreen](https://code.claude.com/docs/en/fullscreen), [Voice dictation](https://code.claude.com/docs/en/voice-dictation).

---

## Artifacts

Publish session output as a live, interactive page at a private URL you can share inside your organisation. Good for incident timelines that update as Claude investigates, or any output you'd rather see visually than as terminal text.

See [Share session output as artifacts](https://code.claude.com/docs/en/artifacts).

---

## Choosing

A practical default:

- **Terminal** for daily work and anything scripted
- **Desktop** for reviewing large diffs and running parallel sessions
- **Web** for long tasks you'll check later
- **Mobile** for kicking things off and answering Claude's questions
- **CI** for anything that should happen without you

---

## Try it

**Exercise 1 — Desktop diff review.**
Do a multi-file change in Desktop. Review the diff visually. Compare against reviewing the same change in the terminal.

**Exercise 2 — Teleport.**
Start a task with `claude --cloud`, check it on your phone, then `claude --teleport` it into your terminal.

**Exercise 3 — Remote control.**
Start `claude --remote-control` locally, then drive it from claude.ai. Useful the first time you're away from your desk mid-task.

**Exercise 4 — Status line.**
Configure a status line showing context usage and cost. You'll notice cost problems much earlier.

**Exercise 5 — Pick your two.**
Try four surfaces on the same task. Choose the two you'll actually use and configure them properly.

---

## Checkpoint

- You've used at least two surfaces on real work
- You know how to move a session between surfaces
- Your primary surface is configured (status line, keybindings, or theme)

---

## Going deeper

- [Platforms and integrations](https://code.claude.com/docs/en/platforms)
- [Desktop application](https://code.claude.com/docs/en/desktop)
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [Remote Control](https://code.claude.com/docs/en/remote-control)
- [VS Code](https://code.claude.com/docs/en/vs-code) · [JetBrains](https://code.claude.com/docs/en/jetbrains)
- [Slack](https://code.claude.com/docs/en/slack) · [Chrome](https://code.claude.com/docs/en/chrome)
- [Mobile](https://code.claude.com/docs/en/mobile)
- [Feature availability across plans and providers](https://code.claude.com/docs/en/feature-availability)
