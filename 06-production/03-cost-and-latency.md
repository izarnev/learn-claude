# 03 · Cost and latency optimisation

**What you'll learn:** the levers, ranked, so you optimise the thing that actually matters.

---

## Measure before optimising

You cannot optimise what you haven't measured. Before anything else, instrument:

| Metric | Why |
|---|---|
| Input / output tokens per request | The bill |
| Cache creation / read tokens | Whether caching works |
| Cost per request, by endpoint | Where the money goes |
| Latency: time-to-first-token and total | Different problems, different fixes |
| Requests per user per day | Growth projections |
| Server tool usage (searches, container time) | Hidden cost |
| Turn count distribution for agents (p50, **p95**) | The mean hides the runaway |

Most cost surprises are a single endpoint nobody looked at, or a p95 that's ten times the mean.

---

## Cost levers, ranked

### 1. Model selection — usually 3–25×

| Model | Input | Output |
|---|---|---|
| Fable 5 | $10 | $50 |
| Opus 5 | $5 | $25 |
| Sonnet 5 | $3 | $15 |
| Haiku 4.5 | $1 | $5 |

The composite pattern:

```
Haiku    → classify, extract, route, tag
Sonnet   → the bulk of the work
Opus     → only the cases Haiku flagged as hard
```

Typical result: 60–80% cost reduction with equal or better quality, because the hard cases get *more* attention, not less.

Also configure `--fallback-model` / `fallbackModel` so an overloaded primary doesn't stall you.

### 2. Prompt caching — 70–90% on input

For any stable prefix over ~2k tokens used repeatedly. See [04-api/07](../04-api/07-prompt-caching.md).

The check: is `cache_read_input_tokens` non-zero on repeat calls? If not, something in your prefix changes per request.

### 3. Batch API — substantial discount

For anything offline: evals, bulk classification, backfills, synthetic data. Combine with caching.

### 4. Effort tuning

Lower effort means fewer thinking tokens. Mechanical work doesn't need `high`. On Opus 5 and Sonnet 5, effort defaults to `high` on the API — so this is an opt-out, not an opt-in.

### 5. Prompt length

Every input token is paid on every turn. Audit your system prompt: how much of it earns its place? Few-shot examples are valuable but expensive — measure whether five examples beat three.

### 6. Output length

Output costs 5× input. If you're generating more than you need, say so:

```
Answer in under 100 words.
```

Note on Opus 5: it defaults to longer responses than prior models, and changing effort does *not* reliably change visible length. Prompt for conciseness explicitly.

### 7. Context management

For agents: subagents for isolation, context editing to drop stale tool results, state files instead of compaction. See [05-agents/03](../05-agents/03-context-engineering.md).

### 8. Tool result size

Frequently the hidden cost. One tool returning 50,000 tokens per call will dominate everything else. Paginate, summarise, return IDs.

### 9. Caching your own results

Identical or near-identical requests don't need to hit the model at all. A simple response cache keyed on normalised input catches more traffic than people expect.

---

## Latency levers, ranked

### 1. Model

Haiku is dramatically faster than Opus. If latency is user-facing, this is your first move.

### 2. Effort

Less thinking, faster response.

### 3. Streaming

Doesn't reduce total time; transforms perceived time. Time-to-first-token drops from seconds to hundreds of milliseconds. For anything a human watches, this is the highest-impact change available.

### 4. Prompt caching

A cache hit skips reprocessing the prefix — real latency reduction, not just cost.

### 5. Prompt length

Fewer input tokens means faster time-to-first-token.

### 6. `max_tokens`

If you set 4096 and need 200, you're not paying for the difference — but a model that generates 4000 tokens takes longer than one that generates 200. Constrain the output in the prompt.

### 7. Parallelisation

Independent calls in parallel, not chained. Also applies within a single call — current models call independent tools in parallel by default.

### 8. Service tiers

Trade throughput and priority. See [Service tiers](https://platform.claude.com/docs/en/api/service-tiers).

Anthropic's guide: [Reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency).

---

## Agent-specific cost control

Agents are where costs run away, because turn count is variable.

**Hard caps:**

```bash
claude -p --max-budget-usd 5.00 --max-turns 20 "task"
```

Subagent spend counts toward the budget cap, and hitting it stops running background subagents.

**Model per subagent.** Mechanical workers on Haiku.

**Restrict tools.** Fewer tools means less wandering.

**Termination conditions.** An agent without a clear "done" oscillates expensively.

**Watch p95, not the mean.** The mean turn count tells you about normal operation. The p95 tells you about your bill.

---

## Organisational controls

| Control | Where |
|---|---|
| Workspaces with separate budgets | Console |
| [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api) | Per-developer or per-group caps |
| [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api) | Pull into your own dashboards |
| [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api) | Adoption and usage patterns |
| [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api) | Team Claude Code usage |
| Gateway spend limits | Per-developer daily/weekly/monthly caps enforced live |

For Claude Code specifically: `/usage` shows what's driving plan limits, broken down by skills, subagents and MCP servers.

---

## A worked example

A support system handling 10,000 tickets/day, 3,000 input tokens and 500 output tokens each.

| Configuration | Daily cost |
|---|---|
| Everything on Opus 5 | $275 |
| Everything on Sonnet 5 | $165 |
| Sonnet 5 with prompt caching (80% of input cached) | ~$100 |
| Haiku classify → Sonnet respond, with caching | ~$45 |
| Same, plus 20% response cache hit rate | ~$36 |

Same quality — arguably better, since the hard cases can now afford Opus. **7.6× reduction**, entirely from architecture rather than prompt golf.

---

## The optimisation loop

```
1. Measure. Find the top cost or latency contributor.
2. Change one thing.
3. Re-measure cost AND quality (your eval set).
4. Keep or revert.
5. Repeat.
```

Step 3 is the one people skip. A change that halves cost and drops accuracy 15% is usually a bad trade — but you can only know that if you have evals.

---

## Try it

**Exercise 1 — Instrument.**
Add full cost and latency logging to something real. Run for a week. Find the top three contributors.

**Exercise 2 — Routing.**
Implement Haiku classification with escalation. Measure cost and quality against your eval set.

**Exercise 3 — Caching.**
Add caching to your largest stable prefix. Verify with `cache_read_input_tokens`. Compute the saving.

**Exercise 4 — Latency ladder.**
Take your slowest endpoint. Apply the eight latency levers one at a time, measuring after each. Find which two mattered.

**Exercise 5 — p95.**
For an agent, report p50 and p95 turn count and cost. If p95 is more than 3× p50, find out why.

**Exercise 6 — Tool result audit.**
Log every tool result size. Find the biggest. Fix it.

---

## Checkpoint

- You know your cost per request and where it goes
- You measure quality alongside cost on every optimisation
- Your agents have hard spend and turn caps
- You've looked at p95, not just the mean

---

## Going deeper

- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [Reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency)
- [Effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Manage costs effectively (Claude Code)](https://code.claude.com/docs/en/costs)
- [Track cost and usage (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/cost-tracking)
