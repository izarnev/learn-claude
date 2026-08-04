---
title: "03 · Plans, pricing, and limits"
---

# 03 · Plans, pricing, and limits

**What you'll learn:** what to pay for, when, and how usage limits actually behave — so you don't get blocked mid-task or overspend on the API.

> ⚠️ Prices and limits change. Verify against [claude.com/pricing](https://claude.com/pricing) and the [API pricing page](https://platform.claude.com/docs/en/about-claude/pricing) before making a decision. Figures below are as of August 2026.

---

## Two entirely separate billing systems

This confuses almost everyone at first.

| | Subscription | API |
|---|---|---|
| **Where** | claude.ai, desktop, mobile, Cowork, Claude Code | platform.claude.com |
| **You buy** | A monthly plan | Prepaid credits |
| **You're limited by** | Usage windows that reset | Your credit balance and rate limits |
| **Good for** | Using Claude | Building on Claude |

A Pro subscription gives you nothing on the API. API credits give you nothing on claude.ai. Claude Code is the one product that works with *either*.

---

## Subscription plans

| Plan | Roughly for | Key unlocks |
|---|---|---|
| **Free** | Trying it out | Chat, limited usage, basic features |
| **Pro** | Individuals | Higher limits, Projects, custom Skills, Cowork, connectors, Claude Code, file creation |
| **Max** | Heavy individual users | Substantially higher limits, priority access to new features |
| **Team** | Small orgs | Everything in Pro plus collaboration, shared projects, central billing |
| **Enterprise** | Large orgs | SSO, audit, compliance controls, zero data retention options, admin APIs |

**The features that require paid:** Projects, Cowork, connectors, code execution / file creation, Claude Code on a subscription.

> **Note:** Skills are available on Free as well as paid plans — but they require code execution to be enabled, which is a paid feature. In practice you need Pro or above.

### How usage limits work

Limits are enforced on rolling windows, not a simple monthly quota. Practical implications:

- **Model choice moves the needle most.** Opus consumes limits far faster than Sonnet, which consumes faster than Haiku.
- **Long conversations are expensive.** Every turn resends the whole transcript. Starting a fresh chat for a new topic is the cheapest optimisation you have.
- **Agentic work is the heaviest thing you can do.** Claude Code and Cowork make many model calls per task.
- **Run `/usage` in Claude Code** to see what's driving your limits, broken down by skills, subagents, and MCP servers.
- **Usage bundles** can be purchased to top up when you hit a wall.

---

## API pricing

Per million tokens (MTok), August 2026:

| Model | Input | Output | Context | Notes |
|---|---|---|---|---|
| Claude Fable 5 | $10 | $50 | 1M | Most capable; thinking always on |
| Claude Opus 5 | $5 | $25 | 1M | Complex agentic coding, enterprise |
| Claude Sonnet 5 | $3 | $15 | 1M | Best speed/intelligence balance |
| Claude Haiku 4.5 | $1 | $5 | 200k | Fastest |

> Claude Sonnet 5 has introductory pricing of **$2 / $10** per MTok through 31 August 2026.

### The three discounts that matter

1. **Prompt caching.** Cache a large, stable prefix (system prompt, documents, tool definitions) and reads against it cost a fraction of normal input. For agents that resend the same context every turn, this is often a 70–90% saving. See [04-api/07](../04-api/07-prompt-caching.md).
2. **Batch API.** Submit work asynchronously for a substantial discount. Perfect for evals, bulk classification, and offline processing. See [04-api/09](../04-api/09-streaming-and-batch.md).
3. **Model routing.** Use Haiku for classification and extraction, Sonnet for the bulk of work, Opus only where it changes the outcome. Haiku is 5× cheaper than Sonnet and 25× cheaper than Fable.

### What things actually cost — rough intuition

| Task | Model | Ballpark |
|---|---|---|
| Summarise a 10-page doc | Sonnet 5 | under a cent |
| Classify 1,000 support tickets | Haiku 4.5 | ~$1–3 |
| A serious Claude Code refactoring session | Opus 5 | $1–10 |
| Long-running agent, thousands of turns | Opus 5 | $10s–$100s |

The failure mode is never "one call was expensive." It's "an agent looped 400 times on a 200k-token context." Set spend limits before you write your first loop.

---

## Rate limits

Separate from cost. The API limits requests per minute and tokens per minute, by tier. Tiers increase as your spend history grows.

Handle them properly:

- Respect the `retry-after` header on 429s
- Use exponential backoff with jitter
- Use the Batch API for anything that doesn't need to be synchronous
- Check current limits in the Console, or query the [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api)

**Service tiers** let you trade latency for throughput or priority — see [Service tiers](https://platform.claude.com/docs/en/api/service-tiers).

---

## Enterprise controls

If you're deploying to a team, these exist and are worth knowing about early:

- **Workspaces** — separate API keys, budgets, and rate limits per project
- **Spend Limits API** — programmatic caps per developer or group
- **Usage and Cost API / Analytics APIs** — pull consumption data into your own dashboards
- **Admin API** — manage users, roles, groups, and service accounts
- **Zero Data Retention** — available for qualified Enterprise accounts, with feature trade-offs
- **Customer-managed encryption keys** — AWS KMS, Azure Key Vault, Google Cloud KMS
- **Workload Identity Federation** — API access without long-lived keys

Covered in [06-production/05](../06-production/05-enterprise-and-governance.md).

---

## What to buy, for this track

| If you're doing | Buy |
|---|---|
| Stage 00–01 only | Nothing (free tier) |
| Stage 02 (power user) | Claude Pro |
| Stage 03 (Claude Code) | Claude Pro or Max — Max if you'll use it daily |
| Stage 04–06 (API) | Pro *and* ~$20 of Console credits |

---

## Try it

**Exercise 1.** Go to Settings → check which plan you're on and what your current usage looks like.

**Exercise 2.** Open [platform.claude.com](https://platform.claude.com), create an account, and find: API keys, Workspaces, and where spend limits live. Don't add credits yet.

**Exercise 3 — cost arithmetic.** You're building a tool that summarises 500 documents per day. Each doc is 8,000 input tokens; each summary is 500 output tokens. Compute daily cost on Haiku 4.5, Sonnet 5, and Opus 5. *(Answer: Haiku ≈ $5.25, Sonnet ≈ $15.75, Opus ≈ $26.25.)* Note how the model choice, not the prompt, dominates.

## Checkpoint

You can explain why a Claude Pro subscription doesn't let you call the API, and name the three biggest levers on API cost.

## Going deeper

- [Choose a Claude plan](https://support.claude.com/en/articles/11049762-choose-a-claude-plan)
- [How do usage and length limits work?](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
