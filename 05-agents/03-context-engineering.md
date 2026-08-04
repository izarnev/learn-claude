# 03 · Context engineering

**What you'll learn:** the discipline that separates agents that work for ten turns from agents that work for a thousand.

---

## The premise

Prompt engineering is about what you *say*. Context engineering is about what's *present* — what occupies the window, in what order, at what cost, and what gets removed when.

For agents this is the dominant concern, because an agent's context is not something you write once. It accumulates.

---

## The four operations

Every context engineering technique is one of these:

| Operation | Examples |
|---|---|
| **Add** | System prompt, tools, retrieval, files, tool results |
| **Order** | Long documents at the top, question at the bottom; stable prefix first for caching |
| **Compress** | Compaction, summarisation, subagent summaries |
| **Remove** | Context editing, clearing old tool results, starting fresh |

Most people only do the first. The other three are where the leverage is.

---

## Ordering

Two rules, both with measurable effects.

**Long material at the top, the question at the bottom.** Up to 30% quality improvement on complex multi-document inputs.

**Stable content first, volatile content last** — for prompt caching. Anything that changes per request must come after your cache breakpoint or you get no caching at all.

These agree with each other, which is convenient:

```
[ system prompt      ]  stable
[ tool definitions   ]  stable
[ reference docs     ]  stable    ← cache breakpoint
[ conversation       ]  grows
[ current message    ]  volatile
```

---

## Compression

### Compaction

The API offers built-in [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction) — summarise the conversation and continue.

Costs: a model call over the whole transcript, cache invalidation afterwards, and lossy summarisation.

### Subagent summarisation

Structurally the best compression available: the expensive reading happens in a context you throw away, and only the conclusion returns.

```
Main agent:      "Find every place we parse dates."   ← 200 tokens in, 400 out
Subagent:        reads 40 files                        ← 60,000 tokens, discarded
```

### Starting fresh with state files

Anthropic's guidance is worth quoting directly:

> When a context window is cleared, consider starting with a brand new context window rather than using compaction. Claude's latest models are extremely effective at discovering state from the local filesystem.

The pattern:

```
progress.txt     freeform notes on what's done and what's next
tests.json       structured status
git log          checkpoint history
```

And the restart prompt:

```
Call pwd; you can only read and write files in this directory.
Review progress.txt, tests.json, and the git log.
Manually run through a fundamental integration test before implementing
new features.
```

This beats compaction on long tasks: it's lossless in the ways that matter, inspectable by you, and it resets the context cost to near zero.

---

## Removal: context editing

Programmatically remove content from the conversation — most usefully, stale tool results. An agent that ran twenty searches doesn't need results 1–15 any more; it needs its conclusions.

See [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing).

---

## Context awareness

Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5 and Haiku 4.5 track their own remaining context budget. This changes their behaviour — they'll start wrapping up as they approach the limit.

If your harness handles that transition, tell Claude so it doesn't stop early:

```
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely from where you left off. Therefore,
do not stop tasks early due to token budget concerns. As you approach your token
budget limit, save your current progress and state to memory before the context
window refreshes. Always be as persistent and autonomous as possible and complete
tasks fully, even if the end of your budget is approaching. Never artificially
stop any task early regardless of the context remaining.
```

Without this, a capable agent will politely give up with 30% of its budget left.

---

## State management practices

From Anthropic's long-horizon guidance:

**Structured formats for structured data.**

```json
{
  "tests": [
    {"id": 1, "name": "authentication_flow", "status": "passing"},
    {"id": 2, "name": "user_management", "status": "failing"},
    {"id": 3, "name": "api_endpoints", "status": "not_started"}
  ],
  "total": 200, "passing": 150, "failing": 25, "not_started": 25
}
```

**Freeform text for progress notes.**

```
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

**Git for checkpoints.** Current models perform especially well using git to track state across sessions — it's a log *and* a set of restore points.

**Emphasise incremental progress.** Explicitly ask Claude to advance a few things at a time rather than attempting everything at once.

---

## The multi-window workflow

For tasks spanning several context windows:

1. **A different prompt for the first window.** Use it to build the framework: write tests, create `init.sh`, set up state files. Later windows iterate on a todo list.

2. **Tests in a structured format, written before the work.** And an explicit rule: *"It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."*

3. **Quality-of-life tooling.** `init.sh` that starts servers, runs the suite, runs linters — so a fresh context doesn't repeat setup.

4. **Verification tools.** Playwright, computer use, a test runner. An agent that can't verify can't be trusted to run long.

5. **Encourage full use of context:**
   > "It's encouraged to spend your entire output context working on the task — just make sure you don't run out of context with significant uncommitted work."

---

## Retrieval

When your knowledge exceeds the window:

**Give Claude search tools rather than dumping documents.** With a search tool, Claude retrieves what it needs when it needs it — which is both cheaper and more accurate than pre-loading everything and hoping the right thing is in there.

**Use the Citations feature** for anything where users need to verify claims. Sentence-level citations back to source documents, natively.

**Structure documents for retrieval.** Descriptive headings, one topic per file, no near-duplicates competing with each other.

---

## Measuring it

Instrument these:

| Metric | Why |
|---|---|
| Tokens per turn | Growth rate tells you when you'll hit the limit |
| Cache hit rate | Should be high and stable; drops mean something broke |
| Compaction frequency | Frequent compaction means your design is wrong |
| Subagent token share | Confirms isolation is working |
| Tool result size distribution | Usually where the surprise is |

That last one catches the most bugs. One tool returning 50,000 tokens per call will destroy an otherwise well-designed agent, and you won't notice until you measure.

---

## Try it

**Exercise 1 — Growth curve.**
Instrument tokens per turn on a real agent. Plot it. Identify the inflection point.

**Exercise 2 — Subagent isolation.**
Take a task that reads many files. Measure main-context growth with and without a subagent.

**Exercise 3 — Fresh vs compacted.**
Run a long task two ways: to compaction and beyond, versus state files plus a fresh session. Compare final quality and total cost.

**Exercise 4 — Tool result audit.**
Log the size of every tool result in a real agent run. Find the biggest. Fix it (paginate, summarise, return IDs).

**Exercise 5 — Persistence prompt.**
Run a long task with and without the context-awareness prompt. Note whether the agent stops early without it.

**Exercise 6 — Search vs dump.**
Build a QA system twice: once dumping all documents into context, once giving Claude a search tool. Compare cost and accuracy across twenty questions.

---

## Checkpoint

- You know all four operations and use more than "add"
- Your long-running agents keep state in files
- You measure tool result sizes

---

## Going deeper

- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)
- [Prompting best practices — agentic systems](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Explore the context window (interactive)](https://code.claude.com/docs/en/context-window)
