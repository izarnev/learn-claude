# 05 · Server tools and the MCP connector

**What you'll learn:** the tools Anthropic runs for you, so you don't have to build them.

---

## Client tools vs server tools

| | Client tools | Server tools |
|---|---|---|
| **Executed by** | Your code | Anthropic's infrastructure |
| **You implement** | Everything | Nothing |
| **Loop** | You run it | Handled for you |
| **Examples** | Your database, your API | Web search, code execution, computer use |

Server tools are enabled by adding them to `tools` with a `type` field. Claude uses them and you get the results — no round trips through your code.

---

## The server tool catalogue

| Tool | What it does |
|---|---|
| **Web search** | Live web search with citations |
| **Web fetch** | Retrieve a specific URL |
| **Code execution** | Run Python in a sandbox. Also what powers Agent Skills. |
| **Bash** | Shell commands in a sandbox |
| **Text editor** | View and edit files in the sandbox |
| **Computer use** | Screenshots and control of a virtual desktop |
| **Memory** | Persistent memory across sessions |
| **Advisor** | Consult a stronger model at key moments during a task |

Full list and configuration: [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools).

---

## Web search

```python
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    tools=[{
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5,
    }],
    messages=[{"role": "user", "content": "What's the current state of the EU AI Act?"}],
)
```

Results come back with citations. Configuration options include `max_uses`, allowed and blocked domains, and user location for localised results.

**Cost:** billed per search on top of tokens. Cap `max_uses` in anything user-facing.

See [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) and [Web fetch tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool).

---

## Code execution

```python
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}],
    betas=["code-execution-2025-05-22"],
    messages=[{"role": "user", "content": "Analyse this CSV and find the outliers: ..."}],
)
```

Runs Python in a sandboxed container. This is the right answer for:

- **Any arithmetic that matters** — Claude reasons about maths well and computes it imperfectly
- Data analysis, statistics, charts
- File format conversion
- Anything deterministic

It's also the container Agent Skills run in ([module 10](10-skills-in-the-api.md)).

**Constraints on the API:** no network access, no runtime package installation, pre-installed packages only.

---

## Memory tool

Gives Claude persistent memory across sessions — it can write notes and read them back later. Pairs well with context awareness for long-horizon work.

See [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

---

## Advisor tool

Pairs your main model with a stronger advisor model that Claude consults at key moments. Useful for running most of a task on Sonnet while escalating the genuinely hard decisions to Opus.

See [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool).

---

## Computer use

Screenshots plus mouse and keyboard control of a virtual desktop. Slow and expensive relative to an API, so use it only when there is no API. Current Opus models are notably better at interpreting screenshots and UI elements than earlier generations.

See [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).

---

## The MCP connector

Connect Claude directly to remote MCP servers from the API — no MCP client implementation on your side.

```python
response = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/sse",
        "name": "example",
        "authorization_token": token,
    }],
    messages=[...],
)
```

This is the fastest path from "there's an MCP server for that" to "my application can use it."

- [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [Remote MCP servers](https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers)

For MCP servers inside your own network that need to be reachable by Anthropic-hosted surfaces, **MCP tunnels** provide certificate-authenticated connectivity, deployable via Docker Compose or Helm. See [MCP tunnels](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview).

---

## Combining tools

Server tools, client tools, and MCP tools coexist in one request. A realistic agent might have:

```python
tools = [
    {"type": "web_search_20250305", "name": "web_search"},      # server
    {"type": "code_execution_20250522", "name": "code_execution"}, # server
    {"name": "query_our_database", "description": "...", "input_schema": {...}},  # client
]
```

Plus `mcp_servers` for anything already exposed over MCP.

Guidance on which combinations work well: [Tool combinations](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-combinations).

---

## Citations

Claude can produce responses with precise citations back to source documents you provide — sentence-level, not just document-level. Essential for RAG systems where users need to verify claims.

Related: the `search_result` content block type lets you feed retrieval results in a form Claude can cite from.

- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
- [Search results](https://platform.claude.com/docs/en/build-with-claude/search-results)

---

## Cost awareness

Server tools have their own pricing on top of tokens:

- Web search: per search
- Code execution: per container-hour
- Computer use: high token cost from screenshots

Cap usage (`max_uses`), and monitor. An agent that searches twenty times per question is a cost problem you'll find in your bill rather than your logs, unless you instrument it.

---

## Try it

**Exercise 1 — Search with citations.**
Build a question-answering endpoint using the web search tool. Return the citations alongside the answer. Verify three of them.

**Exercise 2 — Maths, two ways.**
Ask a genuinely hard numerical question with and without code execution. Check both answers. This is the clearest demonstration of "give it a tool" in the whole track.

**Exercise 3 — Data analysis.**
Upload a CSV via the Files API and use code execution to analyse it and produce a chart.

**Exercise 4 — MCP connector.**
Connect a public remote MCP server via the connector. Note how little code it took.

**Exercise 5 — Mixed toolset.**
Build an agent with one server tool, one client tool, and one MCP server. Watch it choose between them.

**Exercise 6 — Cost instrumentation.**
Log server tool usage separately from token usage. Run twenty realistic queries. Compute the true cost per query.

---

## Checkpoint

- You reach for code execution for anything numeric
- You know which server tools exist without looking them up
- You cap `max_uses` on search in anything user-facing
- You instrument server tool cost separately

---

## Going deeper

- [Server tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools)
- [Web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) · [Web fetch](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [Code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)
- [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
