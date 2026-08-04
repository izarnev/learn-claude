# 01 · What Claude actually is

**What you'll learn:** a working mental model of what's happening when you talk to Claude — enough to explain its strengths and its failure modes without hand-waving.

---

## The one-paragraph version

Claude is a large language model made by Anthropic. It was trained on a very large amount of text to predict what comes next, then further trained with human and AI feedback to be helpful, honest and harmless. When you send a message, Claude reads everything currently in the conversation and generates a response one small chunk at a time. It has no memory between conversations unless a feature explicitly gives it one, no access to the internet unless a tool gives it one, and no ability to change files unless a tool gives it one.

Everything else in this track is a variation on that theme: **what you put in the context, and what tools you hand it.**

---

## Concepts

### Tokens

Claude doesn't read characters or words. It reads **tokens** — chunks of roughly 3–4 characters in English. "Unbelievable" might be three tokens; "cat" is one. Code and non-English text tokenise less efficiently.

This matters for two practical reasons:

1. **You're billed per token** on the API, in and out.
2. **The context window is measured in tokens**, so token efficiency is capacity.

A rough conversion: 750 words ≈ 1,000 tokens. A 200-page book ≈ 100,000 tokens.

### The context window

The context window is everything Claude can see at once: the system prompt, the conversation so far, any files you attached, any tool results, and the response it's currently writing.

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

Each API request is independent. Claude does not remember your last conversation. When a chat interface *appears* to remember, it's because the interface is resending the transcript, or because a memory feature is explicitly retrieving and injecting past content.

This is the single most important thing to internalise, because it explains:

- why context management is the core skill in agent building
- why CLAUDE.md files and Projects exist
- why "Claude forgot what I said" is almost always "the thing left the context window"

### Thinking

Modern Claude models reason before answering. Two mechanisms exist:

- **Adaptive thinking** (`thinking: {type: "adaptive"}`) — Claude decides on its own how much to think, calibrated by task complexity and an `effort` setting. This is the current approach, used by Claude 4.6 and later. On Fable 5 it's always on.
- **Extended thinking** (`thinking: {type: "enabled", budget_tokens: N}`) — the older approach with a manual token budget. Deprecated; on Claude 4.7 and later, setting `budget_tokens` returns a 400 error.

In the chat apps this surfaces as a thinking/effort toggle. In the API it's the `thinking` and `output_config.effort` parameters. Module [01-foundations/03](../01-foundations/03-models-and-modes.md) covers when to reach for it.

### Tools

By itself Claude only produces text. Every other capability — searching the web, reading a file, running code, sending a Slack message — comes from a **tool**: a function description Claude is given, which it can request to call. The surrounding software actually executes the call and hands back the result.

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
Paste a long article (3,000+ words) and ask a one-line question. Then start fresh, paste the same article, and ask ten questions in sequence. The second conversation costs roughly ten times as much, because the article is resent every turn. This is exactly why prompt caching exists (module [04-api/07](../04-api/07-prompt-caching.md)).

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
