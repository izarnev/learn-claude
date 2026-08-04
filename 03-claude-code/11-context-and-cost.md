---
title: "11 · Context and cost management"
---

# 11 · Context and cost management

**What you'll learn:** why sessions get slow and expensive, and the specific levers that fix it.

---

## The core dynamic

Every token in your context is resent on every turn. A session that has read forty files pays for forty files on turn 41, turn 42, and turn 100.

Two consequences follow, and both matter:

- **Cost grows superlinearly** with session length
- **Quality degrades** as signal gets diluted by accumulated noise

The good news: almost everything in this module is one command.

---

## Diagnose first

```
/context
```

Shows what's loaded and what each thing costs. Run it when a session feels slow. The answer is usually obvious once you look.

```
/usage
```

Shows what's driving your plan limits, broken down by skills, subagents, and MCP servers. This is how you find the MCP server nobody uses that's costing you 8k tokens a session.

```
/mcp
```

Per-server connection status and token cost.

---

## The levers, roughly in order of impact

### 1. Start a new session

`/clear` is free and it's the biggest lever you have. **One session per task.** When you change topic, clear.

Concretely: finishing a bug fix and starting a feature in the same session means the feature work carries the entire bug investigation.

### 2. Choose the right model

Opus costs 5× Sonnet on input and output, and consumes plan limits proportionally.

```bash
claude --model sonnet
claude --model opus
```

Or `/model` mid-session. Or the `opusplan` alias — plan on Opus, execute on Sonnet.

Use `--fallback-model sonnet,haiku` so an overloaded primary doesn't stall you.

### 3. Use subagents for anything that reads a lot

A subagent's forty file reads stay in *its* context. Only the summary comes back. See [module 07](07-subagents-and-parallelism.md).

### 4. Keep CLAUDE.md under 200 lines

It loads in full, every session, on every request. `/doctor` proposes trims — it cuts what Claude can derive from the codebase and keeps what it can't.

### 5. Move instructions to path-scoped rules

```yaml
---
paths: ["src/api/**/*.ts"]
---
```

Loads only when Claude touches a matching file. This is the main tool for a large instruction set that doesn't cost you on every session.

### 6. Set `disable-model-invocation: true` on skills you invoke manually

Drops their context cost to zero until you type `/name`.

For skills you didn't write, use `skillOverrides` in settings.

### 7. Disconnect unused MCP servers

Tool search keeps idle servers cheap, but not free. `/mcp` shows the cost.

### 8. Adjust effort

```bash
claude --effort low
```

Levels: `low`, `medium`, `high`, `xhigh`, `max`, `ultracode` (availability varies by model). Lower effort means less thinking, fewer tokens, faster responses. Mechanical work doesn't need `high`.

### 9. Use `--bare` for scripted calls

Skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory and CLAUDE.md. Much faster startup, much smaller context. Perfect for one-off scripted queries.

```bash
claude --bare -p "explain this regex: $PATTERN"
```

### 10. Preprocess before Claude sees it

Don't hand Claude a 50MB log. Grep it first:

```bash
grep -i error app.log | tail -100 | claude -p "what's going wrong?"
```

You can automate this with a hook that filters tool output before it enters context.

---

## Prompt caching

Claude Code manages prompt caching automatically. Things worth knowing:

- **Switching models invalidates the cache.** The first turn after a switch is slow and uncached. Don't flip models casually mid-session.
- **`/compact` costs tokens** — it's a model call over your whole transcript, and it invalidates the cache after.
- **CLAUDE.md edits don't apply mid-session** — the cached prefix is already fixed. Restart to pick them up.
- Check your cache hit rate; a low rate usually means something is changing in your prefix every turn.

See [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching).

---

## Compaction vs. starting fresh

When context fills, Claude Code compacts — summarising and continuing.

**Often, starting fresh is better.** Anthropic's own guidance:

> When a context window is cleared, consider starting with a brand new context window rather than using compaction. Claude's latest models are extremely effective at discovering state from the local filesystem.

The technique: keep state in files, then start clean.

```
# In your CLAUDE.md or a skill:
Keep progress in progress.txt and structured status in tests.json.
Use git commits as checkpoints.
```

```
# Starting a fresh session:
Run pwd. Review progress.txt, tests.json, and the git log.
Run the integration test manually before implementing anything new.
```

This beats compaction on long tasks, and it's more inspectable.

---

## Hard spend limits

```bash
claude -p --max-budget-usd 5.00 "large refactoring task"
```

Print mode only. **Subagent spend counts toward the cap.** Once reached, spawning another subagent fails with `Budget limit reached`, and Claude Code stops background subagents still running.

Also:

```bash
claude -p --max-turns 10 "query"
```

For teams, the Console offers workspace budgets, and the [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api) sets per-developer caps. If you run a Claude apps gateway, it can enforce daily/weekly/monthly caps live on every request.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Session feels slow | Large context | `/context`, then `/clear` |
| Auto-compact thrashing | Context repeatedly hitting the limit | Start fresh; move work to subagents |
| Sudden slow turn | Model switch invalidated the cache | Expected; don't switch casually |
| CLAUDE.md edit not applying | Cached prefix | Restart the session |
| High usage, unclear why | | `/usage` breaks it down |
| High CPU or memory | | See [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) |

---

## A cost-conscious default setup

```json
{
  "model": "sonnet",
  "fallbackModel": "haiku",
  "effortLevel": "medium"
}
```

Plus habits:

- `/clear` between tasks, always
- Opus only when you have a reason
- Subagents for exploration
- CLAUDE.md under 200 lines
- Path-scoped rules for the rest
- `--bare` for scripts

---

## Try it

**Exercise 1 — Watch it grow.**
Fresh session, `/context`. Work for 30 minutes. `/context` again. Identify the three biggest contributors.

**Exercise 2 — Subagent saving.**
Do a codebase-wide search directly, note `/context`. `/clear`, do it via a subagent, note `/context`. Quantify the saving.

**Exercise 3 — Trim CLAUDE.md.**
Run `/doctor` on a project with a long CLAUDE.md. Apply the proposed trims. Note what it cut and whether you agree.

**Exercise 4 — Path-scoped conversion.**
Move a language-specific instruction block out of CLAUDE.md into a path-scoped rule. Verify with `/context` that it's absent until you touch a matching file.

**Exercise 5 — Budget cap.**
Run a deliberately open-ended task with `--max-budget-usd 1.00`. Watch it stop.

**Exercise 6 — Fresh vs compacted.**
Take a long task. Run it to compaction, then continue. Separately, run it with progress files and a fresh session. Compare quality and cost.

---

## Checkpoint

- `/clear` between tasks is automatic for you
- You've run `/usage` and know what drives your limits
- Your CLAUDE.md is under 200 lines
- You know why a mid-session model switch causes one slow turn

---

## Going deeper

- [Manage costs effectively](https://code.claude.com/docs/en/costs)
- [Explore the context window](https://code.claude.com/docs/en/context-window)
- [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
- [Model configuration](https://code.claude.com/docs/en/model-config)
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- [Track team usage with analytics](https://code.claude.com/docs/en/analytics)
