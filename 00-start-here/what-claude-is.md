---
title: "What Claude actually is"
order: 1
---

# What Claude actually is

> **You are here** · All paths · Free plan · 30–40 min · Assumes nothing. This is the mental model everything else builds on.

**What you'll learn:** a working mental model of what's happening when you talk to Claude — enough to explain its strengths and its failure modes without hand-waving.

---

## If you only read one thing

Claude is a program that reads everything in front of it and writes what should come next, one small piece at a time. That's it. It has no memory of you between conversations, no access to the internet, and no ability to open your files — *unless* a specific feature gives it one of those things.

Three consequences follow, and they explain almost every confusing thing Claude ever does:

- **It only knows what's in front of it.** Everything you've said in this conversation, plus anything you've attached. Nothing else. When Claude "forgets" something, it's almost always because the thing fell out of view, not because it changed its mind.
- **There's a limit to how much it can see at once**, and long conversations fill it up with clutter. This is why a fresh chat often works better than arguing with a stuck one.
- **It's confident even when it's wrong**, particularly about recent events, exact numbers, and specific quotes or links. The fix is always the same: give it the real source, or give it a tool that can check.

The technical vocabulary below — tokens, context windows, statelessness — is just precise language for those three points. Learn the three points first.

---

## The one-paragraph version

Claude is a large language model made by Anthropic. It was trained on a very large amount of text to predict what comes next, then further trained with human and AI feedback to be helpful, honest and harmless. When you send a message, Claude reads everything currently in the conversation and generates a response one small chunk at a time. It has no memory between conversations unless a feature explicitly gives it one, no access to the internet unless a tool gives it one, and no ability to change files unless a tool gives it one.

Everything else in this track is a variation on that theme: **what you put in the context, and what tools you hand it.**

---

## Concepts

### Tokens

Claude doesn't read characters or words. It reads **tokens** — chunks of text, roughly 3–4 characters each in English, so about ¾ of a word. "Unbelievable" might be three tokens; "cat" is one. Code and non-English text tokenise less efficiently.

This matters for two practical reasons:

1. **You're billed per token** on the API, in and out.
2. **The context window is measured in tokens**, so token efficiency is capacity.

A rough conversion: 750 words ≈ 1,000 tokens. A 200-page book ≈ 100,000 tokens.

### The context window

The **context window** — think of it as Claude's field of view, or how much it can hold in its head at once — is everything Claude can see: the system prompt, the conversation so far, any files you attached, any tool results, and the response it's currently writing.

Current sizes (August 2026):

| Model | Context window | Max output |
|---|---|---|
| Claude Fable 5 | 1M tokens | 128k |
| Claude Opus 5 | 1M tokens | 128k |
| Claude Sonnet 5 | 1M tokens | 128k |
| Claude Haiku 4.5 | 200k tokens | 64k |

A million tokens is enormous — roughly ten novels. But it is not infinite, and three things follow from that:

- **Long conversations degrade.** Not because Claude "forgets", but because the useful signal gets diluted by everything else you've said. Starting a fresh conversation is often the fix.
- **Position matters.** Put long documents near the *top* of your prompt and your question near the *bottom*. Anthropic's own testing shows this can improve response quality by up to 30% on complex multi-document inputs.
- **Filling the window is expensive.** Every token you put in is a token you pay for on every subsequent turn.

### Statelessness

*Stateless* means "keeps no record between requests". Each request is independent. Claude does not remember your last conversation. When a chat interface *appears* to remember, it's because the interface is resending the transcript, or because a memory feature is explicitly retrieving and injecting past content.

This is the single most important thing to internalise, because it explains:

- why context management is the core skill in agent building
- why CLAUDE.md files and Projects exist
- why "Claude forgot what I said" is almost always "the thing left the context window"

### Thinking

Modern Claude models can reason privately before answering — working through the problem in a scratchpad you don't see, then writing the response. On current models this is automatic: Claude judges how hard the question is and thinks proportionally, so a simple question still gets a fast answer.

In the chat apps you'll see this as a thinking or **effort** control. Turning it up helps on maths, logic, debugging, and decisions with several competing constraints. It doesn't help on simple lookups or rewriting, and it can actually flatten creative writing.

[Models, effort, and thinking](../01-foundations/models-and-modes.md) covers when to reach for it, and the exact API parameters if you need them.

### Tools

By itself Claude only produces text. Every other capability — searching the web, reading a file, running code, sending a Slack message — comes from a **tool**: a capability someone has handed it, described well enough that Claude can ask for it to be used. The surrounding software actually executes the call and hands back the result.

That loop — *model asks, harness executes, result goes back into context, model continues* — is called the **agentic loop**, and it is the thing that turns a chatbot into an agent. Everything in stages 03, 04 and 05 is elaboration on it.

### Training cutoff

Each model has a date past which it doesn't reliably know about the world.

| Model | Reliable knowledge cutoff |
|---|---|
| Claude Opus 5 | May 2026 |
| Claude Sonnet 5 | January 2026 |
| Claude Fable 5 | January 2026 |
| Claude Haiku 4.5 | February 2025 |

Anything after that date, Claude needs to look up. This is why web search matters and why Claude should search rather than answer from memory for anything current.

---

## What Claude is good at, and what it isn't

**Genuinely strong:**

- Writing, editing, and restructuring prose
- Reading and reasoning over long documents
- Code: writing, reading, debugging, refactoring, migrating
- Extracting structure from unstructured text
- Explaining things at whatever level you ask for
- Multi-step agentic work with tools

**Reliably weak, or requiring care:**

- **Precise arithmetic.** Claude reasons about maths well but computes it imperfectly. Give it a calculator/code tool for anything numeric that matters.
- **Facts after its cutoff.** It needs search.
- **Facts it half-knows.** Confident-sounding wrong citations, URLs, and quotes are the classic failure. Ground it in sources you provide.
- **Counting and exact positional tasks.** "How many words is this?" is not its strength.
- **Knowing what it doesn't know.** It's better at this than earlier models, but calibration is not perfect.

The general mitigation for all of these is the same: **give it the ground truth in context, or give it a tool that can check.**

---

## Try it

**Exercise 1 — Feel the cutoff.**
Ask Claude, without web search enabled: *"What is the most recent Claude model, and what's its exact API string?"* Then enable search and ask again. Note the difference.

**Exercise 2 — Feel statelessness.**
Tell Claude your favourite colour. Start a brand-new conversation and ask it what your favourite colour is. Then turn on memory (Settings → Personalisation) and repeat. You've just seen the difference between "the model remembers" and "the product retrieves".

**Exercise 3 — Feel token cost.**
Paste a long article (3,000+ words) and ask a one-line question. Then start fresh, paste the same article, and ask ten questions in sequence. The second conversation costs roughly ten times as much, because the article is resent every turn. This is exactly why prompt caching exists (see [Prompt caching](../04-api/prompt-caching.md)).

**Exercise 4 — Break it on purpose.**
Ask Claude to multiply two 6-digit numbers in its head, with thinking off. Check the answer. Then ask it to use code. This is the clearest demonstration of "give it a tool" you will ever get.

---

## Checkpoint

You can explain, in your own words:

- What a token is and why you care
- Why a long conversation gets worse rather than better
- Why Claude "forgetting" is usually a context problem, not a memory problem
- The difference between a model capability and a tool-provided capability

---

## Going deeper

- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
- [Glossary](https://platform.claude.com/docs/en/about-claude/glossary)
