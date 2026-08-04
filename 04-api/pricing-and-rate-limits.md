---
title: "API pricing and rate limits"
order: 0
---

# API pricing and rate limits

> **You are here** · Paths C and D · Needs a [Claude Console](https://platform.claude.com) account (no credits yet) · 40–60 min · Assumes you've read [What Claude actually is](../00-start-here/what-claude-is.md) and know what a token is.
>
> **Not on Path A or B?** Skip this. Nothing in stages 00–03 needs it. If you only use claude.ai, the desktop app, Cowork, or Claude Code on a subscription, your costs are covered by [Plans and pricing](../00-start-here/plans-and-pricing.md) and none of the below applies to you.

**What you'll learn:** what API usage costs, the three levers that change that cost by an order of magnitude, and how rate limits will bite you.

---

## If you only read one thing

You pay per token, in and out, and output costs 5× what input costs. The model you pick matters far more than the prompt you write — the same job on Haiku versus Opus is a 5× cost difference for identical inputs. Before you write anything that loops, set a spend limit in the Console, because the way people get a surprise bill is never one expensive call; it's an agent that ran 400 times against a large context. Separately from cost, the API caps how fast you can send requests, so any real workload needs retry logic.

---

## The details

### Prices per million tokens (MTok), August 2026

| Model | Input | Output | Context | Notes |
|---|---|---|---|---|
| Claude Fable 5 | $10 | $50 | 1M | Most capable; thinking always on |
| Claude Opus 5 | $5 | $25 | 1M | Complex agentic coding, enterprise |
| Claude Sonnet 5 | $3 | $15 | 1M | Best speed/intelligence balance |
| Claude Haiku 4.5 | $1 | $5 | 200k | Fastest |

> Claude Sonnet 5 has introductory pricing of **$2 / $10** per MTok through 31 August 2026.

> ⚠️ These figures are a snapshot. Verify against the [API pricing page](https://platform.claude.com/docs/en/about-claude/pricing) before you make a decision that depends on them.

### The three discounts that matter

1. **Prompt caching.** Cache a large, stable prefix (system prompt, documents, tool definitions) and reads against it cost a fraction of normal input. For agents that resend the same context every turn, this is often a 70–90% saving. See [Prompt caching](prompt-caching.md).
2. **Batch API.** Submit work asynchronously for a substantial discount. Perfect for evals, bulk classification, and offline processing. See [Streaming and batch processing](streaming-and-batch.md).
3. **Model routing.** Use Haiku for classification and extraction, Sonnet for the bulk of work, Opus only where it changes the outcome. At list prices Haiku is 3× cheaper than Sonnet, 5× cheaper than Opus, and 10× cheaper than Fable.

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

Covered in [Enterprise and governance](../06-production/enterprise-and-governance.md).

---

## Try it

**Exercise 1.** Open [platform.claude.com](https://platform.claude.com), create an account, and find: API keys, Workspaces, and where spend limits live. Don't add credits yet.

**Exercise 2 — cost arithmetic.** You're building a tool that summarises 500 documents per day. Each doc is 8,000 input tokens; each summary is 500 output tokens. That's 4M input tokens and 250k output tokens per day. Compute the daily cost on Haiku 4.5, Sonnet 5, and Opus 5.

<details>
<summary>Worked answer</summary>

The formula is `(input tokens ÷ 1,000,000 × input price) + (output tokens ÷ 1,000,000 × output price)`.

| Model | Input | Output | Daily total |
|---|---|---|---|
| Haiku 4.5 | 4 × $1 = $4.00 | 0.25 × $5 = $1.25 | **$5.25** |
| Sonnet 5 (list) | 4 × $3 = $12.00 | 0.25 × $15 = $3.75 | **$15.75** |
| Sonnet 5 (intro, until 31 Aug 2026) | 4 × $2 = $8.00 | 0.25 × $10 = $2.50 | **$10.50** |
| Opus 5 | 4 × $5 = $20.00 | 0.25 × $25 = $6.25 | **$26.25** |

Two things to notice. Model choice moves the cost 5× while the prompt itself barely matters — and the promotional Sonnet price is a third off, which is enough to change a build-or-not decision, so always check the live pricing page rather than a table in a guide.

</details>

**Exercise 3 — set a spend limit.** Before you add credits, find the spend limit setting and decide what number would make you comfortable letting an agent run unattended overnight. Write it down. Set it when you fund the account.

---

## Checkpoint

- You can name the three biggest levers on API cost
- You can compute the daily cost of a workload from token counts and a price table
- You know what a 429 is and what to do about it

---

## Going deeper

- [API pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Cost and latency optimisation](../06-production/cost-and-latency.md)
