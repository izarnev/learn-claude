---
title: "Tool use"
order: 4
---

# Tool use

**What you'll learn:** the mechanic that turns Claude from a text generator into an agent, and how to design tools Claude uses correctly.

---

## The loop

```
1. You send: messages + tool definitions
2. Claude responds with stop_reason: "tool_use" and a tool_use block
3. YOU execute the tool
4. You send the result back as a tool_result block in a user message
5. Claude continues — possibly calling more tools, or answering
```

**Claude never executes anything.** It asks; your code decides and runs.

---

## Defining a tool

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location. Use when the user asks about weather, temperature, or conditions in a specific place.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g. 'Amsterdam, Netherlands'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit. Default celsius.",
                },
            },
            "required": ["location"],
        },
    }
]
```

**The description is a prompt.** It's how Claude decides whether to call this tool. Say what it does *and when to use it*. Vague descriptions are the number one cause of tools that don't fire, or fire on the wrong thing.

Same for parameter descriptions — `"City and country, e.g. 'Amsterdam, Netherlands'"` prevents Claude passing `"amsterdam"` and your geocoder failing.

---

## The full loop in code

```python
messages = [{"role": "user", "content": "What's the weather in Amsterdam?"}]

while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=tools,
        messages=messages,
    )

    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason != "tool_use":
        break

    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            try:
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
            except Exception as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Error: {e}",
                    "is_error": True,
                })

    messages.append({"role": "user", "content": tool_results})

print(final_text(response))
```

Four things this code gets right:

1. **It appends the whole `response.content`**, preserving thinking and tool_use blocks
2. **It handles multiple tool_use blocks** in one response — parallel calls are the default
3. **Every result carries its `tool_use_id`**
4. **Errors go back as `tool_result` with `is_error: true`**, not as exceptions. Claude can then correct itself.

Add a hard iteration cap in production.

---

## Tool Runner — the shortcut

The SDKs provide `client.beta.messages.tool_runner`, which runs the agentic loop over your own tools so you don't write the `while` loop yourself. Worth using unless you need custom control over each step.

See [Tool Runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner).

---

## Parallel tool calls

Current models call independent tools in parallel by default. You'll get several `tool_use` blocks in one response — execute them all, return all results in one user message.

To maximise it:

```
If you intend to call multiple tools and there are no dependencies between the
calls, make all of the independent calls in parallel. For example, when reading
3 files, run 3 tool calls in parallel. However, if some calls depend on previous
calls to inform parameters, call them sequentially. Never use placeholders or
guess missing parameters.
```

To reduce it:

```
Execute operations sequentially with brief pauses between each step.
```

---

## Controlling when tools are used

```python
tool_choice={"type": "auto"}                       # Claude decides (default)
tool_choice={"type": "any"}                        # must use some tool
tool_choice={"type": "tool", "name": "get_weather"} # must use this one
tool_choice={"type": "none"}                        # no tools
```

`{"type": "tool", ...}` is the reliable way to get structured extraction via a tool — though [structured outputs](06-structured-outputs.md) is usually cleaner now.

---

## Strict tool use

```python
{
    "name": "create_ticket",
    "description": "...",
    "strict": True,
    "input_schema": {...},
}
```

Guarantees schema validation on tool names and inputs through constrained decoding. Use it whenever malformed input would break something downstream.

---

## Getting Claude to actually use tools

Current models follow instructions literally. This bites people:

> "Can you suggest some changes to improve this function?" → you get suggestions
> "Change this function to improve its performance." → you get changes

To make Claude proactive by default:

```
By default, implement changes rather than only suggesting them. If the user's
intent is unclear, infer the most useful likely action and proceed, using tools
to discover any missing details instead of guessing.
```

To make it conservative:

```
Do not jump into implementation or change files unless clearly instructed. When
the user's intent is ambiguous, default to providing information, research, and
recommendations rather than taking action.
```

**Don't shout.** Opus 4.5 and later are far more responsive to the system prompt. Prompts written for older models that say `CRITICAL: You MUST use this tool when...` now cause *over*-triggering. Normal phrasing works better.

---

## Designing a good tool set

**Few, well-scoped tools beat many overlapping ones.** Three tools with clear boundaries outperform twelve with fuzzy ones — Claude spends its reasoning choosing rather than working.

**Return useful errors.** This is the highest-leverage thing you can do:

| Bad | Good |
|---|---|
| `Error` | `Column 'user_id' does not exist on table 'orders'. Available columns: id, customer_id, total, created_at` |
| `Invalid input` | `'date' must be ISO 8601 (YYYY-MM-DD); received '3rd March'` |
| `Not found` | `No user with email 'x@y.com'. Search by name with search_users instead.` |

A good error lets Claude self-correct in one turn. A bad one produces three wasted turns and a wrong answer.

**Keep results small.** Tool results enter the context window and stay there. Paginate. Summarise. Return IDs and let Claude fetch detail if it needs it.

**Make destructive tools obvious** — in the name, in the description, and gated in your execution layer.

---

## Managing tool context at scale

Two mechanisms for large tool sets:

**Tool search** — with hundreds or thousands of tools, load only what's needed on demand rather than putting every schema in context. See [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

**Programmatic tool calling** — Claude writes code that calls your tools, rather than making individual tool_use round trips. Much more efficient for loops and data processing. See [Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

Also: [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context).

---

## Tool use with caching

Tool definitions are a stable prefix — cache them. See [Tool use with prompt caching](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching) and [module 07](07-prompt-caching.md).

---

## Fine-grained tool streaming

For large tool inputs, streaming the parameters as they generate reduces perceived latency. See [Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming).

---

## Try it

**Exercise 1 — Calculator agent.**
Build the loop with one tool: a calculator. Ask a multi-step arithmetic question. Watch the loop iterate.

**Exercise 2 — Error quality.**
Deliberately return a useless error from your tool. Watch Claude flounder. Improve the error. Watch it self-correct. This exercise changes how you write tools permanently.

**Exercise 3 — Description A/B.**
Write two descriptions for the same tool: vague and specific. Try ten naturally-phrased requests with each. Count correct triggers.

**Exercise 4 — Parallel calls.**
Give Claude three independent tools and a question needing all three. Confirm it calls them in one response.

**Exercise 5 — Strict mode.**
Add `strict: True` to a tool with a tight schema. Try to get Claude to produce invalid input. Fail.

**Exercise 6 — Tool Runner.**
Rewrite exercise 1 using `tool_runner`. Compare the code.

---

## Checkpoint

- You can write the tool loop from memory, including error handling
- Your tool errors are specific enough for Claude to self-correct
- You know why "can you suggest..." gets suggestions rather than actions

---

## Going deeper

- [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Tutorial: Build a tool-using agent](https://platform.claude.com/docs/en/agents-and-tools/tool-use/build-a-tool-using-agent)
- [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- [Troubleshooting tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/troubleshooting-tool-use)
