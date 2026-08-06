---
title: "Plans, pricing, and limits"
order: 3
---

# Plans, pricing, and limits

> **You are here** · All paths · Free plan is fine for this module · Read 5 min · Exercises 20 min · Assumes nothing.

**What you'll learn:** which Claude plan to buy, when, and why you sometimes run out of Claude before the month does.

---

## If you only read one thing

There are two completely separate ways to pay Anthropic, and buying one gives you nothing on the other. A **subscription** (Free, Pro, Max, Team, Enterprise) is what you want if you're going to *use* Claude — chat, the desktop app, Cowork, Claude Code. **API credits** are what you want if you're going to *build software* on Claude. Most people only ever need a subscription, and Pro is the right answer for almost everyone doing this track.

Subscriptions don't give you a fixed monthly quota. You get a generous allowance that refills on a rolling basis, and three things burn through it fast: picking a more powerful model than you need, letting one conversation run very long, and using the agent tools (Cowork, Claude Code) which make many requests per task. If you keep hitting limits, starting fresh conversations more often is the cheapest fix available.

---

## The details

> ⚠️ Prices and limits change. Verify against [claude.com/pricing](https://claude.com/pricing) before making a decision. Figures below are as of August 2026.

### Two entirely separate billing systems

This confuses almost everyone at first.

| | Subscription | API |
|---|---|---|
| **Where** | claude.ai, desktop, mobile, Cowork, Claude Code | platform.claude.com |
| **You buy** | A monthly plan | Prepaid credits |
| **You're limited by** | Usage windows that reset | Your credit balance and rate limits |
| **Good for** | Using Claude | Building on Claude |

A Pro subscription gives you nothing on the API. API credits give you nothing on claude.ai. Claude Code is the one product that works with *either*.

If you're not writing software, you can stop thinking about the API entirely. It's covered in [API pricing and rate limits](../04-api/00-pricing-and-rate-limits.md), which is stage 04 — Path C territory.

---

### Subscription plans

| Plan | Roughly for | Key unlocks |
|---|---|---|
| **Free** | Trying it out | Chat, limited usage, basic features |
| **Pro** | Individuals | Higher limits, Projects, custom Skills, Cowork, connectors, Claude Code, file creation |
| **Max** | Heavy individual users | Substantially higher limits, priority access to new features |
| **Team** | Small orgs | Everything in Pro plus collaboration, shared projects, central billing |
| **Enterprise** | Large orgs | SSO, audit, compliance controls, zero data retention options, admin APIs |

**The features that require paid:** Projects, Cowork, connectors, code execution / file creation, Claude Code on a subscription.

> **Note on Skills.** You'll see Skills listed as available on Free. That's technically true and practically misleading: Skills only run when code execution is enabled, and code execution is paid-only. Treat Skills as a Pro-and-above feature.

---

### How usage limits work

Limits are enforced on rolling windows, not a simple monthly quota. Practical implications:

- **Model choice moves the needle most.** Opus consumes limits far faster than Sonnet, which consumes faster than Haiku. If you're hitting walls, this is the first thing to change.
- **Long conversations are expensive.** Every time you send a message, the entire conversation so far is re-sent to the model — so turn 40 of a chat costs many times what turn 2 did. Starting a fresh chat for a new topic is the cheapest optimisation you have.
- **Agentic work is the heaviest thing you can do.** Claude Code and Cowork make many model calls per task. A single Cowork session can consume what a day of chat would.
- **Run `/usage` in Claude Code** to see what's driving your limits, broken down by skills, subagents, and MCP servers.
- **Usage bundles** can be purchased to top up when you hit a wall.

---

## What to buy, for this track

| If you're doing | Buy |
|---|---|
| Stage 00–01 only | Nothing (free tier) |
| Stage 02 (power user) | Claude Pro |
| Stage 03 (Claude Code) | Claude Pro or Max — Max if you'll use it daily |
| Stage 04–06 (API) | Pro *and* ~$20 of Console credits |

The honest recommendation for most readers: start Free, get through stage 01, and buy Pro the moment you hit stage 02. Don't pre-buy Max — you'll know within a fortnight whether you need it, and the signal is unambiguous (you'll be getting told to wait).

---

## Try it

**Exercise 1.** Go to Settings → check which plan you're on and what your current usage looks like. Just locate it; you'll want to know where this lives when you eventually hit a limit.

**Exercise 2 — feel the cost of a long conversation.** Have a genuinely long chat (20+ turns) on one topic. Then start fresh and ask a question about that topic, pasting in only the three or four facts that matter. Notice the answer is at least as good — and that you've just done, by hand, the thing this whole track calls context management.

**Exercise 3 — pick your plan and say why.** Write one sentence in your prompt journal: which plan you're on, which you'll upgrade to, and what specific thing will trigger the upgrade. Vague intentions ("I'll upgrade if I need to") don't survive contact with a paywall; a named trigger does.

---

## Checkpoint

- You can explain why a Claude Pro subscription doesn't let you call the API
- You can name the three things that burn through your usage limits fastest
- You know which plan you need for the stage you're heading into next

---

## Going deeper

- [Choose a Claude plan](https://support.claude.com/en/articles/11049762-choose-a-claude-plan)
- [How do usage and length limits work?](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [API pricing and rate limits](../04-api/00-pricing-and-rate-limits.md) — stage 04, only if you're building
