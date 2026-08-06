---
title: "Memory and personalisation"
order: 7
---

# Memory and personalisation

> **You are here** · All paths · Free plan for settings; memory features vary by plan · Read 10 min · Exercises 30 min · Assumes [What Claude actually is](../00-start-here/01-what-claude-is.md).

**What you'll learn:** how Claude carries context across conversations, how to control it, and how to make Claude sound like you rather than like a press release.

---

## If you only read one thing

By default Claude starts every conversation knowing nothing about you. Two features change that.

**Custom instructions** are standing preferences applied to every chat — who you are, how you like things written, what to never do. Set once, applies forever. This is the higher-value of the two and almost nobody bothers.

**Memory** lets Claude carry things it learned about you between conversations. You can view it, edit it, turn it off, and use incognito chats that don't persist at all.

If you want Claude to write like you rather than like a press release, describing your voice barely works — give it two or three samples of your actual writing instead. That's a bigger jump in quality than any adjective you could pick.

---

## Memory in the chat apps

Claude can remember things across conversations. Not because the model has memory — it doesn't — but because the product stores information and injects it into new chats.

What it remembers: your preferences, ongoing projects, working style, facts you've told it about yourself and your work.

### Controlling it

Settings → Personalisation. You can:

- **Turn memory on or off**
- **View what's stored** — it's readable, plain text
- **Edit or delete individual memories**
- **Import and export** your memory — useful for backup or moving between accounts

### Telling it to remember

Just say so: *"Remember that I always want code examples in TypeScript, not JavaScript."*

### Incognito chats

A conversation that doesn't persist to history and doesn't write to memory. Use it for one-off sensitive queries or when you don't want to pollute your memory with a topic you'll never revisit.

### Chat search

Claude can search your past conversations and build on them. *"Find the conversation where we designed the onboarding flow and continue from there."* This is different from memory — it's retrieval over your history rather than a stored summary.

---

## Personalisation settings

Beyond memory, you can configure:

- **Response style** — how formal, how long, how much explanation
- **Custom instructions** — standing directions applied to every conversation
- **Appearance** — theme, font, layout density
- **Language** — respond in your preferred language regardless of what you write in
- **Break reminders and quiet hours** — nudges to step away

### Writing good custom instructions

Custom instructions apply everywhere, so they should be things that are true everywhere. Good ones are specific and behavioural:

```
Be concise. Skip preamble — start with the answer.
When I ask for code, use TypeScript with strict mode unless I say otherwise.
When I ask about a decision, give me the trade-off, not just a recommendation.
If my question is ambiguous in a way that changes your answer, ask before answering.
Don't apologise for limitations; just state them.
```

Bad ones are vague or contradictory:

```
Be helpful and thorough but also concise.    ← contradictory
Always give the best answer.                 ← meaningless
Be professional.                             ← too vague to act on
```

Remember [Prompting fundamentals](02-prompting-fundamentals.md): tell it what to do, not what to avoid, and explain why when the reason helps it generalise.

---

## Making Claude sound like you

Generic AI writing is a real problem, and it has a specific cause: without a voice reference, Claude writes to the average of everything it's read.

Three levels of fix, in increasing order of effort and effectiveness:

### Level 1 — Describe your voice

> Write this as I would. My style: short sentences. Concrete nouns. No hedging. I never use "leverage", "utilise", "robust", or "seamless". I open with the point, not with context.

### Level 2 — Give examples

Paste three things you actually wrote. Then:

> The three samples above are things I wrote. Match that voice — sentence rhythm, vocabulary, how I open and close. Now write [the thing].

This is dramatically better than description, because voice lives in patterns you can't articulate.

### Level 3 — Build a writing style profile

On surfaces that support it (Cowork, Claude Code), a **writing style skill** can be built from your actual sent messages and documents, then reused automatically for every draft. Once set up, you stop having to paste samples.

If a draft comes back sounding wrong, the fix is to update the profile — not to re-explain in the chat.

---

## Privacy in practice

Worth knowing rather than guessing:

- **Who can see conversations** — see [this support article](https://support.claude.com/en/articles/8325621-i-would-like-to-input-sensitive-data-into-my-chats-with-claude-who-can-view-my-conversations)
- **Shared chats** are public to anyone with the link until you unshare
- **Incognito chats** don't persist
- **Data export** — you can download everything under Settings
- **Enterprise** plans offer zero data retention options and admin-level controls
- **Session management** — you can log out of all active sessions and configure session security

For work with genuine confidentiality obligations, check your organisation's policy before pasting. That's a governance question, not a Claude question.

---

## Try it

**Exercise 1 — Audit your memory.**
Settings → Personalisation → view stored memories. Read all of them. Delete anything wrong or stale. Most people are surprised by what's in there.

**Exercise 2 — Write custom instructions properly.**
Draft five instructions using the specific/behavioural pattern. Use Claude for a week. Come back and revise based on what actually annoyed you.

**Exercise 3 — Voice matching ladder.**
Pick something you need to write. Generate it three ways: no voice guidance, with a described voice, with three writing samples. Show all three to someone who knows your writing and ask which is yours. This exercise is worth doing properly — it's the difference between AI writing you'd send and AI writing you'd be embarrassed by.

**Exercise 4 — Incognito.**
Run an incognito chat. Verify afterwards that it's absent from history and didn't affect memory.

**Exercise 5 — Chat search.**
Find an old conversation using search and continue it. Note this is a genuine alternative to memory for project continuity.

---

## Checkpoint

- You know the difference between memory (stored, injected) and chat search (retrieval over history)
- Your custom instructions are specific enough that you could verify whether Claude followed them
- You know the three levels of voice matching and which one you'll actually use

---

## Going deeper

- [Understanding Claude's personalisation features](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features)
- [Use Claude's chat search and memory to build on previous context](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)
- [Import and export your memory from Claude](https://support.claude.com/en/articles/12123587-import-and-export-your-memory-from-claude)
- [Use incognito chats](https://support.claude.com/en/articles/12260368-use-incognito-chats)
- [Configuring session security settings](https://support.claude.com/en/articles/13163631-configuring-session-security-settings)
