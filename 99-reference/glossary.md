---
title: "Glossary"
order: 1
---

# Glossary

Every term used in this track, defined once.

---

**Adaptive thinking** — `thinking: {type: "adaptive"}`. Claude decides when and how much to reason, calibrated by task complexity and the `effort` setting. Replaces extended thinking.

**Agent** — a system where the *model* decides the control flow, as opposed to a workflow where you do.

**Agent SDK** — Claude Code as a library (Python, TypeScript). Gives you the agentic loop, tools, hooks, permissions, subagents and sessions with full orchestration control.

**Agent team** — multiple independent Claude Code sessions that message each other and share a task list. Experimental; disabled by default.

**Agent view** — the Claude Code dashboard (`claude agents`) for monitoring and dispatching parallel background sessions.

**Agentic loop** — model reasons → calls a tool → harness executes → result returns to context → repeat. The mechanism behind every agent.

**Artifact** — (1) in chat, substantial content rendered in a side panel; (2) in Claude Code, session output published as a live shareable page.

**Auto memory** — notes Claude writes for itself, stored per repository at `~/.claude/projects/<project>/memory/`. Only the first 200 lines / 25KB of `MEMORY.md` loads at session start.

**Auto mode** — a Claude Code / Cowork permission mode where a background classifier evaluates each action for safety and blocks risky ones, rather than prompting for each.

**Batch API** — asynchronous request submission at a discount. The right choice for evals and bulk processing.

**Beta header** — `betas=["..."]`, required to enable pre-GA API features.

**Cache breakpoint** — a `cache_control` marker. Everything up to and including it is cached. Up to four per request.

**CLAUDE.md** — a markdown file Claude Code loads at session start, containing persistent project instructions. Target under 200 lines.

**Channels** — a mechanism for an MCP server to push events (webhooks, alerts, chat) into a running Claude Code session.

**Checkpointing** — tracking file changes so they can be rewound.

**Compaction** — summarising a conversation to free context space. Project-root CLAUDE.md is re-injected afterwards; nested ones and conversation-only instructions are not.

**Connector** — the consumer-app name for an MCP server integration.

**Constrained decoding** — the mechanism behind structured outputs: the model literally cannot produce schema-violating output.

**Context editing** — programmatically removing content from a conversation, typically stale tool results.

**Context engineering** — managing what occupies the context window: adding, ordering, compressing, removing.

**Context awareness** — some models (Sonnet 5, 4.6, 4.5, Haiku 4.5) track their own remaining token budget during a conversation.

**Context window** — everything Claude can see at once. 1M tokens on current frontier models, 200k on Haiku 4.5.

**Cowork** — Claude's agentic interface for non-developers. Multi-step tasks over local files, with cloud-run sessions. Paid plans only.

**Dynamic workflow** — a script Claude writes that orchestrates many subagents; inspectable and rerunnable.

**Effort** — `output_config.effort`. How much internal work Claude does before responding. Defaults to `high` on the API for Opus 5 and Sonnet 5.

**Extended thinking** — the legacy `thinking: {type: "enabled", budget_tokens: N}`. Deprecated; returns a 400 on Claude 4.7+.

**Few-shot / multishot prompting** — giving 3–5 examples to steer format, tone and structure.

**Files API** — upload a file once, reference it by ID. Required for getting files in and out of the code execution container.

**Fork** — branching a session so you can explore alternatives from the same state without altering the original.

**Grounding** — requiring answers to come only from supplied sources, ideally with quotes extracted first.

**Hook** — a command, HTTP request, LLM prompt, or subagent that fires at a Claude Code lifecycle event. Deterministic, unlike instructions.

**LLM-as-judge** — using a model to grade outputs against a rubric. Requires calibration against human scores.

**Managed Agents** — Anthropic-hosted agents running in a managed cloud sandbox, with sessions, memory stores, scheduling and webhooks handled for you.

**Managed settings** — organisation-level configuration enforced by the client regardless of user settings.

**Marketplace** — a hosted collection of plugins.

**MCP (Model Context Protocol)** — an open standard for connecting AI tools to external systems. Servers expose tools; clients call them.

**MCP tunnel** — enterprise connectivity for MCP servers inside your network, reachable by Anthropic-hosted surfaces.

**Memory tool** — an Anthropic-defined but client-executed tool giving Claude persistent memory across sessions; you implement the storage backend.

**Multishot** — see few-shot.

**Namespacing** — plugin skills are invoked as `/plugin:skill` so multiple plugins coexist.

**Orchestrator–worker** — the dominant multi-agent pattern: an orchestrator plans and synthesises, workers do isolated subtasks.

**Output style** — a Claude Code mechanism for adapting the assistant's persona and defaults for non-coding uses.

**Path-scoped rule** — a `.claude/rules/*.md` file with `paths` frontmatter, loading only when Claude touches matching files.

**Permission mode** — `default`/`manual`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. Cycle with `Shift+Tab`.

**Plan mode** — Claude proposes without editing. The highest-value habit in Claude Code.

**Plugin** — an installable bundle of skills, subagents, hooks, MCP servers, commands and themes.

**Prefill** — supplying a partial assistant message to continue from. **No longer supported** on Claude 4.6+; returns a 400.

**Programmatic tool calling** — Claude writes code that calls your tools, rather than individual tool_use round trips.

**Progressive disclosure** — the Skills loading model: metadata always (~100 tokens), instructions when triggered, resources only when read.

**Prompt caching** — caching a stable prefix server-side so repeat requests read it at a fraction of the cost.

**Prompt injection** — an attack where content Claude reads contains instructions aimed at redirecting it.

**RAG (retrieval-augmented generation)** — retrieving relevant chunks and putting them in context, rather than loading everything. How Project knowledge bases work above a size threshold.

**Routine** — a Claude Code automation running on Anthropic-managed infrastructure, triggerable by schedule, API call, or GitHub event.

**Rules** — `.claude/rules/*.md`. Modular instructions, optionally path-scoped.

**Sandbox** — an isolated execution environment. Claude Code's sandboxed Bash tool provides filesystem and network isolation.

**Server tool** — a tool Anthropic executes for you (web search, web fetch, code execution, tool search, advisor), as opposed to a client tool you implement. Bash, text editor, and memory have Anthropic-defined schemas but are client-executed, not server tools; computer use can be either depending on setup.

**Service tier** — an API setting trading latency against throughput and priority.

**Session** — a persisted conversation. Continue, resume, or fork it.

**Skill** — a `SKILL.md` file with frontmatter plus optional bundled files and scripts, loaded on demand.

**Stop reason** — why generation ended: `end_turn`, `max_tokens`, `tool_use`, `stop_sequence`, `refusal`.

**Strict tool use** — `strict: true`. Guarantees tool names and inputs validate against their schemas.

**Structured outputs** — `output_config.format`. Guarantees the response matches a JSON Schema, via constrained decoding.

**Subagent** — an isolated worker with its own context window. Only its summary returns to the caller.

**Surface** — a place Claude Code runs: terminal, VS Code, JetBrains, desktop, web, mobile, Slack, CI.

**System prompt** — a top-level `system` parameter (not a message) setting role and standing instructions.

**Token** — the unit Claude reads and is billed in. Roughly 3–4 characters in English; ~750 words ≈ 1,000 tokens.

**Tool** — a function description Claude can request to call. Claude never executes; the harness does.

**Tool search** — loading only the tools needed on demand, so large tool sets don't fill context. On by default in Claude Code.

**Trajectory evaluation** — grading an agent's *path*, not just its final answer.

**Ultraplan / ultrareview** — cloud-based deep planning and deep multi-agent code review in Claude Code.

**WIF (Workload Identity Federation)** — API access without long-lived keys, using your existing identity provider.

**Workspace** — a Console-level container with its own API keys, budget and rate limits.

**Worktree** — an isolated git working directory. `claude -w <name>` runs a session in one.

**ZDR (Zero Data Retention)** — available to qualified Enterprise accounts, with documented feature trade-offs. Agent Skills are **not** covered.

---

Anthropic's own glossaries: [platform](https://platform.claude.com/docs/en/about-claude/glossary) · [Claude Code](https://code.claude.com/docs/en/glossary)
