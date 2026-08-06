---
title: "Prompting fundamentals"
order: 2
---

# Prompting fundamentals

> **You are here** · All paths · Free plan · Read 15 min · Exercises 40 min · Assumes [Your first real conversation](01-your-first-conversation.md). The most important module in stage 01.

**What you'll learn:** the six techniques that account for most of the quality difference between good and bad prompts — straight from Anthropic's own prompt engineering guidance.

---

## If you only read one thing

Anthropic's own test for a prompt: show it to a colleague who doesn't know the task. If they'd be confused, so is Claude. Everything below is a technique for removing confusion.

The six that matter, in order of how much they'll change your results:

1. **Be specific** about what you want and what format it should be in.
2. **Say why.** "Never use ellipses *because this will be read aloud by a text-to-speech engine*" works better than the rule alone, because Claude can then handle cases you didn't think of.
3. **Show examples.** Three to five. When you can't describe what you want, demonstrate it.
4. **Label the parts of your prompt** so instructions, background and data don't blur together.
5. **Give it a role.** One sentence — "you are a security engineer reviewing this for a bank" — measurably shifts what it notices.
6. **Long documents go at the top, your question at the bottom.** Anthropic measured up to 30% better answers from this alone.

One counterintuitive rule: tell Claude what to do, not what to avoid. "Write in flowing paragraphs" works; "don't use bullet points" only half-works.

---

## The golden rule

> Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too.

That's Anthropic's own framing and it's the whole discipline in one sentence. Everything below is a way of removing confusion.

---

## Technique 1 — Be clear and direct

Claude does not read your mind about scope, ambition, or standard. If you want "above and beyond", say so.

| Less effective | More effective |
|---|---|
| `Create an analytics dashboard` | `Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.` |
| `Fix the bug` | `Fix the login bug where users see a blank screen after entering wrong credentials` |
| `Summarise this` | `Summarise this in five bullet points aimed at a CFO who hasn't read it` |

Two mechanical rules:

- **Be specific about output format and constraints.**
- **Use numbered steps when order or completeness matters.** Claude follows explicit sequences reliably.

---

## Technique 2 — Explain *why*

Giving the reason behind an instruction lets Claude generalise correctly to cases you didn't anticipate.

| Less effective | More effective |
|---|---|
| `NEVER use ellipses` | `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine will not know how to pronounce them.` |

The second version means Claude also avoids em-dashes-used-as-pauses, emoji, and ASCII art — because it understands the actual constraint rather than the literal rule.

This generalises: **motivation beats prohibition.**

---

## Technique 3 — Use examples (few-shot)

Examples are the most reliable way to control format, tone, and structure. When you can't describe what you want, show it.

Make your examples:

- **Relevant** — mirror your real use case
- **Diverse** — cover edge cases; vary enough that Claude doesn't latch onto an accidental pattern
- **Structured** — wrap them in `<example>` tags, multiple in `<examples>`, so Claude can tell them apart from instructions

Three to five examples is the sweet spot.

```xml
<examples>
<example>
  <input>Customer says the app crashes on startup after the latest update.</input>
  <output>severity: high | area: mobile-client | needs_repro: yes</output>
</example>
<example>
  <input>Customer asks whether the annual plan can be paid by invoice.</input>
  <output>severity: low | area: billing | needs_repro: no</output>
</example>
</examples>

Classify this ticket in the same format:
<input>{{TICKET}}</input>
```

**Pro move:** ask Claude to critique your examples for relevance and diversity, or to generate more from your initial set.

---

## Technique 4 — Structure with XML tags

When a prompt mixes instructions, context, examples, and variable input, XML tags remove ambiguity about which is which.

```xml
<instructions>
Rewrite the draft below for a non-technical audience. Preserve every factual claim.
</instructions>

<style_guide>
{{STYLE_GUIDE}}
</style_guide>

<draft>
{{DRAFT}}
</draft>
```

Rules:

- Use consistent, descriptive tag names
- Nest when there's a natural hierarchy
- There's no fixed schema — invent tags that describe your content

XML tags are also an *output* control: "Put your reasoning in `<analysis>` tags and the final answer in `<answer>` tags" makes post-processing trivial and keeps the two separated.

Covered further in [Structured prompting with XML](08-structured-prompting.md).

---

## Technique 5 — Give Claude a role

One sentence of role framing measurably shifts tone and focus.

> You are a senior security engineer reviewing code for a fintech company. You care about auth, injection, and data exposure. You are blunt about risk.

In the API this goes in the `system` parameter. In chat, put it in your first message or in Project instructions.

Don't overdo it. A role sets a lens; it doesn't grant knowledge Claude lacks.

---

## Technique 6 — Long context: position and grounding

Two rules for anything over ~20k tokens of input:

**Put the long material at the top, the question at the bottom.** Up to 30% quality improvement on complex multi-document inputs.

**Wrap documents in tags with metadata:**

```xml
<documents>
  <document index="1">
    <source>annual_report_2025.pdf</source>
    <document_content>{{REPORT}}</document_content>
  </document>
  <document index="2">
    <source>competitor_analysis.xlsx</source>
    <document_content>{{ANALYSIS}}</document_content>
  </document>
</documents>

Analyse both. Identify strategic advantages and recommend Q3 focus areas.
```

**Ground responses in quotes.** For long-document tasks, ask Claude to extract relevant quotes *first*, then answer from them:

> Find quotes from the documents relevant to the question and place them in `<quotes>` tags. Then, based only on those quotes, answer in `<answer>` tags.

This dramatically reduces hallucination because it forces Claude to locate evidence before reasoning.

---

## Output formatting: tell it what to do, not what to avoid

This is a distinct and counterintuitive point.

| Doesn't work well | Works |
|---|---|
| `Do not use markdown` | `Your response should be composed of smoothly flowing prose paragraphs.` |
| `Don't be verbose` | `Answer in under 100 words.` |
| `No bullet points` | `Write in complete paragraphs.` |

Also: **your prompt's style influences the output's style.** If you write your prompt in heavy markdown with bullets and bold, you'll get heavy markdown back. Removing markdown from your prompt reduces markdown in the response.

If you want prose rather than bullet soup, this block works well:

```
When writing reports, explanations, or analyses, write in clear flowing prose using
complete paragraphs. Reserve markdown for inline code, code blocks, and simple headings.
Do not use ordered or unordered lists unless you're presenting truly discrete items or
I explicitly ask for a list. Incorporate items naturally into sentences instead.
```

---

## Two things that changed recently

**Prefilled assistant responses are gone.** Starting with Claude 4.6 models, providing a partial assistant message for Claude to continue from returns a 400 error. Use structured outputs, explicit instructions, or XML output tags instead. (Relevant if you've read older prompt-engineering material.)

**Dial back aggressive language.** Prompts written for older models often shout — `CRITICAL: You MUST always...`. Current models are far more responsive to the system prompt and will *over*-trigger on that language. Normal phrasing (`Use this tool when...`) works better.

---

## Try it

**Exercise 1 — Vague then specific.**
Take a real task. Write the laziest possible prompt. Send it. Then rewrite using techniques 1, 2 and 5. Put both outputs side by side. Keep the rewrite in your journal.

<details>
<summary>Worked example</summary>

**Lazy version:**

> write something about our new returns policy

You'll get a generic paragraph that could belong to any company, hedged in several directions because Claude doesn't know who's reading it.

**Rewritten with role (technique 5), specificity (1), and reasons (2):**

> You're writing customer-facing help centre copy for an online clothing retailer.
>
> Explain our new returns policy: 30 days instead of 14, free returns for members, £3.95 deducted for non-members, and items must be unworn with tags on.
>
> The audience is a customer who has just been told they can't return something, so they're already annoyed. Lead with what they *can* do, not with the rules. Don't apologise more than once — it reads as insincere and makes people angrier.
>
> Under 150 words, plain paragraphs, no bullet points.

**What to notice.** The rewrite isn't longer because it's more formal — it's longer because it contains four things Claude could not have guessed: the actual policy, who's reading, their emotional state, and a specific failure mode to avoid. That last clause ("don't apologise more than once — it reads as insincere") is technique 2 doing its work, and it's why the output will avoid a whole family of mistakes you didn't enumerate.

</details>

**Exercise 2 — Motivation over prohibition.**
Write an instruction as a rule (`never do X`). Then rewrite it as a reason (`because Y, never do X`). Test both on three inputs where the rule's *spirit* applies but the literal rule doesn't. Watch the second version generalise.

**Exercise 3 — Build a few-shot classifier.**
Pick a classification task from your work. Write four `<example>` pairs. Test on ten fresh inputs. Then remove the examples and test again on the same ten. Count the difference.

<details>
<summary>Worked example — with a ready-made task and a way to score it</summary>

No classification task of your own? Use this one: sorting incoming messages into `urgent` / `this week` / `no action needed`.

**Step 1 — write the examples.**

```xml
<examples>
<example>
  <input>Hi — the invoice you sent has last month's dates on it. No rush, just flagging.</input>
  <output>this week</output>
</example>
<example>
  <input>We're live and the checkout page is returning a 500 for everyone.</input>
  <output>urgent</output>
</example>
<example>
  <input>Thanks, received — will look at this when I'm back from leave on the 14th.</input>
  <output>no action needed</output>
</example>
<example>
  <input>Legal need the signed copy before Friday's board meeting or we can't file.</input>
  <output>urgent</output>
</example>
</examples>

Classify this message in the same format, output only the label:
<input>{{MESSAGE}}</input>
```

**Step 2 — test on ten real messages** from your inbox. Write down each label.

**Step 3 — delete the `<examples>` block** and run the same ten with only the instruction "classify this message as urgent, this week, or no action needed."

**How to score it.** Before you look at either result, decide yourself what the correct label is for each of the ten. Then count matches. You're looking for two things: how many labels changed, and — more revealing — whether the no-examples version stayed consistent in its *format*. It'll often start explaining its reasoning, or invent a fourth category like "medium priority". Format drift is usually a bigger cost than accuracy drift, because it breaks anything downstream.

**What to notice.** Example 1 is doing quiet work: it teaches that "no rush, just flagging" means *this week* rather than *no action needed*. That distinction is your judgment, and there's no way to state it in a rule as cleanly as showing it.

</details>

**Exercise 4 — Long-doc grounding.**
Take a 20+ page PDF. Ask a specific factual question two ways: directly, and with the quote-extraction pattern. Verify both answers against the source. Note which one you'd trust.

**Exercise 5 — Format wrestling.**
Get Claude to produce output with zero markdown. Try `do not use markdown` first — it will partially fail. Then use the positive-instruction block above.

---

## Checkpoint

You can, without looking:

- Name the golden rule
- Explain why "explain the why" outperforms "state the rule"
- Write a prompt using `<document>` / `<instructions>` structure
- Say what happened to prefilled responses and what replaced them

---

## Going deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — the canonical reference, worth reading in full
- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
