---
title: "Agent design principles"
order: 1
---

# Agent design principles

**What you'll learn:** how to decide whether you need an agent at all, and how to design one that doesn't fall over.

---

## What an agent is

A system where **the model decides the control flow.**

```
Workflow:  you decide the steps, the model fills in the content
Agent:     the model decides the steps
```

That's the whole distinction, and it's the most important design decision you'll make.

---

## Don't build an agent

Seriously — start here.

| If | Build |
|---|---|
| The steps are always the same | A workflow. Chain prompts. |
| One model call answers it | One model call. |
| Latency must be predictable | A workflow. Agents have variable turn counts. |
| Cost must be predictable | A workflow. |
| Errors must be traceable to a step | A workflow. |
| **The path genuinely depends on what's discovered** | An agent |
| **The task needs open-ended exploration** | An agent |
| **The number of steps is unknowable in advance** | An agent |

Agents are more capable and less predictable. Pay that price deliberately.

A useful test: **can you draw the flowchart?** If yes, build the flowchart. If the flowchart has a box saying "figure out what to do next", you need an agent — but only for that box.

---

## Patterns, in order of complexity

### 1. Single call

```
input → model → output
```

Underrated. Many "agent" projects are one good prompt.

### 2. Chained calls

```
input → extract → analyse → format → output
```

Each step is inspectable, testable, cheap, and can use a different model. The self-correction chain (draft → critique → revise) is this pattern.

### 3. Routing

```
input → classifier (Haiku) → specialised handler
```

Cheap and effective. Classification is a Haiku job; only the hard branch needs Opus.

### 4. Parallelisation

```
        ┌→ security review  ─┐
input ──┼→ perf review     ──┼→ synthesise → output
        └→ style review    ──┘
```

Independent analyses run simultaneously. Also useful for consensus — run three times, compare.

### 5. Orchestrator–worker

```
orchestrator → decides what subtasks are needed
             → spawns workers
             → synthesises results
```

The orchestrator is an agent; the workers may be workflows. This is what Claude Code's subagents do, and it's the pattern that scales furthest.

### 6. Autonomous loop

```
loop until done:
  model decides → acts → observes → reasons
```

Maximum capability, minimum predictability. Requires: a hard iteration cap, a spend cap, a termination condition, and observability.

---

## The five things every agent needs

### 1. A termination condition

Not just an iteration cap — a definition of *done*. Without one, agents oscillate between "nearly finished" states.

```
You are done when: [specific, checkable condition].
State explicitly when you are done and why.
If you cannot reach the done condition, say what is blocking you and stop.
```

That last line matters. Agents that can't succeed and can't stop are the expensive failure mode.

### 2. Verification tools

From Anthropic's own guidance:

> As the length of autonomous tasks grows, Claude needs to verify correctness without continuous human feedback.

An agent that can't check its own work will confidently report success. Give it: a test runner, a linter, a browser (Playwright MCP), a validator, a query it can run.

**Verification capability is the ceiling on how autonomous an agent can safely be.**

### 3. External state

Context windows end. Filesystems don't.

```
Keep progress in progress.txt and structured status in tests.json.
Use git commits as checkpoints.
```

Anthropic's guidance is explicit that current models are extremely effective at rediscovering state from the filesystem — and that starting fresh with good state files often beats compaction.

Use **structured formats for structured data** (JSON for test results, task status) and **freeform text for progress notes**.

### 4. Guardrails

Instructions are requests. Enforcement is code.

- Hard iteration cap
- Hard spend cap (`--max-budget-usd`, or your own accounting)
- Deny rules on destructive operations
- Human approval gates on irreversible actions
- Timeouts

### 5. Observability

You cannot debug what you can't see. Log every turn: the prompt, the tools called, the results, the tokens, the decision. Covered in [Observability](../06-production/observability.md).

---

## Prompting an agent

Six blocks that belong in nearly every agent system prompt.

**Role and objective** — what it is, what it's for.

**Available tools and when to use them** — beyond the schemas, guidance on choice.

**Reversibility guidance:**

```
Consider the reversibility and potential impact of your actions. Take local,
reversible actions freely, but for actions that are hard to reverse, affect
shared systems, or could be destructive, ask before proceeding.

When you hit an obstacle, don't use destructive actions as a shortcut.
```

**Persistence** (if you have compaction or external state):

```
Your context window will be automatically compacted as it approaches its limit,
so do not stop tasks early due to token budget concerns. As you approach the
limit, save your progress and state before the context refreshes. Never
artificially stop a task early regardless of remaining context.
```

**Delegation guidance** (if it has subagents):

```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams. For simple tasks, sequential operations, or
tasks needing context continuity, work directly.
```

Current models delegate readily and may over-delegate.

**Scope discipline:**

```
Only make changes that are directly requested or clearly necessary. Don't add
features, refactor beyond what was asked, or design for hypothetical future
requirements.
```

---

## Long-horizon design

For tasks spanning multiple context windows, Anthropic's guidance is specific:

1. **Use a different prompt for the first context window.** Set up the framework — write tests, create setup scripts — then use later windows to iterate on a todo list.

2. **Have the model write tests in a structured format** (`tests.json`) before starting work. Remind it: *"It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."*

3. **Set up quality-of-life tooling.** Have it create an `init.sh` that starts servers, runs tests, and runs linters — so a fresh context doesn't repeat setup work.

4. **Prefer starting fresh over compacting** for long tasks, with a prescriptive restart prompt:
   > "Call pwd; you can only read and write files in this directory. Review progress.txt, tests.json, and the git logs. Manually run through a fundamental integration test before implementing new features."

5. **Encourage complete use of context:**
   > "It's encouraged to spend your entire output context working on the task — just make sure you don't run out of context with significant uncommitted work."

---

## Failure modes and their fixes

| Failure | Fix |
|---|---|
| Loops forever | Iteration cap + explicit done condition |
| Declares success incorrectly | Verification tools + "verify before claiming done" |
| Wanders off task | Tighter objective; scope-limiting prompt |
| Burns budget | Spend cap; cheaper model for routine turns |
| Loses the thread over long runs | External state files |
| Takes a destructive shortcut | Reversibility prompt + deny rules |
| Over-delegates to subagents | Delegation guidance |
| Over-engineers | Scope discipline prompt |
| Fails silently in production | Observability |

---

## Try it

**Exercise 1 — The flowchart test.**
Take an "agent" idea you have. Try to draw the flowchart. If you can, build the workflow instead and note how much simpler it is.

**Exercise 2 — Routing.**
Build a router: Haiku classifies, then dispatches to a Sonnet or Opus handler. Compute cost against all-Opus.

**Exercise 3 — Verification.**
Build a small agent *without* a verification tool. Note how often it claims success incorrectly. Add one. Measure again.

**Exercise 4 — External state.**
Build an agent that writes `progress.txt` and resumes from it. Kill it halfway. Restart. Confirm it picks up.

**Exercise 5 — Guardrails.**
Add an iteration cap, a spend cap, and a destructive-action gate to an existing agent. Test each triggers.

**Exercise 6 — Parallel review.**
Build the three-reviewer parallelisation pattern. Compare against one general review on the same diff.

---

## Checkpoint

- You can name the six patterns and say which fits a given problem
- Every agent you've written has all five required components
- You've experienced an agent confidently failing without verification tools

---

## Going deeper

- [Prompting best practices — agentic systems](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Tutorial: Build a tool-using agent](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent)
- [Use case guides](https://platform.claude.com/docs/en/about-claude/use-case-guides/overview)
