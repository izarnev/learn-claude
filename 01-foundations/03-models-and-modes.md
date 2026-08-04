# 03 · Models, effort, and thinking

**What you'll learn:** which Claude model to use for what, and how the effort and thinking controls change behaviour.

---

## The model family (August 2026)

| | Claude Fable 5 | Claude Opus 5 | Claude Sonnet 5 | Claude Haiku 4.5 |
|---|---|---|---|---|
| **For** | Next-gen intelligence for long-running agents | Complex agentic coding, enterprise work | Best speed/intelligence balance | Fastest, near-frontier |
| **API ID** | `claude-fable-5` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5-20251001` |
| **Input / output** | $10 / $50 per MTok | $5 / $25 | $3 / $15 * | $1 / $5 |
| **Context** | 1M | 1M | 1M | 200k |
| **Max output** | 128k | 128k | 128k | 64k |
| **Adaptive thinking** | Always on | Yes | Yes | No |
| **Extended thinking** | No | No | No | Yes |
| **Knowledge cutoff** | Jan 2026 | May 2026 | Jan 2026 | Feb 2025 |
| **Latency** | Slower | Moderate | Fast | Fastest |

\* Sonnet 5 has introductory pricing of $2 / $10 through 31 Aug 2026.

There is also **Claude Mythos 5** (`claude-mythos-5`), same specs and pricing as Fable 5, offered invitation-only for defensive cybersecurity workflows under [Project Glasswing](https://anthropic.com/glasswing). No self-serve access.

### Model IDs are pinned snapshots

From the 4.6 generation onward, model IDs use a dateless format (`claude-opus-5`) but are still **pinned snapshots**, not evergreen pointers. Older models used dated IDs (`claude-haiku-4-5-20251001`) with an alias pointing at them.

Practical consequence: pinning a model ID means your behaviour won't shift under you, but you must migrate deliberately when a model is deprecated. Check [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

---

## Choosing a model

### Default to Sonnet

Sonnet 5 handles the overwhelming majority of real work. Start here and escalate only when you have evidence you need to.

### Escalate to Opus when

- The task is genuinely hard reasoning: architecture, tricky debugging, subtle analysis
- You're running a long agentic session where compounding small errors are costly
- Quality matters more than speed or cost
- You're doing complex, multi-file code work

### Reach for Fable when

- Long-running agent work over hours
- The absolute ceiling of capability matters and the price is acceptable

### Drop to Haiku when

- Classification, extraction, routing, tagging
- High volume, low complexity
- Latency is user-facing and matters
- Bear in mind its Feb 2025 cutoff and 200k context

### The composite pattern

Real systems mix models. A support pipeline might be:

```
Haiku      →  classify the ticket, extract entities
Sonnet     →  draft the reply
Opus       →  handle only the tickets Haiku flagged as complex
```

That's ~5× cheaper than running everything on Sonnet, with better outcomes on the hard cases.

---

## Effort

`effort` controls how much internal work Claude does before responding. Available levels vary by model; on Claude Opus 5 and Sonnet 5 it defaults to `high` on the Claude API and in Claude Code. On Claude Opus 4.8 it defaults to `high` everywhere including claude.ai.

```python
client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)
```

**Higher effort:** more exploration, more thinking tokens, better on hard problems, slower and more expensive.
**Lower effort:** faster, cheaper, and often indistinguishable on easy problems.

In the chat apps this is a settings toggle rather than a parameter.

> **Important nuance:** on Claude Opus 5, raising or lowering effort does **not** reliably change visible response length. If you want shorter answers, prompt for conciseness explicitly.

---

## Thinking

### Adaptive thinking (current)

`thinking: {type: "adaptive"}`. Claude decides when and how much to think, calibrated by task complexity and the `effort` setting. On easy queries it responds directly. In Anthropic's internal evaluations, adaptive thinking reliably outperforms the older extended-thinking mode.

Defaults, which differ by model and are worth knowing:

- **Opus 4.6 through 4.8, Sonnet 4.6** — thinking is **off** if you omit the `thinking` parameter
- **Opus 5, Sonnet 5** — thinking is **on** by default; on Opus 5 you can disable it only at effort `high` or lower
- **Fable 5, Mythos 5** — always on, regardless of the parameter

### Extended thinking (legacy)

`thinking: {type: "enabled", budget_tokens: N}`. Deprecated. Still works on Opus 4.6 / Sonnet 4.6 and is the only mode on Haiku 4.5. On Claude 4.7 and later, setting `budget_tokens` returns a 400 error.

Migrating: replace the budget with `effort`, and use `max_tokens` as your hard ceiling.

### Steering thinking with prompts

Adaptive thinking is promptable. If Claude is thinking too often — common with large system prompts:

```
Thinking adds latency and should only be used when it will meaningfully improve
answer quality — typically for problems that require multistep reasoning. When in
doubt, respond directly.
```

If you want more deliberate reasoning after tool calls:

```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding. Use your thinking to plan and iterate based
on this new information, and then take the best next action.
```

If Claude is over-exploring and burning tokens:

```
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning.
```

### When thinking helps most

Maths and logic · architecture decisions · debugging with several plausible causes · anything with multiple interacting constraints · tasks where being wrong is expensive.

### When it doesn't

Simple lookups · formatting and rewriting · creative writing (it can flatten voice) · anything where you'd rather have three fast attempts than one slow one.

---

## Model-specific behaviour worth knowing

Anthropic publishes per-model prompting guides because the models genuinely differ. The highlights:

**Claude Opus 5**
- Default responses run **longer** than prior models. Prompt for conciseness explicitly.
- It **self-verifies well without being told to.** Verification instructions carried over from older prompts cause over-verification and wasted tokens — remove them rather than rewriting them.
- Delegates to subagents readily; may need damping.

**Claude Sonnet 5**
- Follows instructions very literally.
- Watch calibration on response length and thinking depth.

**Claude Opus 4.6 / 4.8**
- Do more upfront exploration, especially at high effort. If your prompt says "if in doubt, use [tool]", it will over-trigger.
- Tendency to over-engineer: extra files, unnecessary abstractions, speculative flexibility. Counter with an explicit scope-limiting instruction.

**All current models**
- Run independent tool calls in parallel by default
- Are more concise and less self-congratulatory than earlier generations
- Default to LaTeX for maths (ask for plain text if you don't want it)

---

## Try it

**Exercise 1 — Same prompt, four models.**
Take a genuinely hard question from your domain. Run it on Haiku, Sonnet, Opus and Fable. Time each. Write down where the quality difference actually appeared — and whether it appeared at all.

**Exercise 2 — Effort ablation.**
Take a logic puzzle or a multi-constraint scheduling problem. Run at low effort, then high. Note whether the *answer* changed or only the *explanation*.

**Exercise 3 — Design a routing table.**
For a workflow you actually have, write down which steps go to Haiku, Sonnet and Opus, and why. Estimate the cost of all-Sonnet vs. your routing.

**Exercise 4 — Prompt the thinking.**
Give Claude a task and add the "commit to an approach" prompt above. Compare the thinking trace length against the same task without it.

---

## Checkpoint

- You can state which model you'd default to and what evidence would make you escalate
- You know whether thinking is on by default for the model you use most
- You can explain why `budget_tokens` is deprecated and what replaced it

---

## Going deeper

- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Steering thinking and cost control](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)
- [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)
