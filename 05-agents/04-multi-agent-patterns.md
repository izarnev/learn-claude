---
title: "Multi-agent patterns"
order: 4
---

# Multi-agent patterns

**What you'll learn:** when several agents beat one, and how to coordinate them without creating a mess.

---

## Start with the objection

Multi-agent systems cost more, are harder to debug, and fail in more interesting ways. **One well-designed agent beats a badly-coordinated team almost every time.**

Add agents only for one of these reasons:

| Reason | Pattern |
|---|---|
| **Context isolation** — the work would flood the main window | Subagents |
| **Parallelism** — independent work that can run simultaneously | Parallel subagents |
| **Specialisation** — genuinely different instructions or tools | Specialised agents |
| **Adversarial checking** — you want disagreement | Debate / critic |

If none of those apply, you want one agent.

---

## Pattern 1 — Orchestrator–worker

```
        orchestrator (decides what's needed)
        ├── worker 1 → summary ─┐
        ├── worker 2 → summary ─┼→ orchestrator synthesises
        └── worker 3 → summary ─┘
```

The dominant pattern. The orchestrator holds the plan; workers hold the detail.

**Key design decisions:**

- **What returns.** The worker's whole value is that only its summary comes back. Specify the return format precisely.
- **What each worker knows.** Workers don't see the conversation. Pass enough context to work alone.
- **Worker models.** Mechanical workers can be Haiku. Only the orchestrator needs to be smart.

---

## Pattern 2 — Parallel specialists

```
        ┌→ security reviewer  ─┐
diff ───┼→ performance rev.  ──┼→ synthesiser → report
        └→ test reviewer     ──┘
```

Each specialist has its own instructions and looks at the same input through a different lens. Genuinely better than one general review, because a general reviewer optimises for breadth and misses depth.

The synthesis step matters: three raw reports is worse than one, unless something reconciles them and ranks by importance.

---

## Pattern 3 — Pipeline

```
extractor → validator → transformer → writer
```

Each stage is specialised and inspectable. Not really "multi-agent" — it's a workflow — but it's often the right answer to a problem someone framed as multi-agent.

---

## Pattern 4 — Debate / critic

```
proposer → critic → proposer revises → critic → ... → judge
```

Deliberate disagreement. Use for high-stakes decisions where the failure mode is confident consensus on a wrong answer.

The critic needs a genuinely adversarial prompt:

```
Your job is to find the strongest case against this proposal. Do not be
balanced. Do not acknowledge its merits. Assume it is wrong and find out why.
If after genuine effort you cannot construct a serious objection, say so
explicitly.
```

That last sentence prevents manufactured objections.

---

## Pattern 5 — Agent teams

Independent sessions that **message each other directly** and share a task list, rather than reporting to a lead.

Use when teammates need to share findings, challenge each other, and self-coordinate: research with competing hypotheses, parallel code review, feature work where each teammate owns a piece.

**The transition point from subagents:** you're running parallel subagents and either hitting context limits or finding your subagents need to talk to each other.

Cost is higher — each teammate is a full Claude instance.

In Claude Code, agent teams are experimental and disabled by default. See [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams).

---

## Pattern 6 — Dynamic workflows

Claude writes a **script** that orchestrates many subagents. You can read it, edit it, and rerun it.

The advantage over ad-hoc delegation: **inspectable and repeatable.** For a codebase audit you'll rerun quarterly, or a migration touching 400 files, you want the orchestration to be an artifact rather than a conversation.

See [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows).

---

## Coordination mechanics

### Shared state

Options, roughly in order of coupling:

| Mechanism | Notes |
|---|---|
| **Return values** | Simplest. Worker returns, orchestrator holds. |
| **Shared files** | `progress.txt`, `findings.json`. Works well; inspectable by you. |
| **A task list** | Agent teams use this. Self-coordinating. |
| **Direct messaging** | Highest coupling, most capability. |

Start with return values. Escalate only when you hit a real limitation.

### Avoiding duplicate work

Give each agent an explicit, non-overlapping remit. "Review the diff" ×3 gets you three overlapping reviews. "Review the diff for auth and authorisation issues only; ignore performance and style" gets you depth.

### Conflict resolution

When agents disagree, something must decide. Options: a judge agent, a rule (most conservative wins), or escalation to a human. Pick one deliberately — the default of "the orchestrator picks whichever it read last" is not a strategy.

---

## Cost

Multi-agent costs multiply. A five-worker orchestration is six conversations.

Controls:

- **Cheap models for mechanical workers.** A "list every TODO comment" worker is a Haiku job.
- **Restrict worker tools.** A worker with fewer tools wanders less.
- **Hard caps.** In Claude Code, `--max-budget-usd` counts subagent spend and stops background subagents when reached.
- **Measure per-agent.** `/usage` in Claude Code breaks it down by subagent.

---

## Over-delegation

Worth repeating: current models delegate readily and sometimes wrongly. From Anthropic's guidance:

> Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice. For example, the model may spawn subagents for code exploration when a direct grep call is faster and sufficient.

The damping prompt:

```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams that don't need to share state. For simple
tasks, sequential operations, single-file edits, or tasks where you need to
maintain context across steps, work directly rather than delegating.
```

---

## Debugging multi-agent systems

The hard part. What you need:

1. **A trace per agent** — its prompt, its tools, its result
2. **A parent-child relationship** in your logs, so you can reconstruct the tree
3. **Token and cost attribution** per agent
4. **The synthesis input** — what the orchestrator actually received

Without these, a multi-agent failure is unanalysable. Build them before you need them.

The Agent SDK's [OpenTelemetry support](https://code.claude.com/docs/en/agent-sdk/observability) gives you most of this. In Claude Code, `--forward-subagent-text` emits subagent text and thinking blocks with `parent_tool_use_id` set, so you can reconstruct each subagent's transcript.

---

## Try it

**Exercise 1 — Orchestrator–worker.**
Build a research orchestrator with three workers on different sources. Specify return formats precisely. Note how much the format specification matters.

**Exercise 2 — Parallel specialists.**
Three reviewers on the same diff with non-overlapping remits, plus a synthesiser. Compare against one general review.

**Exercise 3 — Debate.**
Proposer/critic on a real decision. Use the adversarial critic prompt. Note whether it surfaced something you'd have missed.

**Exercise 4 — Cost comparison.**
Same task: one agent, then five. Compare cost and quality. Decide whether the multi-agent version earned its price.

**Exercise 5 — Tracing.**
Add parent-child tracing to a multi-agent run. Reconstruct the tree from logs. Now break something and debug it from the trace alone.

**Exercise 6 — Over-delegation.**
Give a model a task simple enough not to need delegation. See whether it delegates. Add the damping prompt.

---

## Checkpoint

- You can justify every additional agent in your system by one of the four reasons
- Your workers have non-overlapping remits and specified return formats
- You can reconstruct a multi-agent run from logs

---

## Going deeper

- [Run agents in parallel](https://code.claude.com/docs/en/agents)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent teams](https://code.claude.com/docs/en/agent-teams)
- [Dynamic workflows](https://code.claude.com/docs/en/workflows)
- [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)
- [Multiagent orchestration (Managed Agents)](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
- [A harness for every task](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
