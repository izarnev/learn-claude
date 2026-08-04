# 03 · Thinking and effort

**What you'll learn:** how to control how hard Claude thinks, and how to avoid paying for reasoning you don't need.

---

## Adaptive thinking

The current mechanism. Claude decides when and how much to think, calibrated by task complexity and the `effort` setting.

```python
client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)
```

In Anthropic's internal evaluations, adaptive thinking reliably outperforms the older manual mode.

### Defaults by model — worth memorising

| Model | Without a `thinking` parameter |
|---|---|
| Opus 4.6, 4.7, 4.8; Sonnet 4.6 | **Off** |
| Opus 5, Sonnet 5 | **On.** On Opus 5, you can disable it only at effort `high` or lower |
| Fable 5, Mythos 5 | **Always on**, regardless of the parameter |
| Haiku 4.5 | Adaptive not supported; uses extended thinking |

---

## Effort

```python
output_config={"effort": "high"}
```

Levels vary by model. In Claude Code the CLI exposes `low`, `medium`, `high`, `xhigh`, `max`, and `ultracode`.

**Defaults:** on Opus 5 and Sonnet 5, `effort` defaults to `high` on the Claude API and in Claude Code. On Opus 4.8 it defaults to `high` everywhere including claude.ai. Set it explicitly to use a different level.

Higher effort → more exploration, more thinking tokens, better on hard problems, slower and more expensive.

> **Nuance on Opus 5:** changing effort does *not* reliably change visible response length. If you want shorter answers, prompt for conciseness explicitly.

---

## Extended thinking (legacy)

```python
thinking={"type": "enabled", "budget_tokens": 10000}
```

Deprecated. Still functional on Opus 4.6 / Sonnet 4.6, and it's the only mode on Haiku 4.5. **On Claude 4.7 and later, setting `budget_tokens` returns a 400 error.**

### Migrating

```python
# Before
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[...],
)

# After
client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...],
)
```

If you need a hard ceiling on cost, use `max_tokens` — not `budget_tokens`.

---

## Thinking blocks in the response

With thinking on, `content` contains `thinking` blocks before the `text` blocks.

```python
for block in message.content:
    if block.type == "thinking":
        pass                      # reasoning — usually not shown to users
    elif block.type == "text":
        print(block.text)
```

**Preserve thinking blocks in conversation history.** When you append `response.content` to your messages array, the thinking blocks go with it. This matters for multi-turn tool workflows — dropping them degrades subsequent turns. See [Thinking in tool and multi-turn workflows](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows).

---

## Steering thinking with prompts

Adaptive thinking is promptable. Three prompts worth having.

**Thinking too often** (common with large system prompts):

```
Thinking adds latency and should only be used when it will meaningfully improve
answer quality — typically for problems that require multistep reasoning. When
in doubt, respond directly.
```

**Want more deliberation after tool results:**

```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding. Use your thinking to plan and iterate
based on this new information, and then take the best next action.
```

**Over-exploring and burning tokens:**

```
When you're deciding how to approach a problem, choose an approach and commit
to it. Avoid revisiting decisions unless you encounter new information that
directly contradicts your reasoning. If you're weighing two approaches, pick
one and see it through.
```

---

## Prompting patterns with thinking

- **Prefer general instructions over prescriptive steps.** "Think thoroughly" often produces better reasoning than a hand-written step-by-step plan. Claude's reasoning frequently exceeds what a human would prescribe.
- **Multishot examples work with thinking.** Use `<thinking>` tags inside your few-shot examples to demonstrate the reasoning pattern; Claude generalises the style.
- **Ask for self-checks** — "before you finish, verify your answer against [criteria]" catches errors reliably, especially on coding and maths.

**Two important exceptions:**

**Claude Opus 5 self-verifies well without being told.** Verification instructions carried over from prompts tuned for earlier models cause over-verification, adding tokens and latency. When migrating to Opus 5, *remove* them rather than rewriting them.

**When thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word "think"** and its variants. Use "consider", "evaluate", or "reason through" instead.

Also: on Opus 5 with thinking disabled, the model can occasionally emit internal XML tags into visible output. Prefer keeping thinking on at a lower effort level rather than turning it off.

---

## When thinking earns its cost

**Worth it:** maths and logic, architecture decisions, debugging with several plausible causes, multi-constraint planning, anything where being wrong is expensive.

**Not worth it:** classification, extraction, formatting, simple lookups, high-volume low-complexity work, and creative writing (where it can flatten voice).

Cost intuition: thinking tokens are output tokens. On Opus 5 that's $25/MTok. A task that thinks for 5,000 tokens before a 500-token answer costs 11× the answer alone.

---

## Mid-conversation effort changes

You can raise or lower effort partway through a conversation — for example, low effort for routine turns and high effort when a hard decision arrives. Anthropic documents this as an [orchestration mode](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-effort-example).

---

## Try it

**Exercise 1 — Effort ablation.**
A hard reasoning problem, run at each available effort level. Record: correctness, latency, thinking tokens, cost. Find the point where more effort stops helping.

**Exercise 2 — Thinking on an easy task.**
Run a classification task with thinking on and off. Compare accuracy and cost. This will convince you not to leave it on everywhere.

**Exercise 3 — Steering prompts.**
Take a task where Claude over-thinks. Add the "commit to an approach" prompt. Measure the thinking token reduction.

**Exercise 4 — Block preservation.**
Build a multi-turn tool-use conversation. Deliberately drop thinking blocks from history. Compare quality against preserving them.

**Exercise 5 — Migration.**
If you have code using `budget_tokens`, migrate it. Verify behaviour is equivalent or better.

---

## Checkpoint

- You know whether thinking is on by default for the model you use
- You can explain why `budget_tokens` was deprecated and what replaced it
- You preserve thinking blocks in conversation history
- You know when *not* to enable thinking

---

## Going deeper

- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Steering thinking and cost control](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)
- [Thinking in tool and multi-turn workflows](https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows)
- [Troubleshooting thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting)
- [Extended thinking (legacy)](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
