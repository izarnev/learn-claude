---
title: "02 · The Claude Agent SDK"
---

# 02 · The Claude Agent SDK

**What you'll learn:** how to use Claude Code as a library, so you don't rebuild the agentic loop yourself.

---

## What it gives you

The Agent SDK is Claude Code's engine, available as a Python and TypeScript library. You get, for free:

- The agentic loop
- The full built-in tool suite (file operations, search, bash, web)
- Permissions and permission modes
- Hooks
- Subagents
- Skills
- Session management, persistence, and forking
- File checkpointing
- MCP integration and tool search
- Structured outputs
- Cost tracking
- OpenTelemetry observability

You control orchestration, tool access, and permissions.

**Choose the SDK over raw Messages API when** your agent needs to work with files, run commands, or do multi-step tool work — which is most agents. Choose raw Messages API when you need one call, or total control over the loop.

---

## Quickstart

```bash
pip install claude-agent-sdk
npm install @anthropic-ai/claude-agent-sdk
```

```python
from claude_agent_sdk import query

async for message in query(prompt="Analyse the codebase and list the three biggest tech debt items"):
    print(message)
```

The [quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart) covers both languages properly.

---

## The pieces you'll configure

### System prompt

Four starting points, and the choice matters:

| Option | When |
|---|---|
| `claude_code` preset | Your agent is a coding assistant |
| Preset + `append` | Coding assistant with extra rules — **keeps default tool guidance and safety instructions** |
| CLAUDE.md loading | Project conventions come along |
| Fully custom | The identity or permission model is genuinely different |

Replacing drops everything including safety instructions. Prefer appending unless you have a reason.

See [Modifying system prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts).

### Permissions

```python
options = ClaudeAgentOptions(
    permission_mode="acceptEdits",
    allowed_tools=["Read", "Grep", "Bash(npm test)"],
    disallowed_tools=["Bash(git push*)"],
)
```

Plus a `canUseTool` callback for programmatic decisions, and hooks for enforcement. See [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions).

### Custom tools

The SDK includes an **in-process MCP server**, so you define tools as plain functions — no separate process:

```python
@tool("query_orders", "Query the orders database. Use when asked about order history, status, or totals.")
async def query_orders(customer_id: str, since: str | None = None) -> str:
    ...
```

Much simpler than writing a standalone MCP server. See [Give Claude custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools).

### Subagents

Define specialised workers with their own context, tools, and instructions. Same model as Claude Code's subagents. See [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents).

### Hooks

Intercept behaviour at the same lifecycle points as Claude Code. Use for enforcement, logging, and injecting context. See [Hooks](https://code.claude.com/docs/en/agent-sdk/hooks).

### Skills

Load skills into SDK agents, including your existing Claude Code skills. See [Agent Skills in the SDK](https://code.claude.com/docs/en/agent-sdk/skills).

### Structured outputs

Get validated JSON back **after** the agent completes its multi-turn workflow — via JSON Schema, Zod, or Pydantic. This is what makes an agent a component in a pipeline rather than something a human reads.

See [Get structured output from agents](https://code.claude.com/docs/en/agent-sdk/structured-outputs).

---

## Input and output modes

**Single-message mode** — one prompt, run to completion. Simple.

**Streaming input mode** — feed messages into a running agent. Needed for interactive applications and for handling mid-run user input.

**Streaming output** — get text and tool calls as they happen, for real-time UI.

See [Streaming input](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode) and [Stream responses in real-time](https://code.claude.com/docs/en/agent-sdk/streaming-output).

---

## Sessions

Sessions persist conversation history. Three operations:

| | What |
|---|---|
| `continue` | Pick up the most recent |
| `resume` | Return to a specific session |
| `fork` | Branch from a session without altering the original |

Forking is the one people miss. It lets you explore several continuations from the same state — useful for "try three approaches" patterns.

For production, mirror transcripts to external storage (S3, Redis, your own backend) so any host can resume them. See [Work with sessions](https://code.claude.com/docs/en/agent-sdk/sessions) and [Persist sessions to external storage](https://code.claude.com/docs/en/agent-sdk/session-storage).

---

## Handling approvals and questions

Real agents need to ask. The SDK surfaces Claude's approval requests and clarifying questions so you can present them in your own UI and return the decisions.

See [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input).

---

## Scaling to many tools

**Tool search** loads only the tools needed, on demand — so you can expose thousands without filling context with schemas.

See [Scale to many tools with tool search](https://code.claude.com/docs/en/agent-sdk/tool-search).

---

## Cost tracking

Track token usage, estimate cost, and configure prompt caching. Build this in from the start — retrofitting cost accounting into a running agent system is unpleasant.

See [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking).

---

## Hosting in production

The SDK runs a subprocess architecture. Production considerations:

- Session persistence across hosts
- Scaling and worker management
- Observability
- Multi-tenant isolation
- Docker, Kubernetes, and sandbox providers

See [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting).

### Security

Isolation, credential management, and network controls. Read this before you deploy anything that touches production data.

See [Securely deploying AI agents](https://code.claude.com/docs/en/agent-sdk/secure-deployment).

---

## Observability

Export traces, metrics and events to your observability backend via OpenTelemetry. See [Observability with OpenTelemetry](https://code.claude.com/docs/en/agent-sdk/observability).

---

## Using it on a Claude plan

The Agent SDK can be used with your Claude subscription rather than API credits, subject to your plan's limits. See [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan).

---

## Try it

**Exercise 1 — Hello, agent.**
Run the quickstart. Point it at a real repository. Ask for something multi-step.

**Exercise 2 — Custom tool.**
Define an in-process tool for a system you have (a database, an internal API). Watch Claude use it.

**Exercise 3 — Structured output.**
Build an agent that does multi-turn tool work and returns a Pydantic/Zod-validated result. This is the shape most production agents should have.

**Exercise 4 — Permission callback.**
Implement `canUseTool` that approves reads, denies writes outside a directory, and escalates anything destructive to a human.

**Exercise 5 — Fork.**
Fork a session three ways and try three different continuations from the same state. Compare.

**Exercise 6 — Cost tracking.**
Instrument cost per run. Run twenty realistic tasks. Compute the mean and, more importantly, the p95 — that's the number that will surprise you.

---

## Checkpoint

- You've built an agent with a custom tool and structured output
- You know when to append to the system prompt vs. replace it
- Cost tracking is in place before anything goes near production

---

## Going deeper

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- [Python reference](https://code.claude.com/docs/en/agent-sdk/python) · [TypeScript reference](https://code.claude.com/docs/en/agent-sdk/typescript)
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features)
- [Hosting](https://code.claude.com/docs/en/agent-sdk/hosting) · [Secure deployment](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
