# 02 · The Claude landscape

**What you'll learn:** every place Claude exists, what each one is for, and how they relate — so you always know which door to walk through.

---

## The map

Anthropic ships Claude across four broad layers. They share the same underlying models but differ in what they can touch.

```
                        ┌──────────────────────────┐
                        │      Claude models       │
                        │  Fable 5 / Opus 5 /      │
                        │  Sonnet 5 / Haiku 4.5    │
                        └────────────┬─────────────┘
                                     │
        ┌────────────────┬───────────┴──────────┬──────────────────┐
        │                │                      │                  │
   ┌────▼────┐     ┌─────▼──────┐      ┌────────▼───────┐   ┌──────▼──────┐
   │  CHAT   │     │  AGENTIC   │      │  IN-APP        │   │  DEVELOPER  │
   │         │     │  DESKTOP   │      │  INTEGRATIONS  │   │  PLATFORM   │
   │ claude  │     │            │      │                │   │             │
   │ .ai     │     │ Cowork     │      │ Excel, Word,   │   │ Claude API  │
   │ mobile  │     │ Claude     │      │ PowerPoint,    │   │ Agent SDK   │
   │ desktop │     │ Code       │      │ Outlook, M365, │   │ Managed     │
   │ Projects│     │            │      │ Chrome, Slack, │   │ Agents      │
   │         │     │            │      │ Xcode          │   │ Console     │
   └─────────┘     └────────────┘      └────────────────┘   └─────────────┘
```

And cutting across all of them, four **extension mechanisms** you'll meet repeatedly:

- **Skills** — packaged instructions and workflows Claude loads on demand
- **MCP / Connectors** — a standard protocol for plugging Claude into external systems
- **Plugins** — bundles of skills, agents, hooks, and MCP servers, distributed via marketplaces
- **Memory** — persistent context across sessions

---

## Layer 1 — Chat

### claude.ai (web), desktop app, mobile app

The conversational interface. Same account, same conversations, synced across all three.

What lives here:

| Feature | What it does | Covered in |
|---|---|---|
| Conversations | The basic chat | [01-foundations/01](../01-foundations/01-your-first-conversation.md) |
| Artifacts | Live, rendered output — code, HTML, docs, diagrams | [01-foundations/05](../01-foundations/05-artifacts-and-file-creation.md) |
| File upload | PDFs, images, spreadsheets, code | [01-foundations/04](../01-foundations/04-files-and-vision.md) |
| File creation | Real .docx, .xlsx, .pptx, .pdf outputs | [01-foundations/05](../01-foundations/05-artifacts-and-file-creation.md) |
| Web search & Research | Live lookups; Research runs a multi-step investigation | [01-foundations/06](../01-foundations/06-search-and-research.md) |
| Memory & personalisation | Claude remembers preferences across chats | [01-foundations/07](../01-foundations/07-memory-and-personalisation.md) |
| Projects | A workspace with its own knowledge base and instructions | [02-power-user/01](../02-power-user/01-projects.md) |
| Skills | Custom, reusable capabilities | [02-power-user/02](../02-power-user/02-skills.md) |
| Connectors | MCP integrations to Gmail, Drive, Slack, Jira, etc. | [02-power-user/03](../02-power-user/03-connectors-and-mcp.md) |
| Claude Design | A canvas for design work | [02-power-user/05](../02-power-user/05-claude-in-your-apps.md) |
| Incognito chats | Conversations that don't persist | [01-foundations/07](../01-foundations/07-memory-and-personalisation.md) |

**Use it for:** thinking, writing, analysis, one-off questions, anything conversational.

---

## Layer 2 — Agentic desktop

Both of these give Claude a loop: it plans, acts, observes the result, and continues — without you approving every step.

### Claude Cowork

The non-developer agent. A visual interface where Claude works on multi-step tasks against your **local files** — research synthesis, file organisation, document generation — with visible progress and the ability to steer mid-task.

- Available on all paid plans (Pro, Max, Team, Enterprise)
- Full experience on the Claude Desktop app (macOS, Windows, Linux beta), where Claude can also use your local files and browser
- Also available on web and mobile for handing off and checking on tasks
- Supports Skills, Connectors, Plugins, scheduled tasks, and computer use

**Use it for:** "here is a folder, do a job with it" — no terminal, no code.

Covered in [02-power-user/04](../02-power-user/04-cowork.md).

### Claude Code

The developer agent. Reads your codebase, edits files, runs commands, and integrates with your dev tools.

Surfaces: terminal CLI, VS Code, JetBrains, desktop app, web (`claude.ai/code`), mobile, Slack, GitHub Actions, GitLab CI. **All surfaces share the same engine** — your CLAUDE.md, settings, and MCP servers work across every one of them.

**Use it for:** anything involving a repository.

Covered in all of [stage 03](../03-claude-code/).

> **Cowork vs Claude Code:** same underlying agentic engine, different audience. Cowork is file-and-document oriented with a GUI; Claude Code is repository oriented and code-native. If your task has a `git` directory in it, use Claude Code.

---

## Layer 3 — In-app integrations

Claude showing up where you already work.

| Integration | What it is |
|---|---|
| **Claude for Excel** | A spreadsheet agent inside Excel |
| **Claude for Word / PowerPoint / Outlook** | Office agents for docs, decks, and mail |
| **Microsoft 365** | Works across M365 apps, including with third-party platforms |
| **Claude in Chrome** | A browsing agent extension — navigates, fills forms, extracts data, debugs web apps |
| **Claude in Slack** | Mention `@Claude` in a channel; delegate coding tasks and get a PR back |
| **Claude in Xcode** | Apple-platform development |
| **Claude Security** | Security-focused workflows |

Covered in [02-power-user/05](../02-power-user/05-claude-in-your-apps.md).

---

## Layer 4 — Developer platform

### Claude API

Direct model access over HTTP. The Messages API is the core endpoint. Official SDKs in Python, TypeScript, Go, Java, C#, PHP, Ruby, plus an OpenAI-compatibility shim and a first-party CLI (`ant`).

Also available through Amazon Bedrock, Claude Platform on AWS, Google Cloud, and Microsoft Foundry.

Covered in [stage 04](../04-api/).

### Claude Agent SDK

Claude Code as a library. You get the agentic loop, the tool suite, hooks, permissions, subagents, skills, and session management — with full control over orchestration. Python and TypeScript.

Covered in [05-agents/02](../05-agents/02-agent-sdk.md).

### Managed Agents

Anthropic-hosted agents that run in a managed cloud sandbox. You define the agent; Anthropic runs it. Supports scheduled deployments, webhooks, memory stores, and multi-agent orchestration without you operating infrastructure.

Covered in [05-agents/05](../05-agents/05-managed-agents.md).

### Claude Console

The web dashboard at [platform.claude.com](https://platform.claude.com): API keys, workspaces, spend limits, usage analytics, the prompt workbench, and evaluation tooling.

---

## The cross-cutting mechanisms

These four appear at every layer. Learning them once pays off everywhere.

### Skills

A `SKILL.md` file with YAML frontmatter (`name`, `description`) plus optional bundled files and scripts. Claude loads the description always, the body when triggered, and bundled resources only when needed — **progressive disclosure**. Roughly 100 tokens per installed skill until it fires.

Works in: claude.ai (upload as zip), Cowork, Claude Code (`~/.claude/skills/` or `.claude/skills/`), the API (`skill_id` + code execution tool), Agent SDK, Managed Agents.

> Skills do **not** sync between surfaces. A skill uploaded to claude.ai is not available in the API or in Claude Code. Upload separately per surface.

### MCP (Model Context Protocol)

An open standard for connecting AI tools to external data and actions. In consumer products these are called **Connectors**. In Claude Code and the SDK they're **MCP servers**. Same protocol.

### Plugins

Installable bundles that can contain skills, subagents, hooks, MCP servers, and commands. Distributed through **marketplaces**. Available in Claude Code and in Cowork.

### Memory

- **claude.ai** — Claude remembers preferences and past context across chats; importable and exportable
- **Claude Code** — `CLAUDE.md` files you write, plus *auto memory* Claude writes for itself per repository
- **API / Managed Agents** — the memory tool and memory stores

---

## Choosing a door: a decision table

| Your situation | Go here |
|---|---|
| Ask a question, write something, analyse a document | claude.ai chat |
| Same task repeatedly, with the same background material | A Project |
| Same task repeatedly, with the same *procedure* | A Skill |
| "Here's a folder of files, do a job" | Cowork |
| Anything in a git repository | Claude Code |
| Data already in Excel | Claude for Excel |
| Something on a website, repeatedly | Claude in Chrome |
| Embed Claude in your own product | Claude API |
| Build an autonomous agent with tools | Agent SDK |
| Run agents without operating servers | Managed Agents |

---

## Try it

**Exercise 1.** Open [claude.ai](https://claude.ai) and find, in the UI: the model picker, the attachment button, the search/research toggles, and Settings → Features. Just locate them.

**Exercise 2.** Install the Claude Desktop app from [claude.com/download](https://claude.com/download). Note the three tabs: Chat, Cowork, Code.

**Exercise 3.** Take the three most repetitive things you do at work and place each one in the decision table above. Write the answers in your prompt journal. You'll revisit this at the end of stage 02.

## Checkpoint

Without looking, name: three surfaces where Skills work, the difference between a Connector and an MCP server, and when you'd pick Cowork over Claude Code.

## Going deeper

- [Where can I access Claude?](https://support.claude.com/en/articles/8461763-where-can-i-access-claude)
- [Claude Code overview](https://code.claude.com/docs/en/overview)
- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Browse skills, connectors, and plugins in one directory](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)
