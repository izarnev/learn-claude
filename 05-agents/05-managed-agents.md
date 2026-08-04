---
title: "Managed Agents"
order: 5
---

# Managed Agents

**What you'll learn:** running agents on Anthropic's infrastructure instead of your own.

---

## What it is

You define the agent. Anthropic runs it — in a managed cloud sandbox, with session management, memory, webhooks, scheduling and multi-agent orchestration handled for you.

The trade: less control over the runtime, dramatically less operational work.

---

## Managed Agents vs. the Agent SDK

| | Agent SDK | Managed Agents |
|---|---|---|
| **Runs on** | Your infrastructure | Anthropic's |
| **You operate** | Hosting, scaling, session storage, sandboxes | Nothing |
| **Control** | Full | Configuration-level |
| **Sandbox** | You choose (Docker, K8s, dev container...) | Managed, or self-hosted |
| **Best when** | You need custom orchestration or must run in your own VPC | You want an agent running without an ops project |

Both use the same underlying model and tool concepts. Migrating between them is not a rewrite.

---

## The pieces

### Agent setup

Define the agent: instructions, tools, model, permissions. See [Define your agent](https://platform.claude.com/docs/en/managed-agents/agent-setup).

### Sessions

Start a session, stream events, operate on it mid-run.

- [Start a session](https://platform.claude.com/docs/en/managed-agents/sessions)
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)
- [Session operations](https://platform.claude.com/docs/en/managed-agents/session-operations)

### Outcomes

Define what "done" means, declaratively. This is the termination-condition problem from [Agent design principles](01-agent-design-principles.md), given first-class support.

See [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes).

### Environments and sandboxes

Configure the cloud environment the agent runs in — or bring your own sandbox if you need the execution inside your network.

- [Cloud environment setup](https://platform.claude.com/docs/en/managed-agents/environments)
- [Cloud sandbox reference](https://platform.claude.com/docs/en/managed-agents/cloud-sandboxes-reference)
- [Self-hosted sandboxes](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) and their [security model](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-security)

### Memory stores

Persistent memory across sessions, as a managed resource. This is the "external state" principle from [Context engineering](03-context-engineering.md), without you running the storage.

See [Memory stores](https://platform.claude.com/docs/en/managed-agents/memory).

### Tools, MCP, and Skills

- [Tools](https://platform.claude.com/docs/en/managed-agents/tools)
- [MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector)
- [Agent Skills](https://platform.claude.com/docs/en/managed-agents/skills)

### Credentials

**Vaults** hold credentials the agent needs, so secrets aren't in prompts or configuration.

See [Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults).

### Permission policies

Declarative control over what the agent may do. See [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies).

### Files

Attach files to a session and download what the agent produces. See [Attach and download files](https://platform.claude.com/docs/en/managed-agents/files).

### GitHub

First-class GitHub access for agents that work on repositories. See [Access GitHub](https://platform.claude.com/docs/en/managed-agents/github).

### Scheduling and webhooks

- [Scheduled deployments](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments) — recurring runs
- [Subscribe to webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks) — react to events, and be notified of agent progress

### Multi-agent orchestration

Coordinate multiple managed agents. See [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration).

### Dreams

A distinct capability with its own lifecycle (create, cancel, archive). See [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams).

---

## Prototyping in the Console

You can prototype an agent in the Console before writing any code — define it, run it, iterate on the instructions, then move to the API.

See [Prototype in Console](https://platform.claude.com/docs/en/managed-agents/onboarding).

---

## When to choose Managed Agents

**Good fit:**

- You want an agent running in production without building the runtime
- Recurring scheduled work
- Event-driven agents (webhook in, work out)
- You don't have an ops team to give this to
- Multi-agent orchestration you don't want to coordinate yourself

**Poor fit:**

- Execution must happen inside your VPC and you can't use self-hosted sandboxes
- You need control over the loop itself, not just its configuration
- The agent is embedded in a local tool (that's Claude Code or the SDK)

---

## Migrating

If you have something built on the Agent SDK or an older shape, there's a migration path.

See [Migration](https://platform.claude.com/docs/en/managed-agents/migration).

---

## Try it

**Exercise 1 — Console prototype.**
Define an agent in the Console. Run it. Iterate on the instructions until the output is good. Note how much faster this is than writing code first.

**Exercise 2 — Outcomes.**
Define an explicit outcome. Give the agent a task it can't complete. Confirm it stops cleanly rather than looping.

**Exercise 3 — Memory store.**
Build an agent that accumulates knowledge across sessions via a memory store. Run it three times on related tasks. Verify the third run benefits from the first two.

**Exercise 4 — Scheduled deployment.**
Schedule a recurring agent. Check the output twice before trusting it.

**Exercise 5 — Webhook.**
Trigger an agent from an event. Subscribe to a webhook for its completion.

**Exercise 6 — Compare.**
Build the same simple agent twice: once on the Agent SDK, once as a Managed Agent. Compare the code volume and the operational surface.

---

## Checkpoint

- You've run a Managed Agent end to end
- You can articulate when you'd choose Managed Agents over the Agent SDK
- You use vaults for credentials rather than putting them in configuration

---

## Going deeper

- [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Managed Agents reference](https://platform.claude.com/docs/en/managed-agents/reference)
- [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)
- [Memory stores](https://platform.claude.com/docs/en/managed-agents/memory)
- [Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
