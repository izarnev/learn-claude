# 04 · Observability

**What you'll learn:** what to log so that when something breaks at 2am, you can find out why.

---

## The problem

LLM systems fail differently from ordinary software. There's no stack trace. The system returns a plausible answer that happens to be wrong, or takes forty turns instead of four, or silently stops caching.

**You cannot debug what you didn't record.** And you can't retroactively record it.

---

## What to log, per request

| Field | Why |
|---|---|
| Request ID | Correlation |
| Timestamp | Obviously |
| Model and parameters | The most common cause of "it changed" |
| System prompt version / hash | Which prompt produced this |
| Input (or a hash, if sensitive) | Reproduction |
| Output | What actually happened |
| `stop_reason` | Truncation and refusals hide here |
| `usage` — all fields including cache | Cost and cache health |
| Latency: TTFT and total | Two different problems |
| Errors and retries | |
| User / tenant ID | Per-customer analysis |

**Prompt versioning is the one people skip.** Without it, "did the model get worse or did we change the prompt?" is unanswerable. Hash your prompt and log the hash.

---

## What to log, per tool call

| Field | Why |
|---|---|
| Tool name | |
| Input | Reproduction |
| Output **size** | The most common hidden cost |
| Success or error, and the error text | Whether Claude could self-correct |
| Duration | Which tool is slow |

Tool result size is the field that catches the most bugs. One tool returning 50,000 tokens per call will destroy an otherwise well-designed agent, and it's invisible until you measure it.

---

## What to log, per agent run

| Field | Why |
|---|---|
| Turn count | The runaway signal |
| Total cost | |
| Termination reason | Done? Cap hit? Error? Gave up? |
| Full trajectory — every turn's tools and decisions | The only way to debug |
| Parent-child relationships for subagents | Reconstructing the tree |
| Whether verification ran and passed | Did it check its own work? |

---

## Distributed tracing

Model the request as a trace:

```
trace: user request
├── span: retrieval
├── span: model call 1
│   ├── span: tool call — search
│   └── span: tool call — fetch
├── span: model call 2
│   └── span: subagent
│       ├── span: model call
│       └── span: tool call
└── span: response
```

Attach tokens, cost and latency to each span. Now a slow request is a picture rather than a mystery.

**OpenTelemetry** is the standard, and both Claude Code and the Agent SDK support it:

- [Monitoring (Claude Code)](https://code.claude.com/docs/en/monitoring-usage)
- [Observability with OpenTelemetry (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/observability)
- [Monitor Claude Cowork activity with OpenTelemetry](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry)

---

## Dashboards worth having

**Health**
- Request rate, error rate, p50/p95/p99 latency
- Refusal rate
- Truncation rate (`stop_reason == "max_tokens"`)

**Cost**
- Cost per hour, per endpoint, per tenant
- **Cache hit rate** — a sudden drop means someone broke the prefix
- Token distribution — the tail matters more than the mean

**Quality**
- Continuous eval scores if you run them against production samples
- User feedback rate, if you collect it
- Escalation-to-human rate
- Low-confidence output rate

**Agents**
- Turn count distribution (p50, **p95**)
- Termination reasons
- Cost per run, p50 and p95
- Subagent spawn rate

---

## Alerts that earn their place

| Alert | Threshold |
|---|---|
| Error rate spike | Above your normal band |
| Cost per hour above budget | Set it low enough to catch it same-day |
| **Cache hit rate drop** | A silent, expensive failure |
| p95 latency regression | |
| Truncation rate above baseline | You changed something |
| Agent turn count p95 above a ceiling | Runaway detection |
| Refusal rate spike | Either an attack or a prompt regression |

The cache hit rate alert is the one people don't think of and then wish they had.

---

## Sampling and privacy

You probably can't log every input verbatim.

Options:

- **Hash inputs** and store full text only for a sampled subset
- **Redact** PII before logging
- **Short retention** on full text, long retention on metrics
- **Tenant-scoped storage** if you have data residency obligations

Decide this before you start logging, not after your first compliance conversation.

Related: [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention), and [Zero data retention](https://code.claude.com/docs/en/zero-data-retention) for qualified Enterprise accounts.

---

## Continuous evaluation

Run your eval set against production regularly — not just before deploys.

Better: sample real production traffic, grade it (programmatically where possible, LLM-judge otherwise), and track the score over time. Model updates, data drift and prompt edits all show up here before users complain.

---

## Debugging playbook

**"Quality got worse."**
1. Did the prompt change? (Check your prompt version log.)
2. Did the model change? (Pinned model IDs prevent this — check you pinned.)
3. Did the input distribution change?
4. Run your eval set. Compare against the last known-good run.

**"It got expensive."**
1. Cache hit rate — first thing to check.
2. Token distribution — is the tail growing?
3. For agents: turn count p95.
4. Tool result sizes.
5. Server tool usage (searches, container hours).

**"It's slow."**
1. TTFT or total? Different problems.
2. Cache hit rate.
3. Which span is slow — model call, tool call, or your own code?
4. Are you chaining calls that could be parallel?

**"The agent did something weird."**
1. Read the full trajectory.
2. What was in context at the turn where it went wrong?
3. Did a tool return something unexpected?
4. Was there injected content in a tool result?

---

## Try it

**Exercise 1 — Log everything.**
Add complete request logging to something real. Include prompt version. Run for a week.

**Exercise 2 — Trace.**
Build a distributed trace for one multi-step request. Look at it. Note where the time actually goes — it's rarely where you assumed.

**Exercise 3 — Cache alert.**
Set up a cache hit rate metric and alert. Then deliberately break the cache and confirm the alert fires.

**Exercise 4 — Trajectory review.**
Take ten agent runs. Read the full trajectories. Note how many did something you didn't expect but that happened to work.

**Exercise 5 — Continuous eval.**
Sample production traffic daily, grade it, track the score. After a month you'll have a curve nobody else on your team has.

---

## Checkpoint

- Every model call logs model, prompt version, stop reason, and full usage
- You have a cache hit rate metric and an alert on it
- You can reconstruct a full agent trajectory from logs
- You track quality over time, not just at deploy

---

## Going deeper

- [Monitoring (Claude Code)](https://code.claude.com/docs/en/monitoring-usage)
- [Observability with OpenTelemetry (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/observability)
- [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api)
- [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api)
- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
