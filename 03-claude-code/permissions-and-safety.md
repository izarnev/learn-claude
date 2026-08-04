---
title: "Permissions, sandboxing, and safety"
order: 4
---

# Permissions, sandboxing, and safety

**What you'll learn:** exactly what Claude Code can and can't do, how to constrain it, and what "enforcement" means versus "instruction".

---

## The single most important distinction

**An instruction is a request. A permission rule is enforcement.**

Writing "never edit `.env`" in CLAUDE.md is a request Claude will usually honour. Adding a deny rule, or a `PreToolUse` hook that blocks it, is a guarantee.

If a rule *must* hold every time — compliance, secrets, production — it belongs in permissions or hooks, not in prose.

---

## Permission modes

Cycle with `Shift+Tab`. Set at launch with `--permission-mode`.

| Mode | Behaviour | When |
|---|---|---|
| `default` / `manual` | Asks before each file change and command | Learning a repo; anything unfamiliar |
| `acceptEdits` | Auto-approves file edits; still asks about commands | Repos you trust, work you'll review in the diff |
| `plan` | Proposes without editing | Anything you want to review before it happens |
| `auto` | Background safety classifier evaluates each action and blocks risky ones; falls back to prompting after repeated blocks | Long autonomous sessions |
| `dontAsk` | Fewer prompts | Narrow, well-understood tasks |
| `bypassPermissions` | No prompts | Isolated sandboxes only |

`--dangerously-skip-permissions` is equivalent to `--permission-mode bypassPermissions`. `--allow-dangerously-skip-permissions` adds it to the `Shift+Tab` cycle without starting in it.

### Auto mode

Auto mode runs a classifier over each proposed action against a configurable rule set. It's the practical middle ground for long sessions: you're not approving every `ls`, but destructive and exfiltration-shaped actions still get stopped.

You can tell it what your organisation trusts:

```bash
claude auto-mode defaults              # print the built-in rules as JSON
claude auto-mode config                # your effective config
claude auto-mode reset                 # restore defaults
```

Configure repos, buckets and domains you trust, override the default block/allow rules, and add hard deny rules that apply unconditionally. See [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config).

---

## Permission rules

Fine-grained control in settings. Rule syntax is `Tool(pattern)`.

```json
{
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(npm test)",
      "Read"
    ],
    "deny": [
      "Read(.env)",
      "Read(**/*.pem)",
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Edit(.github/workflows/**)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(npm publish *)"
    ],
    "additionalDirectories": ["../shared-lib"]
  }
}
```

Precedence: **deny > ask > allow.** A deny rule at any settings scope, including managed policy, always wins — including over a hook returning `allow`.

Rules can also be set per-invocation:

```bash
claude --allowedTools "Bash(git log *)" "Read"
claude --disallowedTools "Edit" "mcp__*"
claude --tools "Bash,Edit,Read"          # restrict which built-in tools exist at all
```

Note the difference: `--disallowedTools "Edit"` (a bare tool name) **removes the tool from Claude's context entirely**. `--disallowedTools "Bash(rm *)"` (a scoped rule) leaves Bash available and denies only matching calls.

---

## Sandboxing

Four levels of isolation, increasing:

| Option | Isolation | Use |
|---|---|---|
| **Sandboxed Bash tool** | Filesystem and network isolation for shell commands | Built in; the default first line |
| **Dev containers** | Container per project | Team-consistent environments |
| **Docker / VM** | Full isolation | Untrusted code, aggressive autonomy |
| **Claude Code on the web** | Anthropic-managed cloud sandbox | No local setup, no local risk |

The sandboxed Bash tool is the one you'll actually use. Enable it and Claude can be far more autonomous with far less risk, because a bad command can't reach outside the sandbox.

```json
{ "sandbox": { "enabled": true } }
```

See [Choose a sandbox environment](https://code.claude.com/docs/en/sandbox-environments) and [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing).

---

## Worktrees as a safety mechanism

```bash
claude -w feature-auth
```

Runs the session in an isolated git worktree at `<repo>/.claude/worktrees/<name>`. Changes can't collide with your main working tree, and abandoning the work is `rm -rf` on a directory rather than an unwinding exercise.

Also useful for parallel sessions and for subagent isolation.

---

## Hooks as enforcement

The strongest local control. A `PreToolUse` hook fires **before any permission-mode check, in every permission mode including `bypassPermissions`.** A hook returning `deny` blocks the tool even with `--dangerously-skip-permissions`.

The reverse is not true: a hook returning `allow` cannot override deny rules from settings.

**Hooks tighten. They never loosen.**

Minimal example — block edits to protected files:

```bash
#!/bin/bash
# .claude/hooks/protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED=(".env" "package-lock.json" ".git/")

for p in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$p"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$p'" >&2
    exit 2
  fi
done
exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh" }]
    }]
  }
}
```

Covered fully in [Hooks](hooks.md).

---

## The threat model

Three things to actually worry about.

### 1. Destructive commands

Mitigations: deny rules on `rm -rf`, `git push --force`, `git reset --hard`, `DROP TABLE`. A `PreToolUse` hook on `Bash` that pattern-matches. The confirmation-gate prompt from [Everyday workflows](everyday-workflows.md). And most fundamentally: **work in git, commit often.**

### 2. Prompt injection

Claude reads files, web pages, issue text, MCP tool results. Any of those can contain instructions. A malicious dependency's README, a poisoned issue, a compromised MCP server.

Mitigations:

- Sandbox the Bash tool
- Keep destructive tools behind deny/ask rules — injection that can't trigger an action is much less dangerous
- Be deliberate about which MCP servers you connect and what they can reach
- Audit skills and plugins before installing
- Use `auto` mode, whose classifier specifically checks for exfiltration shapes

### 3. Secret exposure

Claude reads files. If `.env` is readable, it's in context, and context goes to the model.

Mitigations: deny `Read(.env)` and `Read(**/*.pem)` and similar. Don't keep secrets in the repo. Use `claudeMdExcludes` and permission rules together.

---

## Organisation controls

For teams, these are enforced client-side regardless of what a user configures:

| Control | Where |
|---|---|
| `permissions.deny` | Managed settings |
| `sandbox.enabled` | Managed settings |
| Auth method and org lock (`forceLoginMethod`, `forceLoginOrgUUID`) | Managed settings |
| MCP server allowlist/denylist | [Managed MCP](https://code.claude.com/docs/en/managed-mcp) |
| Disable bypass mode (`permissions.disableBypassPermissionsMode`) | Managed settings |
| Behavioural guidance | Managed CLAUDE.md, or the `claudeMd` key in managed settings |
| Approved version range | Managed settings |

Managed settings live at OS-specific policy paths and can be deployed via MDM, Group Policy, Ansible, or [server-managed settings](https://code.claude.com/docs/en/server-managed-settings) — which needs no device management infrastructure.

---

## A sane default configuration

For a normal work repository:

```json
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/*.pem)",
      "Read(**/id_rsa*)",
      "Bash(rm -rf /*)",
      "Bash(git push --force*)",
      "Bash(git reset --hard*)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(npm publish*)",
      "Bash(docker push*)"
    ],
    "allow": [
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(npm test*)",
      "Read",
      "Grep",
      "Glob"
    ]
  },
  "sandbox": { "enabled": true }
}
```

Commit this as `.claude/settings.json`. It's a team asset.

---

## Try it

**Exercise 1 — Prove the distinction.**
Put "never read .env" in CLAUDE.md. Ask Claude to read it. Then add a deny rule and ask again. The difference between "usually complies" and "cannot" is the whole lesson.

**Exercise 2 — Build the default config.**
Add the config above to a real project. Work in it for a day. Note every prompt you found annoying and every one you were glad of.

**Exercise 3 — Sandbox.**
Enable the sandboxed Bash tool. Ask Claude to do something that would reach outside the project. Observe the failure.

**Exercise 4 — Mode comparison.**
Do the same moderate task in `default`, `acceptEdits`, and `auto`. Time each. Decide which is your daily driver.

**Exercise 5 — Injection tabletop.**
Write down: if a malicious instruction reached Claude via a file it reads, what's the worst it could do in your setup? Now check which of those actions is denied. Fix the gaps.

---

## Checkpoint

- You can explain why a hook can deny in bypass mode but can't allow past a deny rule
- Your main work repo has a committed `.claude/settings.json` with deny rules
- You know your own threat model and where the gaps are

---

## Going deeper

- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config)
- [Security](https://code.claude.com/docs/en/security)
- [Choose a sandbox environment](https://code.claude.com/docs/en/sandbox-environments)
- [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
- [Settings](https://code.claude.com/docs/en/settings)
- [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup)
