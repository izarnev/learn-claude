---
title: "Model cheat sheet"
---

# Model cheat sheet

*As of August 2026. Verify against [the models overview](https://platform.claude.com/docs/en/about-claude/models/overview) — this changes.*

---

## The table

| | Claude Fable 5 | Claude Opus 5 | Claude Sonnet 5 | Claude Haiku 4.5 |
|---|---|---|---|---|
| **API ID** | `claude-fable-5` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5-20251001` |
| **Alias** | `claude-fable-5` | `claude-opus-5` | `claude-sonnet-5` | `claude-haiku-4-5` |
| **Input / MTok** | $10 | $5 | $3 * | $1 |
| **Output / MTok** | $50 | $25 | $15 * | $5 |
| **Context** | 1M | 1M | 1M | 200k |
| **Max output** | 128k | 128k | 128k | 64k |
| **Adaptive thinking** | Always on | Yes | Yes | No |
| **Extended thinking** | No | No | No | Yes |
| **Reliable cutoff** | Jan 2026 | May 2026 | Jan 2026 | Feb 2025 |
| **Latency** | Slower | Moderate | Fast | Fastest |

\* Sonnet 5 introductory pricing: **$2 / $10** through 31 August 2026.

**Claude Mythos 5** (`claude-mythos-5`) — same specs and pricing as Fable 5. Invitation-only for defensive cybersecurity via [Project Glasswing](https://anthropic.com/glasswing). No self-serve access.

**Cloud IDs:** Bedrock uses `anthropic.claude-opus-5` style; Google Cloud uses `claude-opus-5`; Claude Platform on AWS uses the same IDs as the Claude API.

**Batch API extended output:** Opus 5, Opus 4.8/4.7/4.6, Sonnet 5 and Sonnet 4.6 support up to **300k output tokens** with the `output-300k-2026-03-24` beta header.

---

## Which model

| Task | Model |
|---|---|
| Default for almost everything | **Sonnet 5** |
| Complex agentic coding, enterprise work | **Opus 5** |
| Long-running agents, absolute ceiling | **Fable 5** |
| Classification, extraction, routing, tagging | **Haiku 4.5** |
| High-volume, latency-sensitive | **Haiku 4.5** |
| Hard reasoning where being wrong is expensive | **Opus 5** |

**The composite pattern:** Haiku classifies → Sonnet handles → Opus takes only the hard cases. Typically 60–80% cheaper with equal or better quality.

---

## Thinking defaults — memorise this

| Model | Without a `thinking` parameter |
|---|---|
| Opus 4.6 / 4.7 / 4.8, Sonnet 4.6 | **Off** |
| Opus 5, Sonnet 5 | **On** (Opus 5: can only disable at effort `high` or lower) |
| Fable 5, Mythos 5 | **Always on** |
| Haiku 4.5 | Adaptive not supported |

**Effort defaults:** `high` on the Claude API and Claude Code for Opus 5 and Sonnet 5. `high` everywhere including claude.ai for Opus 4.8.

---

## Request shapes

```python
# Current
client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)

# Legacy — 400 error on Claude 4.7+
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[...],
)
```

---

## Model-specific behaviour

**Opus 5**
- Longer default responses. Effort does **not** reliably change visible length — prompt for conciseness.
- Self-verifies well without instruction. **Remove** verification instructions carried from older prompts; they cause over-verification.
- Delegates to subagents readily; may need damping.

**Sonnet 5**
- Very literal instruction following.
- Watch response length and thinking-depth calibration.

**Opus 4.6 / 4.8**
- More upfront exploration, especially at high effort. Prompts saying "if in doubt, use [tool]" will over-trigger.
- Tendency to over-engineer. Counter with an explicit scope-limiting instruction.

**Opus 4.5**
- When thinking is disabled, unusually sensitive to the word "think". Use "consider", "evaluate", "reason through".

**All current models**
- Run independent tool calls in parallel by default
- More concise and less self-congratulatory than earlier generations
- Default to LaTeX for maths
- **No prefill support** from 4.6 onward
- Over-trigger on aggressive prompt language (`CRITICAL: YOU MUST`)

---

## Versioning

From the 4.6 generation, model IDs use a dateless format (`claude-opus-5`) but are still **pinned snapshots**, not evergreen pointers. Earlier models used dated IDs with an alias pointing at them.

Pin explicitly. Migrate deliberately. Check [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).

Query capabilities programmatically via the [Models API](https://platform.claude.com/docs/en/api/models/list) — the response includes `max_input_tokens`, `max_tokens` and a `capabilities` object.

---

## Cost arithmetic

Per 1,000 requests of 3,000 input + 500 output tokens:

| Model | Cost |
|---|---|
| Fable 5 | $55 |
| Opus 5 | $27.50 |
| Sonnet 5 | $16.50 (intro: $11) |
| Haiku 4.5 | $5.50 |

Add prompt caching (80% of input cached) and Sonnet 5 drops to roughly $9. Add Haiku routing and it drops further.
