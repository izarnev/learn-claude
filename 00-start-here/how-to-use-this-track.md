---
title: "How to use this track"
order: 0
---

# How to use this track

> **You are here** · All paths · Free plan · 10 min · Assumes nothing. This is the first file to read.

**What you'll learn:** how to work through this material so it actually sticks.

---

## If you only read one thing

This track is 60-odd short guides, grouped into stages. You don't do all of it — you pick one of the four paths in the [README](../README.md) and follow that. Every guide has the same shape, and every guide ends with exercises.

The exercises are the point. Reading about prompting improves your prompting roughly as much as reading about swimming improves your swimming. If you're going to skip something, skip the deep explanations and keep the exercises — not the other way round.

---

## The shape of every module

Every file follows the same five sections. When you're skimming, you can jump straight to **Try it**.

| Section | What it is |
|---|---|
| What you'll learn | One sentence. If you already know it, skip the module. |
| Concepts | The guide. Read once, properly. |
| Try it | Exercises. Do them in a real Claude window, not in your head. |
| Checkpoint | A self-test. If you can't do it, reread. |
| Going deeper | Official doc links for the parts this guide compresses. |

---

## What you need before you start

**Minimum:** a free Claude account at [claude.ai](https://claude.ai). Stages 00 and most of 01 work on free.

**For stage 02 (power user):** a paid plan — Pro, Max, Team, or Enterprise. Projects, custom Skills, Cowork, connectors and file creation are paid features.

**For stage 03 (Claude Code):** a paid Claude plan or a Claude Console account with credits, plus a terminal.

**For stages 04–06 (API):** a Claude Console account with prepaid credits at [platform.claude.com](https://platform.claude.com). Budget $5–20 to complete every exercise comfortably.

See [plans-and-pricing.md](plans-and-pricing.md) for the details.

---

## How to practise so it sticks

### Use a scratch project

Before module 01, create a folder on your computer called `claude-practice`. Everything you build in the exercises goes there. By stage 03 you'll be pointing Claude Code at it.

### Keep a prompt journal

One markdown file. Every time a prompt works well, paste it in with a one-line note on why. This is the single highest-leverage habit in the whole track — you're building a personal prompt library, and by stage 02 you'll convert the best entries into Skills.

### Do the exercises badly, on purpose

Several exercises ask you to write a deliberately vague prompt first, then a specific one. Do the vague version. Seeing the bad output is the lesson; skipping to the good prompt teaches you nothing.

### Don't chase completeness

You will not memorise every flag and parameter. Nobody does. The goal is knowing **that a capability exists** and **roughly where to look**. The cheat sheets in `99-reference/` exist so you can forget the details safely.

---

## A note on how fast this moves

Anthropic ships changes to Claude Code weekly and new models every few months. Specific things that will drift:

- **Model names and prices.** Check [the models overview](https://platform.claude.com/docs/en/about-claude/models/overview).
- **Claude Code flags and commands.** Check [the CLI reference](https://code.claude.com/docs/en/cli-reference) and the [weekly What's New](https://code.claude.com/docs/en/whats-new/index).
- **Consumer features.** Check [support.claude.com](https://support.claude.com).

Things that will *not* drift much, and which is why most of this track is durable:

- How to write a good prompt
- What a context window is and why it constrains you
- Why context isolation matters for agents
- Why evals matter more than prompt tweaking
- The trade-offs between instruction, tool, and enforcement

Weight your attention accordingly.

---

## Try it

1. Create your `claude-practice` folder.
2. Create `claude-practice/prompt-journal.md` with a single heading: `# Prompts that worked`.
3. Open [claude.ai](https://claude.ai) and confirm you can send a message.

## Checkpoint

You can answer: *which of the four learning paths in the README am I on, and which folders am I skipping?*

## Going deeper

- [Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude)
- [Where can I access Claude?](https://support.claude.com/en/articles/8461763-where-can-i-access-claude)
