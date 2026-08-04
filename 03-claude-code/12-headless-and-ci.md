---
title: "12 · Headless, CI, and automation"
---

# 12 · Headless, CI, and automation

**What you'll learn:** running Claude Code without a human watching — in scripts, in CI, and on a schedule.

---

## Print mode

```bash
claude -p "explain this function"
cat logs.txt | claude -p "summarise the errors"
claude -c -p "check for type errors"      # continue the last conversation, headless
```

`-p` runs the query and exits. This is the foundation of everything else in this module.

---

## Output formats

```bash
claude -p "list the exported functions in src/" --output-format json
claude -p "query" --output-format stream-json --verbose
```

| Format | For |
|---|---|
| `text` | Human reading (default) |
| `json` | Scripting — parse the result |
| `stream-json` | Real-time streaming; needed for several other flags |

### Structured output with a schema

```bash
claude -p --json-schema '{
  "type":"object",
  "properties":{
    "risk":{"type":"string","enum":["low","medium","high"]},
    "findings":{"type":"array","items":{"type":"string"}}
  },
  "required":["risk","findings"]
}' "assess the security risk of the current diff"
```

Returns validated JSON matching the schema after the agent completes its workflow. Print mode only. Claude Code exits with an error on an invalid schema.

This is the clean way to make Claude Code a step in a pipeline rather than something a human reads.

---

## Controlling the run

```bash
claude -p \
  --max-turns 10 \
  --max-budget-usd 2.00 \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Grep" "Edit" "Bash(npm test)" \
  --disallowedTools "Bash(git push*)" \
  "fix the failing tests"
```

| Flag | Effect |
|---|---|
| `--max-turns N` | Hard cap on agentic turns; errors when reached |
| `--max-budget-usd N` | Hard spend cap; subagent spend counts |
| `--allowedTools` | Execute without prompting |
| `--disallowedTools` | Deny rules; a bare tool name removes the tool entirely |
| `--tools` | Restrict which built-in tools exist at all |
| `--permission-mode` | Which mode to run in |
| `--no-session-persistence` | Don't save to disk |
| `--bare` | Skip auto-discovery — much faster startup |

**In CI, be explicit about permissions.** Don't reach for `--dangerously-skip-permissions` as the default; enumerate what the job actually needs.

---

## System prompt control

Four flags, all working in both interactive and print mode:

| Flag | Effect |
|---|---|
| `--append-system-prompt` | Add to the default prompt |
| `--append-system-prompt-file` | Same, from a file |
| `--system-prompt` | **Replace** the entire default prompt |
| `--system-prompt-file` | Same, from a file |

**Which to use:** append when Claude should stay a coding assistant that also follows your extra rules — you keep the default tool guidance, safety instructions and coding conventions. Replace when the identity or permission model is genuinely different, like a non-coding agent in an unwatched pipeline. Replacing drops *everything*, including safety instructions, so you own whatever the task still needs.

`--system-prompt` and `--system-prompt-file` are mutually exclusive; append flags combine with either.

---

## Cache-friendly multi-user runs

```bash
claude -p --exclude-dynamic-system-prompt-sections "query"
```

Moves per-machine sections (working directory, environment info, memory paths, git-repo flag) out of the system prompt and into the first user message. This makes the cached prefix identical across users and machines running the same task — a large saving for scripted, multi-user workloads.

Only applies with the default system prompt.

---

## GitHub Actions

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      Review this PR for security issues. Comment on specific lines.
      Focus on: auth, input validation, secrets handling.
```

Common jobs:

- **PR review** on every pull request
- **Issue triage** — label, assign, ask for repro steps
- **Automated fixes** — `/autofix-pr` from your terminal, or PR auto-fix in the cloud
- **Docs sync** — update docs when code changes
- **Translations** — `claude -p "translate new strings into French and raise a PR"`

For a managed version of PR review, [GitHub Code Review](https://code.claude.com/docs/en/code-review) does multi-agent analysis of your full codebase on every PR.

GitLab CI/CD is supported too.

---

## Authentication in CI

```bash
claude setup-token
```

Generates a long-lived OAuth token, printed to the terminal and not saved. Requires a Claude subscription. Store it as a CI secret.

Or use an API key via `ANTHROPIC_API_KEY`, or a cloud provider (Bedrock, Google Cloud, Foundry), or [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) so CI has no long-lived credential at all.

---

## Setup hooks

For one-time preparation in CI or scripts:

```bash
claude --init-only              # run Setup and SessionStart hooks, then exit
claude -p --init "query"        # Setup hooks with the `init` matcher
claude -p --maintenance "query" # Setup hooks with the `maintenance` matcher
```

Useful for installing dependencies or warming caches before the real run.

---

## Routines

Cloud-hosted recurring runs on Anthropic-managed infrastructure. Beyond schedules, they can trigger on an **API call** or a **GitHub event**.

Create from the web, the Desktop app, or `/schedule` in the CLI.

Good candidates: morning PR review, overnight CI failure analysis, weekly dependency audit, docs sync after merges.

See [Routines](https://code.claude.com/docs/en/routines) and [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire).

---

## Claude Code on the web

```bash
claude --cloud "Fix the login bug"     # start a web session from the terminal
claude --teleport                       # pull a web session back to your terminal
```

Runs in Anthropic's sandbox with configurable setup scripts, network access, and Docker. Good for long tasks you want running while your laptop is closed, and for repos you don't have locally.

---

## Writing a headless prompt

Different from interactive in the same three ways as scheduled tasks:

1. **No clarification is possible.** Resolve every ambiguity in advance.
2. **State the failure behaviour.** "If you can't determine X, exit without changing anything and say why."
3. **Specify the output contract.** A schema, a file path, a format.

Example CI prompt:

```
Review the diff between HEAD and origin/main.

Report only these categories: hardcoded secrets, SQL built by string
concatenation, missing auth checks on new endpoints, unvalidated user input
reaching a filesystem or shell call.

For each finding: file, line, category, severity (high/medium/low), and a
one-sentence explanation.

If you find nothing in these categories, return an empty findings array.
Do not report style issues, naming, or anything not in the list above.
Do not modify any files.
```

Every clause prevents a specific failure: scope creep, style noise, invented findings, and unwanted edits.

---

## Deep links

Embed `claude-cli://` links in runbooks, alerts and dashboards so a click opens Claude Code in the right repo with the right prompt. See [Launch sessions from links](https://code.claude.com/docs/en/deep-links).

---

## Try it

**Exercise 1 — JSON pipeline.**
Write a shell script that runs `claude -p --output-format json`, parses the result with `jq`, and does something with it.

**Exercise 2 — Schema-validated output.**
Use `--json-schema` to get a structured risk assessment of your current diff. Feed it into a script that fails the build on `high`.

**Exercise 3 — CI review job.**
Add a Claude Code review step to a real repository's CI. Constrain it with `--allowedTools` and `--max-budget-usd`. Watch it on three PRs.

**Exercise 4 — Bare mode benchmark.**
Time `claude -p "query"` against `claude --bare -p "query"` on a project with plugins and MCP servers.

**Exercise 5 — Routine.**
Set up a routine for something recurring. Check it produced useful output twice before trusting it.

**Exercise 6 — Failure behaviour.**
Write a headless prompt, then deliberately give it an input it can't handle. Confirm it fails the way you specified rather than improvising.

---

## Checkpoint

- You've run Claude Code in a real CI pipeline with explicit tool constraints
- You know when to append to the system prompt and when to replace it
- Your headless prompts specify failure behaviour and output contract

---

## Going deeper

- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)
- [Code Review](https://code.claude.com/docs/en/code-review)
- [Routines](https://code.claude.com/docs/en/routines)
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [Authentication](https://code.claude.com/docs/en/authentication)
