---
title: "09 · MCP in Claude Code"
---

# 09 · MCP in Claude Code

**What you'll learn:** how to connect Claude Code to your database, ticket system, browser and internal tools — and how to keep the context cost near zero.

---

## Recap

The **Model Context Protocol** is an open standard. An MCP server exposes tools; Claude Code is the client that discovers and calls them.

Without MCP, Claude Code can read your repo and run shell commands. With MCP, it can query your staging database, read a Jira ticket, check a Sentry error, or drive a browser — as first-class tools, not shell hacks.

---

## Adding a server

```bash
# Fastest path
claude mcp add <name> <command> [args...]

# Or from a config file
claude --mcp-config ./mcp.json

# Only use servers from that file, ignoring everything else
claude --strict-mcp-config --mcp-config ./mcp.json
```

Config shape:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    }
  }
}
```

Transports: **stdio** (a local process), **HTTP**, and **SSE**.

### Scope

| Scope | Where | Shared |
|---|---|---|
| **Local** | Your machine, this project | No |
| **Project** | `.mcp.json` in the repo | Yes, via git |
| **User** | `~/.claude.json` | You, all projects |

Precedence: **local > project > user.**

Project scope is the good one for teams — commit `.mcp.json` and everyone gets the same tools.

### Authentication

```bash
claude mcp login sentry           # run the OAuth flow from the shell
claude mcp login sentry --no-browser   # over SSH: prints the URL to paste
claude mcp logout sentry
```

Or use `/mcp` inside a session for the interactive panel.

---

## Context cost, and why it's low

**Tool search is on by default.** At session start, Claude Code loads only **tool names** from connected servers; full JSON schemas stay deferred until Claude needs a specific tool.

The consequence: idle MCP servers cost very little. You can connect several without paying for all of them on every request.

Check the actual cost:

```
/mcp
```

Shows connection status and token cost per server. Disconnect what you're not using.

Claude Code reconnects to remote servers automatically if they drop.

---

## Servers worth connecting

| Server | Why |
|---|---|
| **Database** (Postgres, MySQL, SQLite) | Claude can inspect the real schema and run real queries instead of guessing |
| **Playwright / browser** | Verification. Claude can actually check the UI works, which matters enormously for autonomous work |
| **Sentry / error tracking** | Go from an error to a fix without leaving the terminal |
| **GitHub / GitLab** | Issues, PRs, reviews |
| **Jira / Linear** | Ticket context in the session |
| **Filesystem** (scoped) | Read a directory outside the repo |
| **Your own internal tools** | Usually the highest-value one |

Browse: [Connectors directory](https://claude.com/partners/mcp).

The Playwright/browser one deserves emphasis. Anthropic's own guidance on long-horizon agentic work says: *"As the length of autonomous tasks grows, Claude needs to verify correctness without continuous human feedback. Tools like Playwright MCP server or computer use capabilities for testing UIs are helpful."* Verification tooling is what makes long autonomous runs actually work.

---

## Writing your own MCP server

You don't need to unless you have a system worth exposing. When you do:

- SDKs exist for TypeScript, Python and others at [modelcontextprotocol.io](https://modelcontextprotocol.io)
- The Agent SDK has an **in-process MCP server** so you can define custom tools as plain functions without a separate process — see [Give Claude custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)

**Tool design rules that matter:**

1. **Descriptions are prompts.** Claude picks tools by matching your description. Say what it does and when to use it.
2. **Few, well-scoped tools beat many overlapping ones.** Three tools with clear boundaries outperform twelve with fuzzy ones.
3. **Return useful errors.** "Query failed" teaches Claude nothing. "Column `user_id` does not exist on table `orders`; did you mean `customer_id`?" lets it self-correct.
4. **Keep results small.** Tool results enter the context window. Paginate. Summarise. Don't return 10,000 rows.
5. **Mark destructive tools.** Set `requiresUserInteraction` on anything irreversible so it always prompts.

---

## Security

MCP servers are the widest attack surface you can add to Claude Code.

**A server can:** read anything it has access to, take actions with its credentials, and return content that Claude reads as context — which means it can inject instructions.

Practical controls:

- **Deny rules work on MCP tools.** `"mcp__somesrv__delete_*"` in `permissions.deny`.
- **`--disallowedTools "mcp__*"`** removes every MCP tool for a session.
- **`requiresUserInteraction`** on a tool forces a prompt that even a hook returning `allow` can't suppress.
- **Organisation controls on connector tools** — admins can set tools to `ask` org-wide.
- **Managed MCP** — allowlists and denylists of which servers users may add. See [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp).
- **Hooks on MCP tools** — match `mcp__.*` in a `PreToolUse` hook to log or gate every MCP call.

Treat connecting a third-party MCP server like adding a dependency with production credentials — because that's what it is.

---

## MCP tunnels

For enterprise cases where an MCP server lives inside your network and needs to be reachable by Anthropic-hosted surfaces, **MCP tunnels** provide the connection with certificate-based auth. Deployable via Docker Compose or Helm, manageable in the Console.

See [MCP tunnels](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview).

---

## Channels

A related research-preview mechanism: an MCP server can **push** events into a running Claude Code session — CI results, chat messages, monitoring alerts — so Claude reacts while you're away.

```bash
claude --channels plugin:my-notifier@my-marketplace
```

See [Channels](https://code.claude.com/docs/en/channels).

---

## Try it

**Exercise 1 — Database server.**
Connect a Postgres or SQLite MCP server to a dev database. Ask Claude a question requiring schema knowledge. Compare against what it guessed before.

**Exercise 2 — Cost check.**
Run `/mcp` before and after connecting two servers. Note the token cost. Then note how it doesn't change much — that's tool search working.

**Exercise 3 — Verification loop.**
Connect a browser MCP server. Ask Claude to make a UI change and *verify it works*. This is the difference between "Claude wrote code" and "Claude shipped a change."

**Exercise 4 — Project scope.**
Create `.mcp.json` at your repo root with the servers your team needs. Commit it. Onboarding just got shorter.

**Exercise 5 — Gate an MCP tool.**
Add a `PreToolUse` hook with matcher `mcp__.*` that logs every MCP call. Read the log after a day.

**Exercise 6 — Error quality.**
If you build a server: deliberately return a bad error message, watch Claude flounder, then improve it and watch it self-correct. This is the single biggest lever on tool usability.

---

## Checkpoint

- You have at least one MCP server connected that gives Claude real capability
- You can explain why connecting five servers doesn't cost five servers' worth of context
- You know three ways to constrain an MCP tool

---

## Going deeper

- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)
- [MCP quickstart](https://code.claude.com/docs/en/mcp-quickstart)
- [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp)
- [Give Claude custom tools (Agent SDK)](https://code.claude.com/docs/en/agent-sdk/custom-tools)
- [Remote MCP servers](https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers)
- [MCP connector (API)](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [modelcontextprotocol.io](https://modelcontextprotocol.io)
