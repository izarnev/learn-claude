---
title: "01 · Your first real conversation"
---

# 01 · Your first real conversation

**What you'll learn:** how to drive a Claude conversation deliberately rather than hopefully — including the interface controls most people never touch.

---

## The interface, control by control

Open [claude.ai](https://claude.ai) or the desktop app. Here's what each thing does and when it matters.

### The message box

Type, hit Enter. `Shift+Enter` gives you a newline without sending — use it constantly, because multi-line prompts are almost always better than single-line ones.

### The model picker

Sits near the top or beside the input. Switching mid-conversation is allowed; the transcript carries over.

Rules of thumb:

- **Sonnet** — default. Fast, very capable, cheapest on your limits.
- **Opus** — hard reasoning, complex code, long agentic tasks, anything where quality clearly matters more than speed.
- **Fable** — the frontier option for long-running, genuinely difficult work.
- **Haiku** — when speed is everything.

Covered properly in [module 03](03-models-and-modes.md).

### Effort / thinking controls

Recent models let you set an **effort** level. Higher effort means more internal reasoning before answering: better on hard problems, slower and more token-hungry on easy ones.

Default is fine for most things. Raise it for maths, architecture decisions, subtle debugging, and multi-constraint planning.

### The attachment button

Files, images, screenshots. Drag-and-drop and paste both work. See [module 04](04-files-and-vision.md).

### Web search and Research

Two different things:

- **Web search** — Claude does a few lookups and cites them
- **Research** — Claude runs a multi-step investigation across many sources and produces a report

See [module 06](06-search-and-research.md).

### Editing and branching

Hover any message you sent and you can **edit** it. This does not append a correction — it **rewrites history and re-runs from that point**, discarding everything after.

This is the most underused feature in the product. When a conversation goes wrong, don't argue with Claude in follow-up messages — that pollutes the context with the wrong answer *and* your correction. Go back, fix the original prompt, re-run.

You can also **retry** a Claude response to get a different generation from the same prompt.

### Projects

A container with its own knowledge base and standing instructions. Covered in [02-power-user/01](../02-power-user/01-projects.md).

---

## Concepts: how to actually run a conversation

### Start over more than you think you should

A conversation is a context window that only grows. Once it contains a wrong answer, a tangent, and three corrections, every subsequent response is being generated against that mess.

**Heuristic:** if you've corrected Claude twice on the same point, or you've changed topic entirely, start a new chat. Paste in the two or three things worth keeping.

### Front-load the context, back-load the question

For anything with substantial input material:

```
[long document / data / code]

---

Given the above: [your actual question]
```

Not the other way round. Anthropic's testing shows queries at the end can improve quality by up to 30% on complex, multi-document inputs.

### Ask for the shape you want

Claude will pick a format if you don't. Naming one costs you eight words and removes an entire round trip.

> "...as a table with columns Risk, Likelihood, Mitigation."
> "...in three paragraphs of prose, no bullet points."
> "...as a numbered checklist I can print."

### Let it ask you questions

For anything ambiguous, this is the single highest-leverage sentence you can add:

> "Before you start, ask me up to five questions that would materially change your answer."

You'll be surprised how often it identifies the thing you forgot to mention.

### Treat it as a colleague, not a search box

The prompt that works is the one you'd send a competent new hire who has no context on your situation. That means: what you want, why, who it's for, what "good" looks like, and any constraints.

---

## An anatomy of a good first prompt

**Bad:**

> write a project update

**Good:**

> Write a project status update for my engineering team's weekly email.
>
> Context: we're building a payments integration. We shipped the sandbox environment this week, hit a delay on PCI review (now expected 2 weeks late), and started work on the refund flow.
>
> Audience: 12 engineers plus two product managers. They're technical and busy.
>
> Tone: direct, no corporate padding. Lead with the delay because that's what affects their planning.
>
> Length: under 200 words. Plain prose, no bullet points.

The second one takes forty seconds to write and saves three rounds of "no, shorter" and "no, less formal."

---

## Try it

**Exercise 1 — Feel the difference.**
Send the bad prompt above. Read the output. Start a new chat and send the good one. Note specifically what changed: not just quality, but how much *of your job* Claude did for you.

**Exercise 2 — Practise editing over arguing.**
Ask Claude for a 500-word blog intro on a topic you know. When it's not right, resist replying. Instead, edit your original message to add the missing constraint and re-run. Do this three times. Notice the output gets cleaner each time, and the conversation stays one turn long.

**Exercise 3 — The question-first pattern.**
Pick something genuinely underspecified from your real work ("help me plan the offsite", "review my pricing page"). Send it with: *"Before answering, ask me up to five questions that would materially change your response."* Answer them. Compare against what you'd have got without.

**Exercise 4 — Format control.**
Ask the same question five ways: as a table, as prose, as a checklist, as a decision tree, as a one-line answer. Save the phrasings that worked into your prompt journal.

**Exercise 5 — Deliberately fill the window.**
Have a long, meandering conversation — 20+ turns, several topic changes. Then ask a precise question about the first topic. Then start fresh, paste only the relevant part, and ask the same question. This is your proof that context hygiene matters.

---

## Checkpoint

- You can name what the edit button actually does to conversation history
- You know why you'd start a new chat instead of correcting
- You can write a prompt containing task, context, audience, tone, and format without thinking about it

---

## Going deeper

- [Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude)
- [What are some things I can use Claude for?](https://support.claude.com/en/articles/7996845-what-are-some-things-i-can-use-claude-for)
- [Change the model, effort, and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)
