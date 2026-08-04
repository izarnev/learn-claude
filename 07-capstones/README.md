---
title: "Capstone projects"
order: 1
---

# Capstone projects

Five projects, one per stage. Each has a spec, a done-check, and a stretch goal.

Do the one that matches where you stopped. **A finished capstone is worth more than three more modules read.**

---

## Capstone 1 — The personal operating system

**After:** stage 01 (Foundations)
**Time:** 2–3 hours
**Requires:** free tier is enough, though a paid plan helps

### Build

A prompt library plus a personalisation setup that measurably changes how you work.

1. **A prompt library** — `claude-practice/prompts/` with at least eight structured prompt templates for things you actually do. Each with role, task, constraints, examples, input placeholder, and output format.
2. **Custom instructions** — five specific, verifiable behavioural instructions in Settings → Personalisation.
3. **A voice sample set** — 10–20 things you've written, ready to paste when you need Claude to sound like you.
4. **A cleaned memory** — audit and prune what Claude has stored about you.

### Done when

- You've used at least five of your templates on real work
- Someone who knows your writing can't reliably identify which of three samples was AI-assisted
- You can articulate what your custom instructions changed

### Stretch

Write a one-page guide teaching a colleague the three techniques that helped you most.

---

## Capstone 2 — The recurring workflow

**After:** stage 02 (Power user)
**Time:** 4–6 hours
**Requires:** a paid plan

### Build

Automate one thing you currently do manually every week.

1. **A Project** with instructions covering role, audience, format, vocabulary, constraints and ambiguity handling — plus a curated knowledge base
2. **At least one custom Skill** with a description that reliably triggers, and a body written like a runbook
3. **A connector** doing real work in the loop
4. **A Cowork task** with a proper brief: outcome, inputs, output location, constraints, definition of done
5. **A schedule** so it runs without you, with explicit no-op behaviour

### Done when

- It runs unattended and produces something you actually read
- It says "nothing to report" rather than padding when there's nothing
- You've measured the time saved against the time spent building it

### Stretch

Package the Skill and connector configuration so a colleague can adopt it in under ten minutes.

---

## Capstone 3 — The configured repository

**After:** stage 03 (Claude Code)
**Time:** 6–8 hours
**Requires:** a real repository you work in

### Build

Turn a repository into one where Claude Code is genuinely productive on day one.

1. **`CLAUDE.md`** — under 200 lines, with a Gotchas section, containing nothing derivable from the code
2. **`.claude/rules/`** — at least two path-scoped rules
3. **`.claude/settings.json`** — committed, with deny rules on secrets and destructive commands, and sandboxing enabled
4. **At least two Skills** — one procedure, one reference. Anything with side effects has `disable-model-invocation: true`
5. **At least one custom subagent** with a specified return format
6. **At least two hooks** — one notification, one enforcement
7. **`.mcp.json`** — committed, with at least one server that gives real capability
8. **A CI job** running Claude Code with explicit tool constraints and a budget cap

### Done when

- A colleague can clone the repo and be productive with Claude Code immediately
- Your enforcement hook blocks even in `bypassPermissions` mode
- The CI job has run on three real PRs and produced useful output
- `/context` shows a lean session

### Stretch

Package it as a plugin and install it in a second repository.

---

## Capstone 4 — The production endpoint

**After:** stage 04 (API)
**Time:** 8–12 hours
**Requires:** Console credits

### Build

A real API-backed service, built properly.

1. **A structured-output endpoint** — `output_config.format` with enums and an uncertainty field
2. **Prompt caching** — verified working via `cache_read_input_tokens`
3. **Model routing** — Haiku classify → Sonnet handle → Opus escalate
4. **At least one client tool and one server tool**
5. **Streaming** for the user-facing path
6. **Full instrumentation** — tokens, cost, cache, latency, stop reasons, prompt version
7. **An eval set of 20+ real examples** with a baseline score
8. **Error handling** for every stop reason and status code

### Done when

- Your eval score is recorded and you've improved it at least once by a measured change
- Cache hit rate is above 80% on repeat traffic
- You can state your cost per request to the nearest cent
- Feeding it garbage produces a graceful failure, not a stack trace

### Stretch

Compute the cost of the naive all-Opus version and show your architecture's reduction factor.

---

## Capstone 5 — The agent

**After:** stages 05–06 (Agents, Production)
**Time:** 15–25 hours
**Requires:** Console credits, and a real problem worth solving

### Build

An agent that does something genuinely useful, safely.

**Design (write this down before coding):**

- The problem, and why an agent rather than a workflow
- The termination condition
- The verification tools
- The worst-case outcome if it's compromised, and why that's acceptable

**Implementation:**

1. Built on the **Agent SDK** or **Managed Agents**
2. **Custom tools** for your domain, with errors specific enough for self-correction
3. **Verification tooling** — the agent can check its own work
4. **External state** — progress and status in files, resumable after a kill
5. **Structured output** — a typed result, not prose
6. **Guardrails** — iteration cap, spend cap, destructive-action gating, human escalation
7. **Subagents** where isolation genuinely helps
8. **Full observability** — per-turn trace, parent-child for subagents, cost attribution

**Testing:**

9. **An eval set** including edge cases, adversarial inputs, and every bug you've fixed
10. **Trajectory evaluation** — grade the path, not just the answer
11. **Failure injection** — tool errors, timeouts, nonsense responses
12. **Termination testing** — an impossible task, cleanly refused

### Done when

- It completes 20 realistic tasks with a recorded success rate
- You can reconstruct any run from logs
- p95 cost and turn count are within 3× of p50
- You killed it mid-run and it resumed correctly
- Your red-team attempts either failed or led to a fix
- It stops cleanly on a task it cannot complete

### Stretch

Deploy it. Run it against real traffic for a week with continuous eval. Write up what surprised you — that document is the most valuable thing you'll produce in this entire track.

---

## A note on finishing

Every one of these is deliberately more work than it first looks, because the gap between "I understand agents" and "I have shipped an agent" is where all the actual learning is.

If you only do one: **capstone 2 if you don't write code, capstone 3 if you do.** Those two change how you work every day.
