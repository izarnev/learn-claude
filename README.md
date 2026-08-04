---
title: "Claude: Zero to Hero"
---

# Claude: Zero to Hero

A complete, step-by-step learning track for Claude — from "I've never typed a prompt" to "I ship production agents."

**Built:** August 2026 · **Sources:** live Anthropic docs (`platform.claude.com/docs`, `code.claude.com/docs`, `support.claude.com`)

---

## How this track is organised

Eight numbered folders. Each folder is a **stage**. Each file inside is a **module** with the same shape:

1. **What you'll learn** — the outcome, in one line
2. **Concepts** — the actual guide
3. **Try it** — hands-on exercises you can do immediately
4. **Checkpoint** — how you know you've got it
5. **Going deeper** — links to the official docs for the details this guide compresses

Modules are numbered in the order you should do them. Nothing later assumes anything you haven't already read.

```
learn-claude/
├── 00-start-here/     Orientation. What Claude is, where it lives, what plan you need.
├── 01-foundations/    Chat mastery. Prompting, models, files, artifacts, research.
├── 02-power-user/     No-code power. Projects, Skills, Connectors, Cowork, automation.
├── 03-claude-code/    Agentic coding. CLI, CLAUDE.md, subagents, hooks, MCP, plugins.
├── 04-api/            Building on Claude. Messages API, tools, caching, structured output.
├── 05-agents/         Agent engineering. Agent SDK, context engineering, multi-agent.
├── 06-production/     Shipping. Evals, guardrails, cost, observability, governance.
├── 07-capstones/      Five projects that prove you learned it.
└── 99-reference/      Cheat sheets, glossary, links. Come back to these forever.
```

---

## Learning paths

You do not have to do all of it. Pick the path that matches where you're going.

### Path A — "I just want to use Claude really well" (~6 hours)

`00-start-here` → `01-foundations` → `02-power-user` → capstone 1 & 2

You'll never touch code. You'll end up better at Claude than most engineers.

### Path B — "I want to code with Claude" (~15 hours)

Path A → `03-claude-code` → capstone 3

### Path C — "I want to build products on Claude" (~30 hours)

Path A (skim) → `03-claude-code` → `04-api` → `05-agents` → `06-production` → capstones 4 & 5

### Path D — "I'm technical, skip the basics"

`00-start-here/02-the-claude-landscape.md` → `01-foundations/02-prompting-fundamentals.md` → `01-foundations/03-models-and-modes.md` → then jump to `03-claude-code` or `04-api`.

---

## Full module index

### 00 · Start here

| # | Module | Why |
|---|--------|-----|
| 00 | [How to use this track](00-start-here/00-how-to-use-this-track.md) | Ground rules, how to practise |
| 01 | [What Claude actually is](00-start-here/01-what-claude-is.md) | Mental model: LLM, context, tokens |
| 02 | [The Claude landscape](00-start-here/02-the-claude-landscape.md) | Every surface, one map |
| 03 | [Plans, pricing, and limits](00-start-here/03-plans-and-pricing.md) | What you need to buy, and when |

### 01 · Foundations — chat mastery

| # | Module |
|---|--------|
| 01 | [Your first real conversation](01-foundations/01-your-first-conversation.md) |
| 02 | [Prompting fundamentals](01-foundations/02-prompting-fundamentals.md) |
| 03 | [Models, effort, and thinking](01-foundations/03-models-and-modes.md) |
| 04 | [Files, images, and vision](01-foundations/04-files-and-vision.md) |
| 05 | [Artifacts and file creation](01-foundations/05-artifacts-and-file-creation.md) |
| 06 | [Web search and Research](01-foundations/06-search-and-research.md) |
| 07 | [Memory and personalisation](01-foundations/07-memory-and-personalisation.md) |
| 08 | [Structured prompting with XML](01-foundations/08-structured-prompting.md) |

### 02 · Power user — no code required

| # | Module |
|---|--------|
| 01 | [Projects](02-power-user/01-projects.md) |
| 02 | [Skills](02-power-user/02-skills.md) |
| 03 | [Connectors and MCP, explained without code](02-power-user/03-connectors-and-mcp.md) |
| 04 | [Cowork](02-power-user/04-cowork.md) |
| 05 | [Claude inside your apps](02-power-user/05-claude-in-your-apps.md) |
| 06 | [Automation: scheduled tasks and routines](02-power-user/06-automation.md) |
| 07 | [Plugins](02-power-user/07-plugins.md) |
| 08 | [Advanced prompting patterns](02-power-user/08-advanced-prompting.md) |

### 03 · Claude Code — agentic coding

| # | Module |
|---|--------|
| 01 | [Install and first session](03-claude-code/01-install-and-first-session.md) |
| 02 | [How Claude Code works](03-claude-code/02-how-it-works.md) |
| 03 | [Everyday workflows](03-claude-code/03-everyday-workflows.md) |
| 04 | [Permissions, sandboxing, and safety](03-claude-code/04-permissions-and-safety.md) |
| 05 | [CLAUDE.md, rules, and memory](03-claude-code/05-claude-md-and-memory.md) |
| 06 | [Skills and slash commands](03-claude-code/06-skills-and-commands.md) |
| 07 | [Subagents, teams, and parallelism](03-claude-code/07-subagents-and-parallelism.md) |
| 08 | [Hooks](03-claude-code/08-hooks.md) |
| 09 | [MCP in Claude Code](03-claude-code/09-mcp.md) |
| 10 | [Plugins and marketplaces](03-claude-code/10-plugins-and-marketplaces.md) |
| 11 | [Context and cost management](03-claude-code/11-context-and-cost.md) |
| 12 | [Headless, CI, and automation](03-claude-code/12-headless-and-ci.md) |
| 13 | [Surfaces: desktop, web, IDE, Slack](03-claude-code/13-surfaces.md) |

### 04 · API — building on Claude

| # | Module |
|---|--------|
| 01 | [Setup and your first API call](04-api/01-setup-and-first-call.md) |
| 02 | [The Messages API in depth](04-api/02-messages-api.md) |
| 03 | [Thinking and effort](04-api/03-thinking-and-effort.md) |
| 04 | [Tool use](04-api/04-tool-use.md) |
| 05 | [Server tools and MCP connector](04-api/05-server-tools-and-mcp.md) |
| 06 | [Structured outputs](04-api/06-structured-outputs.md) |
| 07 | [Prompt caching](04-api/07-prompt-caching.md) |
| 08 | [Vision, PDFs, and the Files API](04-api/08-vision-pdfs-files.md) |
| 09 | [Streaming and batch processing](04-api/09-streaming-and-batch.md) |
| 10 | [Skills in the API](04-api/10-skills-in-the-api.md) |

### 05 · Agents

| # | Module |
|---|--------|
| 01 | [Agent design principles](05-agents/01-agent-design-principles.md) |
| 02 | [The Claude Agent SDK](05-agents/02-agent-sdk.md) |
| 03 | [Context engineering](05-agents/03-context-engineering.md) |
| 04 | [Multi-agent patterns](05-agents/04-multi-agent-patterns.md) |
| 05 | [Managed Agents](05-agents/05-managed-agents.md) |

### 06 · Production

| # | Module |
|---|--------|
| 01 | [Evals and testing](06-production/01-evals-and-testing.md) |
| 02 | [Guardrails and safety](06-production/02-guardrails.md) |
| 03 | [Cost and latency optimisation](06-production/03-cost-and-latency.md) |
| 04 | [Observability](06-production/04-observability.md) |
| 05 | [Enterprise and governance](06-production/05-enterprise-and-governance.md) |

### 07 · Capstones

[Five projects](07-capstones/README.md), one per stage, each with a spec and a done-check.

### 99 · Reference

| File | Use |
|------|-----|
| [Glossary](99-reference/glossary.md) | Every term in one place |
| [Model cheat sheet](99-reference/model-cheatsheet.md) | Which model, when, what it costs |
| [Prompting cheat sheet](99-reference/prompting-cheatsheet.md) | Copy-paste patterns |
| [Claude Code cheat sheet](99-reference/claude-code-cheatsheet.md) | Commands, flags, file layout |
| [API cheat sheet](99-reference/api-cheatsheet.md) | Request shapes and parameters |
| [Official links](99-reference/official-links.md) | Where to check when this goes stale |

---

## Three rules for getting through this

**1. Do the exercises.** Reading about prompting improves nothing. The gap between people who are good at Claude and people who aren't is almost entirely reps.

**2. Keep a scratch file.** Every time a prompt works surprisingly well, paste it into a notes file. In two weeks that file is worth more than this track.

**3. Assume this document is slightly out of date.** Claude ships weekly. Every module ends with links to the live docs. When something here disagrees with the docs, the docs win — and the changelogs are listed in [99-reference/official-links.md](99-reference/official-links.md).
