# 07 · Subagents, teams, and parallelism

**What you'll learn:** the four ways Claude Code does more than one thing at once, and how to pick between them.

---

## Why isolation matters

The core problem: **your context window is finite and everything you read stays in it.**

A research task that reads forty files leaves forty files in your conversation forever, even though you only wanted the conclusion. Subagents solve this: the work happens in a separate window, and only a summary comes back.

That's the whole idea. Everything else is variations on it.

---

## The four mechanisms

| | Subagent | Agent team | Agent view (background) | Dynamic workflow |
|---|---|---|---|---|
| **What** | Isolated worker inside your session | Independent sessions that message each other | Many full sessions, one screen | A script Claude writes that orchestrates subagents |
| **Context** | Own window; result returns to caller | Own window; fully independent | Fully independent | Each subagent isolated |
| **Communication** | Reports back to the lead only | Teammates message each other | You, manually | Via the script |
| **Cost** | Lower — summary returns | Higher — each is a full instance | Higher | Varies |
| **Best for** | Focused tasks where only the result matters | Work needing discussion and disagreement | Long parallel investigations | Codebase audits, large migrations |

---

## Subagents

### Built-in

Claude Code ships with several, and spawns them itself when useful:

| Agent | For |
|---|---|
| `Explore` | Broad fan-out searches. Reads excerpts, returns conclusions. Locates code; doesn't review it. |
| `Plan` | Designing implementation strategies |
| `general-purpose` | Anything else multi-step |

You can also ask directly: *"Use a subagent to find every place we parse dates."*

### Custom subagents

`.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user):

```markdown
---
name: test-auditor
description: Audits test coverage and quality for a module. Use when asked to review tests or find coverage gaps.
tools: Read, Grep, Glob, Bash
model: sonnet
skills:
  - testing-conventions
memory: true
---

You audit test suites. For the module you're given:

1. List every exported function and whether it has a test.
2. For each test, judge whether it tests behaviour or implementation.
   Implementation tests are a finding.
3. Identify edge cases the tests miss: nulls, empty collections, boundaries,
   concurrency.
4. Do not write or modify any code. Report only.

Return: a table of gaps ordered by risk, then your three highest-priority
recommendations. Under 400 words.
```

Key frontmatter:

| Field | What |
|---|---|
| `description` | When Claude should use it — same rules as skill descriptions |
| `tools` | Restrict its toolbox |
| `model` | Run it on a cheaper or stronger model |
| `skills` | Skills to **fully preload** into its context at launch |
| `memory` | Give it its own persistent auto memory |

You can also define them inline:

```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'
```

Precedence: **managed > CLI flag > project > user > plugin.**

### What loads in a subagent

- Its own system prompt (not the full Claude Code one)
- Skills listed in `skills:`, in full
- CLAUDE.md and git status — **except** `Explore` and `Plan`, which omit both
- Whatever the lead agent passes in the prompt

It does **not** inherit your conversation history, your invoked skills, or the main conversation's auto memory. The exception is a **fork**, which inherits the parent conversation and system prompt.

Subagents can spawn their own subagents.

### Writing a good subagent prompt

Three rules:

**Be explicit about the return format.** The subagent's whole value is that only its summary comes back. If you don't specify the shape, you get an essay.

**Be explicit about scope.** "Report only, don't modify" or "fix it and report what you changed." Ambiguity here is expensive.

**Give it enough context to work alone.** It can't see your conversation.

---

## Agent teams

Multiple independent Claude Code sessions that share a task list and message each other directly.

Use when teammates need to **share findings, challenge each other, and coordinate independently** — research with competing hypotheses, parallel code review from different angles, feature work where each owns a separate piece.

The transition point: you're running parallel subagents but hitting context limits, or your subagents need to talk to each other.

Display modes: `in-process` (default), `auto`, `tmux`, `iterm2`. Set with `--teammate-mode`.

> Agent teams are experimental and disabled by default. See [Agent teams](https://code.claude.com/docs/en/agent-teams).

---

## Background sessions and agent view

```bash
claude --bg "investigate the flaky test in test_billing.py"
claude --bg --exec 'pytest -x'          # run a shell command as a background job
claude agents                            # the dashboard
claude agents --json                     # scriptable
claude logs 7c5dcf5d
claude attach 7c5dcf5d
claude stop 7c5dcf5d
claude respawn 7c5dcf5d --all            # restart, e.g. after a binary update
claude rm 7c5dcf5d
claude daemon status
```

**Agent view** (`claude agents`) shows every session, what it's doing, and which need your input. Notification hooks with the `agent_needs_input` and `agent_completed` matchers fire while agent view is open.

Combine with worktrees so parallel sessions don't collide:

```bash
claude -w feature-auth --bg "implement the rate limiter"
```

---

## Dynamic workflows

For large orchestration — codebase audits, big migrations, cross-checked research — Claude writes a **script** that orchestrates many subagents. You can read it, edit it, and rerun it.

The advantage over ad-hoc delegation: it's inspectable and repeatable. When an audit needs rerunning next quarter, you have the script.

See [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows) and Anthropic's post [A harness for every task](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code).

---

## Model behaviour: watch for over-delegation

Current models orchestrate subagents natively and will delegate without being told. Anthropic's guidance notes this can go too far:

> Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice. For example, the model may spawn subagents for code exploration when a direct grep call is faster and sufficient.

Claude Opus 5 also delegates more readily than prior models.

If you're seeing excessive delegation:

```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams that don't need to share state. For simple
tasks, sequential operations, single-file edits, or tasks where you need to
maintain context across steps, work directly rather than delegating.
```

---

## Cost

Subagents cost real tokens — each has its own input and output. A ten-subagent audit is ten conversations.

Controls:

- Assign cheaper models to mechanical subagents (`model: haiku` in frontmatter)
- Restrict `tools` so a subagent can't wander
- Use `--max-budget-usd` in print mode; subagent spend counts toward the cap, and hitting it stops running background subagents
- Check `/usage` to see which subagents drive your limits

---

## Try it

**Exercise 1 — Prove the context saving.**
Ask Claude to find every usage of a pattern across a large codebase, directly. Check `/context`. Then `/clear` and do the same via a subagent. Compare.

**Exercise 2 — Build a custom subagent.**
Write `.claude/agents/test-auditor.md` (adapt the example above). Run it on a real module. Refine the return-format instruction until the output is genuinely useful.

**Exercise 3 — Cheap subagent.**
Write a mechanical subagent (e.g. "list every TODO comment with file and line") on `model: haiku` with `tools: Read, Grep, Glob`. Note how much cheaper it is.

**Exercise 4 — Parallel review.**
Spawn three subagents to review the same diff from different angles: security, performance, tests. Compare against one general review.

**Exercise 5 — Background investigation.**
`claude --bg` a genuinely slow task. Work on something else. Check in with `claude logs`.

**Exercise 6 — Over-delegation.**
Give Claude a task simple enough not to need subagents and see whether it spawns any. If it does, add the damping prompt to CLAUDE.md.

---

## Checkpoint

- You can articulate when a subagent beats doing it inline, and when it doesn't
- You have at least one custom subagent with a specified return format
- You know how to check whether subagents are driving your usage

---

## Going deeper

- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Run agents in parallel](https://code.claude.com/docs/en/agents) — compares all four mechanisms
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
- [Dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
