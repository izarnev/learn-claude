---
title: "Claude Code cheat sheet"
order: 4
---

# Claude Code cheat sheet

*Verify against the [CLI reference](https://code.claude.com/docs/en/cli-reference) — this ships weekly.*

---

## Install

```bash
curl -fsSL https://claude.ai/install.sh | bash     # macOS / Linux / WSL
irm https://claude.ai/install.ps1 | iex             # Windows PowerShell
brew install --cask claude-code                     # stable channel
brew install --cask claude-code@latest              # latest channel
winget install Anthropic.ClaudeCode
claude --version
```

Native installs auto-update. Homebrew and WinGet do not.

---

## Shell commands

| Command | What |
|---|---|
| `claude` | Interactive session |
| `claude "task"` | Interactive, with an initial prompt |
| `claude -p "query"` | Print and exit |
| `cat f \| claude -p "q"` | Pipe content in |
| `claude -c` | Continue the most recent here |
| `claude -r [id\|name]` | Resume — picker or direct |
| `claude -n "name"` | Name the session |
| `claude update` | Update |
| `claude install [version]` | Install a specific version |
| `claude auth login\|logout\|status` | Auth |
| `claude setup-token` | Long-lived OAuth token for CI |
| `claude doctor` | Read-only diagnostics from the shell |
| `claude mcp` | Manage MCP servers |
| `claude mcp login\|logout <name>` | MCP OAuth from the shell |
| `claude plugin` | Manage plugins |
| `claude agents` | Agent view dashboard |
| `claude attach\|logs\|stop\|respawn\|rm <id>` | Background session control |
| `claude daemon status\|stop` | Supervisor control |
| `claude project purge [path]` | Delete local state for a project |
| `claude remote-control` | Remote Control server |
| `claude ultrareview [target]` | Non-interactive deep review |
| `claude gateway --config gateway.yaml` | Self-hosted gateway |

---

## Key flags

**Model and effort**

```bash
--model sonnet|opus|haiku|fable|<full-id>
--effort low|medium|high|xhigh|max|ultracode
--fallback-model sonnet,haiku
--advisor opus|sonnet
```

**Permissions and tools**

```bash
--permission-mode default|acceptEdits|plan|auto|dontAsk|bypassPermissions|manual
--allowedTools "Bash(git log *)" "Read"
--disallowedTools "Edit" "mcp__*"
--tools "Bash,Edit,Read"
--dangerously-skip-permissions
--allow-dangerously-skip-permissions
```

**Print mode**

```bash
-p / --print
--output-format text|json|stream-json
--input-format text|stream-json
--json-schema '{...}'
--max-turns N
--max-budget-usd N
--verbose
--include-partial-messages
--forward-subagent-text
--no-session-persistence
```

**System prompt**

```bash
--append-system-prompt "text"
--append-system-prompt-file ./file
--system-prompt "text"           # replaces everything
--system-prompt-file ./file      # replaces everything
--append-subagent-system-prompt "text"
--exclude-dynamic-system-prompt-sections
```

**Config and startup**

```bash
--add-dir ../lib ../apps
--settings ./settings.json
--setting-sources user,project,local
--mcp-config ./mcp.json
--strict-mcp-config
--plugin-dir ./plugin
--plugin-url https://...
--agents '{"name":{"description":"...","prompt":"..."}}'
--agent my-agent
--bare                            # skip all auto-discovery; fast
--safe-mode                       # all customisations disabled
--debug "api,mcp"
--debug-file /tmp/claude.log
```

**Sessions and surfaces**

```bash
-w, --worktree [name|#PR]
--tmux
--bg, --background
--exec 'pytest -x'
--fork-session
--session-id <uuid>
--from-pr 123
--cloud "task"
--teleport
--remote-control ["name"]
--ide
--chrome / --no-chrome
--teammate-mode in-process|auto|tmux|iterm2
```

---

## Session commands

| Command | What |
|---|---|
| `/help` | Everything |
| `/init` | Generate CLAUDE.md |
| `/context` | What's loaded and its cost |
| `/memory` | View and edit memory files |
| `/usage` | What's driving plan limits |
| `/doctor` | Diagnose config; propose CLAUDE.md trims |
| `/config` | Set any setting |
| `/hooks` | Browse registered hooks (read-only) |
| `/mcp` | Server status and token cost |
| `/plugin list` | Installed plugins |
| `/clear` | Clear history |
| `/compact` | Compact manually |
| `/rewind` | Resume from before a `/clear` |
| `/resume` `/rename` | Session management |
| `/model` | Change model |
| `/login` `/logout` | Auth |
| `/desktop` | Continue in the Desktop app |
| `/cd` | Move to a new directory |
| `/schedule` | Create a routine |
| `/goal` | Set a completion condition |
| `/loop` | Repeat a prompt |
| `/debug` | Enable debug logging |
| `/code-review [ultra]` | Review the working diff |
| `/review` | Review a GitHub PR |
| `/security-review` | Security review of pending changes |
| `/exit` | Quit |

**Keys:** `Shift+Tab` cycles permission modes · `Ctrl+O` transcript view · `Ctrl+R` search command history across projects · `↑` history · Tab completes

---

## File layout

```
project/
├── CLAUDE.md                 # or .claude/CLAUDE.md
├── CLAUDE.local.md           # personal, gitignore it
├── .mcp.json                 # project MCP servers
└── .claude/
    ├── settings.json         # committed
    ├── settings.local.json   # gitignored
    ├── rules/*.md            # modular, optionally path-scoped
    ├── skills/<name>/SKILL.md
    ├── agents/<name>.md
    ├── commands/*.md         # legacy; still works
    └── hooks/*.sh

~/.claude/
├── CLAUDE.md
├── settings.json
├── rules/ skills/ agents/
└── projects/<project>/memory/MEMORY.md
```

**Precedence:** managed policy > `--settings` > local > project > user

- CLAUDE.md files: **additive**, all levels
- Skills: managed > user > project
- Subagents: managed > CLI flag > project > user > plugin
- MCP: local > project > user
- Hooks: **all merge**

---

## Settings essentials

```json
{
  "model": "sonnet",
  "fallbackModel": "haiku",
  "effortLevel": "medium",
  "autoMemoryEnabled": true,
  "sandbox": { "enabled": true },
  "permissions": {
    "deny": ["Read(.env)", "Read(**/*.pem)", "Bash(rm -rf /*)", "Bash(git push --force*)"],
    "ask":  ["Bash(git push*)", "Bash(npm publish*)"],
    "allow":["Read", "Grep", "Glob", "Bash(git status)", "Bash(git diff*)", "Bash(npm test*)"],
    "additionalDirectories": ["../shared-lib"]
  },
  "claudeMdExcludes": ["**/other-team/CLAUDE.md"],
  "hooks": { }
}
```

---

## Hook events

`SessionStart` `Setup` `UserPromptSubmit` `UserPromptExpansion` `PreToolUse` `PermissionRequest` `PermissionDenied` `PostToolUse` `PostToolUseFailure` `PostToolBatch` `Notification` `MessageDisplay` `SubagentStart` `SubagentStop` `TaskCreated` `TaskCompleted` `Stop` `StopFailure` `TeammateIdle` `InstructionsLoaded` `ConfigChange` `CwdChanged` `FileChanged` `WorktreeCreate` `WorktreeRemove` `PreCompact` `PostCompact` `Elicitation` `ElicitationResult` `SessionEnd`

**Types:** `command` `http` `mcp_tool` `prompt` `agent`

**Exit codes:** `0` no objection (stdout enters context for `UserPromptSubmit` / `UserPromptExpansion` / `SessionStart`) · `2` block, stderr becomes Claude's feedback · other = proceed with an error notice

**`PreToolUse` hooks fire in every permission mode including bypass.** Hooks tighten; they never loosen.

---

## Skill frontmatter

```yaml
---
name: my-skill                      # lowercase, hyphens, ≤64 chars
description: What it does. Use when [triggers].   # ≤1024 chars
disable-model-invocation: true      # only you can invoke; zero context cost
context: fork                       # run in an isolated subagent
allowed-tools: Read, Grep
model: haiku
---
```

## Subagent frontmatter

```yaml
---
name: test-auditor
description: When Claude should use it
tools: Read, Grep, Glob, Bash
model: sonnet
skills: [testing-conventions]
memory: true
---
```

## Path-scoped rule

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.{ts,tsx}"
---
```

---

## Diagnostics, in order

```
/context      what actually loaded
/doctor       is the config broken
/hooks        which hooks are registered
/mcp          server status and cost
claude --safe-mode
claude --debug-file /tmp/claude.log
```
