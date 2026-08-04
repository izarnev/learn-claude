---
title: "Web search and Research"
order: 6
---

# Web search and Research

> **You are here** · All paths · Free plan has limited search; Research needs Pro · 40–50 min · Assumes [Prompting fundamentals](02-prompting-fundamentals.md).

**What you'll learn:** when to use plain search vs. Research mode, and how to get output you can actually trust.

---

## If you only read one thing

Claude's built-in knowledge stops at a fixed date. For anything current, it has to look things up, and there are two ways it does that.

**Web search** is a handful of quick lookups with citations — right for a fact, a price, a recent announcement.

**Research** is a different animal: Claude plans an investigation, runs many searches, follows leads, and writes you a sourced report. It takes minutes rather than seconds. Right for "what's the landscape here", not "what's the capital of Peru".

The discipline that matters in both: **click the citations.** A confident summary attached to a source that doesn't say that is the most common way people get burned. Spot-check two or three links on anything you're going to act on.

---

## Three different things

| Feature | What it does | Time | Use when |
|---|---|---|---|
| **Web search** | A handful of live lookups, cited inline | Seconds | You need a current fact |
| **Extended thinking** | More internal reasoning, no external lookups | Seconds to a minute | The problem is hard, not unknown |
| **Research** | Multi-step investigation across many sources, produces a structured report | Minutes | You need a survey of a landscape |

They compose. Research uses search *and* thinking.

---

## Web search

Claude decides when to search based on your question, or you can force it. Results come back with citations you can click.

**Always search for:**

- Anything after the model's knowledge cutoff (May 2026 for Opus 5, Jan 2026 for Sonnet 5 and Fable 5)
- Prices, versions, release dates
- Who currently holds a role
- Whether something is still true
- Anything where being out of date would be embarrassing

**Prompting search well:**

Be specific about recency and source quality.

> Bad: `what's the best vector database`
>
> Good: `What are the leading vector databases as of mid-2026? Prioritise sources from the last six months. For each, note pricing model and whether it supports hybrid search. Cite everything.`

### Verify the citations

This matters. Claude cites what it retrieved, but summarisation can drift from the source. For anything consequential, **click through on at least the load-bearing claims.** The failure mode isn't fabricated URLs any more — it's a real source being characterised slightly wrong.

Ask for it explicitly:

> For each claim, quote the exact sentence from the source that supports it.

---

## Research

Research runs a longer, multi-step investigation. Claude plans an approach, searches repeatedly, follows leads, reconciles conflicting sources, and returns a structured report with citations. It can also search your connected apps (Gmail, Drive, etc.) if you have connectors enabled.

**Use it for:**

- Competitive landscapes
- Literature and prior-art surveys
- "What's the current state of X?" where X is broad
- Due diligence
- Anything where you'd otherwise open thirty tabs

**Don't use it for:** single facts. It's slower and it's overkill.

### Getting a good report

Research responds enormously to scoping. Give it:

1. **The question, sharply.** "Should we build or buy an auth system?" not "tell me about auth."
2. **Your context.** Team size, constraints, what you already ruled out.
3. **What "done" looks like.** "A recommendation with three options compared on cost, time-to-ship, and compliance burden."
4. **Source preferences.** "Prioritise primary sources and vendor docs over listicles."
5. **The output shape.** "A table comparing options, then a one-page recommendation."

Example:

> Research the current landscape for European payment processors suitable for a B2B SaaS doing ~€2M ARR, selling into Germany, France and the Netherlands.
>
> We need: SEPA direct debit, invoice payments, and card. We already ruled out Stripe on pricing.
>
> Deliver: a comparison table (pricing, supported methods, SEPA support, integration effort, notable limitations) covering at least five providers, then a one-page recommendation with reasoning. Prioritise vendor documentation and recent independent reviews over marketing content. Cite everything.

---

## The structured research prompt

For genuinely hard research — the kind where you want Claude to be rigorous rather than fast — this pattern (from Anthropic's own guidance) works well:

```
Search for this information in a structured way. As you gather data, develop several
competing hypotheses. Track your confidence levels in your progress notes to improve
calibration. Regularly self-critique your approach and plan. Update a hypothesis tree
or research notes file to persist information and provide transparency. Break down this
complex research task systematically.
```

It changes the character of the output from "here's what I found" to "here's what I found, here's what contradicts it, and here's how confident I am."

---

## Trust calibration

A practical hierarchy for how much to trust research output:

| Claim type | Trust level | What to do |
|---|---|---|
| Direct quote with a link you clicked | High | Fine |
| Cited factual claim | Medium-high | Spot-check the load-bearing ones |
| Synthesis across sources | Medium | Check the sources support the synthesis |
| Numbers, prices, dates | Check every time | These drift and get mis-transcribed |
| "Most experts agree" | Low | Ask which experts, where |
| Uncited claim in a search-enabled answer | Low | Ask for the source |

---

## Try it

**Exercise 1 — Cutoff demonstration.**
Ask about something that happened last month with search off, then on. Note what the model does when it doesn't know.

**Exercise 2 — Vague vs. scoped research.**
Run Research twice on the same topic: once with a one-line question, once with the full scoping structure above. Compare the reports.

**Exercise 3 — Citation audit.**
Take any Research report and check five citations at random. Rate each: accurate / slightly off / wrong. This gives you a personal calibration you'll rely on for years.

**Exercise 4 — Competing hypotheses.**
Run a research task with the structured prompt above. Note whether it surfaces contradictions it would otherwise have smoothed over.

**Exercise 5 — Real decision.**
Use Research on an actual decision you're facing. Judge it by whether it changed your mind about anything, not by whether it sounded good.

---

## Checkpoint

- You know when search is enough and when Research earns its extra minutes
- You have a personal sense of how often citations need checking
- Your research prompts specify output shape and source preferences

---

## Going deeper

- [When should I use web search, extended thinking, and research?](https://support.claude.com/en/articles/11095361-when-should-i-use-web-search-extended-thinking-and-research)
- [Enable and use web search](https://support.claude.com/en/articles/10684626-enable-and-use-web-search)
- [Use research on Claude](https://support.claude.com/en/articles/11088861-use-research-on-claude)
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
