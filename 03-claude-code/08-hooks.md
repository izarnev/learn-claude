---
title: "Hooks"
order: 8
---

# Hooks

**What you'll learn:** how to make things happen deterministically, rather than hoping Claude remembers.

---

## Why hooks exist

Everything else in Claude Code is *context*: CLAUDE.md, skills, rules. Claude reads them and usually complies. A hook is a **shell command Claude Code runs at a fixed lifecycle point**. It always fires. No interpretation.

**The rule:** if it must happen every time, make it a hook. If Claude should decide how to apply it, make it a skill.

---

## Your first hook

Get a desktop notification whenever Claude is waiting on you. Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

Linux: `notify-send 'Claude Code' 'Claude Code needs your attention'`.

Verify with `/hooks`. The menu is read-only — edit the JSON, or ask Claude to write the hook for you.

> If nothing appears on macOS: `osascript` routes through Script Editor, which needs notification permission. Run `osascript -e 'display notification "test"'` once in Terminal, then enable **Script Editor** in System Settings → Notifications.

---

## The event lifecycle

| Event | Fires |
|---|---|
| `SessionStart` | Session begins or resumes |
| `Setup` | `--init-only`, or `--init` / `--maintenance` in `-p` mode |
| `UserPromptSubmit` | You submit a prompt, before Claude processes it |
| `UserPromptExpansion` | A typed command expands into a prompt. Can block |
| `PreToolUse` | Before a tool call. **Can block** |
| `PermissionRequest` | A tool call needs a permission decision |
| `PermissionDenied` | Denied by the auto mode classifier |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `PostToolBatch` | After a batch of parallel calls resolves |
| `Notification` | Claude Code sends a notification |
| `MessageDisplay` | While assistant text is displayed |
| `SubagentStart` / `SubagentStop` | Subagent spawned / finished |
| `TaskCreated` / `TaskCompleted` | Todo list changes |
| `Stop` | Claude finishes responding |
| `StopFailure` | Turn ends due to an API error |
| `TeammateIdle` | An agent-team teammate is about to go idle |
| `InstructionsLoaded` | A CLAUDE.md or rules file loads |
| `ConfigChange` | A config file changes during a session |
| `CwdChanged` | Working directory changes |
| `FileChanged` | A watched file changes on disk |
| `WorktreeCreate` / `WorktreeRemove` | Worktree lifecycle |
| `PreCompact` / `PostCompact` | Around context compaction |
| `Elicitation` / `ElicitationResult` | MCP server requests user input |
| `SessionEnd` | Session terminates |

---

## Hook types

| Type | What it does |
|---|---|
| `command` | Run a shell command (the default) |
| `http` | POST event data to a URL |
| `mcp_tool` | Call a tool on a connected MCP server |
| `prompt` | Single-turn LLM evaluation (Haiku by default) |
| `agent` | Multi-turn verification with tool access (experimental) |

---

## Input, output, exit codes

Claude Code passes event data as JSON on **stdin**:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/sarah/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test" }
}
```

Your script tells Claude Code what to do via **exit code**:

| Exit | Meaning |
|---|---|
| **0** | No objection. Normal flow continues. For `UserPromptSubmit`, `UserPromptExpansion` and `SessionStart`, **stdout is added to Claude's context**. |
| **2** | Block the action. **stderr becomes Claude's feedback**, so it can adjust. |
| Anything else | The action proceeds. A `<hook> hook error` notice shows the first stderr line. |

Note: exit 0 on a `PreToolUse` hook does **not** approve the call — the normal permission flow still applies.

### Structured JSON output

Exit 0 and print JSON for finer control:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

`permissionDecision` values for `PreToolUse`: `allow` (skip the prompt), `deny` (cancel and explain), `ask` (prompt normally), `defer` (non-interactive only).

Inject context on every prompt:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Current branch: release-42. Deploy freeze until Friday."
  }
}
```

> `additionalContext` must be nested inside `hookSpecificOutput`. At the top level it's silently ignored.

**Don't mix exit 2 and JSON.** Claude Code ignores JSON when you exit 2.

---

## Matchers

Without a matcher, a hook fires on every occurrence of its event.

```json
{ "matcher": "Edit|Write" }
```

What each event matches on:

| Event | Matches | Examples |
|---|---|---|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | tool name | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | how it started | `startup`, `resume`, `clear`, `compact`, `fork` |
| `SessionEnd` | why it ended | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` |
| `Notification` | type | `permission_prompt`, `idle_prompt`, `auth_success`, `agent_needs_input`, `agent_completed`, elicitation events |
| `SubagentStart` / `SubagentStop` | agent type | `general-purpose`, `Explore`, `Plan`, custom names |
| `PreCompact` / `PostCompact` | trigger | `manual`, `auto` |
| `ConfigChange` | source | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `InstructionsLoaded` | reason | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact` |
| `FileChanged` | literal filenames | `.envrc\|.env` |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `CwdChanged`, `MessageDisplay`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `TeammateIdle` | no matcher support | always fire |

MCP tools are named `mcp__<server>__<tool>`, so `mcp__github__.*` matches one server and `mcp__.*__write.*` matches write-shaped tools across servers.

### Filter by arguments with `if`

`matcher` filters by tool name. `if` uses permission rule syntax to filter by name **and arguments**, so the hook process only spawns on a match:

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "if": "Bash(git *)",
    "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-git-policy.sh"
  }]
}
```

The filter is best-effort and **fails open** when a command can't be parsed. Use the permission system, not a hook `if`, for hard enforcement. `if` works only on tool events.

---

## Recipes worth having

### Auto-format after edits

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" }]
    }]
  }
}
```

### Block edits to protected files

```bash
#!/bin/bash
# .claude/hooks/protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
for p in ".env" "package-lock.json" ".git/"; do
  if [[ "$FILE_PATH" == *"$p"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$p'" >&2
    exit 2
  fi
done
exit 0
```

`chmod +x` it, then register on `PreToolUse` with matcher `Edit|Write`.

### Re-inject context after compaction

```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "compact",
      "hooks": [{ "type": "command", "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'" }]
    }]
  }
}
```

Replace `echo` with anything dynamic — `git log --oneline -5`, for instance.

### Audit configuration changes

```json
{
  "hooks": {
    "ConfigChange": [{
      "matcher": "",
      "hooks": [{ "type": "command", "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log" }]
    }]
  }
}
```

### Reload environment on directory change (direnv)

```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "direnv export bash > \"$CLAUDE_ENV_FILE\"" }] }],
    "CwdChanged": [{ "hooks": [{ "type": "command", "command": "direnv export bash > \"$CLAUDE_ENV_FILE\"" }] }]
  }
}
```

`CLAUDE_ENV_FILE` is run as a script preamble before each Bash command.

### Log every Bash command

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt" }]
    }]
  }
}
```

---

## Prompt and agent hooks

When the decision needs judgment rather than a rule, use `type: "prompt"` — Claude Code sends the hook input to a model (Haiku by default) which returns `{"ok": true}` or `{"ok": false, "reason": "..."}`.

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
      }]
    }]
  }
}
```

On `Stop` and `SubagentStop`, `ok: false` feeds the reason back so Claude keeps working. On `PreToolUse` it denies the call; set `continueOnBlock: true` to return the reason as a tool error so Claude can adjust and continue instead of ending the turn.

When verification needs to inspect files or run commands, use `type: "agent"` — a subagent with tool access, 60s default timeout, up to 50 tool turns. `$ARGUMENTS` in the prompt is replaced with the hook's JSON input.

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{ "type": "agent", "prompt": "Verify that all unit tests pass. Run the test suite. $ARGUMENTS", "timeout": 120 }]
    }]
  }
}
```

> Agent hooks are experimental. Prefer command hooks for production.

---

## HTTP hooks

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "http",
        "url": "https://localhost:8080/hooks/tool-use",
        "headers": { "Authorization": "Bearer $MY_TOKEN" },
        "allowedEnvVars": ["MY_TOKEN"]
      }]
    }]
  }
}
```

The endpoint gets the same JSON and returns results in the response body using the same format. HTTP status codes alone can't block — return 2xx with `hookSpecificOutput`. Only variables in `allowedEnvVars` are interpolated.

---

## Where to put hooks

| Location | Scope | Shareable |
|---|---|---|
| `~/.claude/settings.json` | All your projects | No |
| `.claude/settings.json` | One project | Yes, commit it |
| `.claude/settings.local.json` | One project | No, gitignored |
| Managed policy settings | Org-wide | Admin-controlled |
| Plugin `hooks/hooks.json` | When the plugin is enabled | Bundled |
| Skill or agent frontmatter | While that component is active | In the component file |

Disable everything with `"disableAllHooks": true` — though managed-settings hooks still run unless disabled there too.

---

## Multiple hooks on one event

All matching hooks run **in parallel** and every one completes before results merge. One returning `deny` doesn't stop the others executing — don't rely on a deny to suppress another hook's side effects.

For `PreToolUse` decisions, the most restrictive wins: `deny` > `defer` > `ask` > `allow`. `additionalContext` from every hook is kept and passed together.

---

## Hooks and permission modes

**`PreToolUse` hooks fire before any permission-mode check, in every mode** — including `bypassPermissions` and `--dangerously-skip-permissions`. A hook returning `deny` blocks the tool regardless.

The reverse doesn't hold: a hook returning `allow` doesn't bypass deny rules from settings, and can't suppress prompts for connector tools your org set to `ask`.

**Hooks tighten. Never loosen.**

---

## Limitations

- Command hooks talk only through stdout/stderr/exit codes. They can't trigger `/` commands or tool calls.
- Timeouts: `command`/`http`/`mcp_tool` 10 min (30s for `UserPromptSubmit`, 10s for `MessageDisplay`); `prompt` 30s; `agent` 60s. `SessionEnd` hooks share a 1.5s budget. Override with `timeout` in seconds.
- `PostToolUse` can't undo — the tool already ran.
- `Stop` hooks fire whenever Claude finishes responding, not only at task completion, and don't fire on interrupts.
- A `Stop` hook that blocks eight times in a row gets overridden. Check `stop_hook_active` in the input and exit 0 if true. Raise the cap with `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`.
- Claude can also modify files via Bash. If a hook must see every change, add a `Stop` hook that scans the working tree, or match `Bash` and use `git status --porcelain`.
- When multiple `PreToolUse` hooks return `updatedInput`, the last to finish wins — and order is non-deterministic. Don't have two hooks rewrite the same tool's input.

---

## Debugging

```bash
# Test manually
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
echo $?

# Full execution detail
claude --debug-file /tmp/claude.log
tail -f /tmp/claude.log
```

`Ctrl+O` shows the transcript view with a line per fired hook.

Common failures:

| Symptom | Fix |
|---|---|
| Hook never runs | `/hooks` to confirm registration; matchers are case-sensitive; check you're on the right event |
| `command not found` | Use absolute paths or `${CLAUDE_PROJECT_DIR}`; or add `"args": []` for exec form |
| `jq: command not found` | Install jq, or parse with Python/Node |
| Script doesn't run at all | `chmod +x` |
| `/hooks` shows nothing | Invalid JSON (no trailing commas, no comments); wrong file location; restart to force reload |
| JSON validation failed despite valid output | Your shell profile is echoing into stdout. Wrap profile echoes in `if [[ $- == *i* ]]; then ... fi` |

---

## Try it

**Exercise 1 — Notification hook.**
Set it up. Work for an hour. This one pays for itself immediately.

**Exercise 2 — Formatter.**
Add the Prettier (or gofmt, or black) hook. Ask Claude to write badly-formatted code and watch it get fixed.

**Exercise 3 — Guardrail.**
Write a `PreToolUse` hook that blocks a command pattern you genuinely never want. Test it in `bypassPermissions` mode to confirm it still blocks.

**Exercise 4 — Context injection.**
Write a `UserPromptSubmit` hook that injects your current git branch and any deploy-freeze status via `additionalContext`.

**Exercise 5 — Prompt hook.**
Add the `Stop` prompt hook that checks whether all tasks are complete. Note how often it catches a premature stop.

**Exercise 6 — Audit trail.**
Add the Bash command logging hook. After a week, read the log. It's an accurate picture of what Claude actually does.

---

## Checkpoint

- You have at least one notification hook and one enforcement hook
- You can explain why a hook can deny in bypass mode but can't allow past a deny rule
- You know the difference between exit 2 and structured JSON output

---

## Going deeper

- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide)
- [Hooks reference](https://code.claude.com/docs/en/hooks) — full schemas, async hooks, MCP tool hooks
- [Security considerations](https://code.claude.com/docs/en/hooks#security-considerations)
- [Bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)
