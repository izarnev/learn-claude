---
title: "API cheat sheet"
order: 5
---

# API cheat sheet

---

## Minimal request

```python
import anthropic
client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
```

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"claude-sonnet-5","max_tokens":1024,
       "messages":[{"role":"user","content":"Hello"}]}'
```

---

## Parameters

| Parameter | Notes |
|---|---|
| `model` | Required. Pinned snapshot ID. |
| `max_tokens` | Required. Output ceiling, not a target. |
| `messages` | Required. Alternating user/assistant. First must be `user`. |
| `system` | Top-level string or block array — **not** a message |
| `temperature` / `top_p` / `top_k` | Removed on current models — a non-default value returns a `400` on Opus 4.7+, Opus 5, Sonnet 5, Fable 5 and Mythos 5. Only Haiku 4.5 and Sonnet 4.5-and-older still accept them. Steer with prompting, or `output_config.format` for determinism of shape. |
| `stop_sequences` | Array of strings |
| `thinking` | `{"type": "adaptive"}` |
| `output_config` | `{"effort": "high"}`, `{"format": {...}}` |
| `tools` | Tool definitions |
| `tool_choice` | `auto` \| `any` \| `tool` \| `none` |
| `stream` | Boolean |
| `metadata` | `{"user_id": "..."}` |
| `mcp_servers` | Remote MCP connector |
| `container` | Skills and code execution container config |
| `betas` | Beta headers |

---

## Response

```json
{
  "id": "msg_...",
  "role": "assistant",
  "model": "claude-sonnet-5",
  "content": [{"type": "text", "text": "..."}],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 18,
    "output_tokens": 94,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

`content` is an **array of blocks**. Never assume `content[0]` is text.

```python
text = "".join(b.text for b in msg.content if b.type == "text")
```

### Stop reasons

| Value | Do |
|---|---|
| `end_turn` | Normal |
| `max_tokens` | **Truncated.** Raise the limit or handle it |
| `tool_use` | Execute and continue the loop |
| `stop_sequence` | Normal |
| `refusal` | Handle gracefully |

### Status codes

`400` invalid · `401` bad key · `403` forbidden · `404` not found · `413` too large · `429` rate limited (check `retry-after`) · `500` server error · `529` overloaded

---

## Thinking and effort

```python
thinking={"type": "adaptive"},
output_config={"effort": "high"},     # low|medium|high|xhigh|max
```

Legacy `{"type": "enabled", "budget_tokens": N}` returns a 400 on Claude 4.7+.

Preserve `thinking` blocks in conversation history.

---

## Structured outputs

```python
output_config={
    "format": {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                "summary":  {"type": "string"},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            },
            "required": ["severity", "summary", "confidence"],
            "additionalProperties": False,
        },
    }
}
```

Was `output_format` in beta; now `output_config.format`, no beta header.

---

## Tool use

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather. Use when asked about weather, temperature, or conditions in a place.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and country, e.g. 'Amsterdam, Netherlands'"},
        },
        "required": ["location"],
        "additionalProperties": False,
    },
}]
```

### The loop

```python
messages = [{"role": "user", "content": q}]
for _ in range(MAX_TURNS):
    r = client.messages.create(model=M, max_tokens=1024, tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": r.content})
    if r.stop_reason != "tool_use":
        break
    results = []
    for b in r.content:
        if b.type == "tool_use":
            try:
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": str(execute(b.name, b.input))})
            except Exception as e:
                results.append({"type": "tool_result", "tool_use_id": b.id,
                                "content": f"Error: {e}", "is_error": True})
    messages.append({"role": "user", "content": results})
```

Or use `client.beta.messages.tool_runner`.

---

## Server tools

```python
tools = [
  {"type": "web_search_20250305",    "name": "web_search", "max_uses": 5},
  {"type": "code_execution_20260521","name": "code_execution"},
]
```

Available: web search, web fetch, code execution, bash, text editor, computer use, memory, advisor.

---

## MCP connector

```python
client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    mcp_servers=[{"type": "url", "url": "https://mcp.example.com/sse",
                  "name": "example", "authorization_token": token}],
    messages=[...],
)
```

---

## Prompt caching

```python
system=[
    {"type": "text", "text": SHORT_ROLE},
    {"type": "text", "text": LONG_MATERIAL, "cache_control": {"type": "ephemeral"}},
]
```

Layout: tools → system → reference docs → **breakpoint** → history → current message.

Up to four breakpoints. Verify with `usage.cache_read_input_tokens`. If it stays 0, something in your prefix changes per request.

---

## Images and documents

```python
{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}}
{"type": "image", "source": {"type": "url", "url": "https://..."}}
{"type": "image", "source": {"type": "file", "file_id": "file_..."}}
{"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": b64}}
```

Resize images before sending. Text-only PDFs are cheaper sent as extracted text.

---

## Files API

```python
f = client.beta.files.upload(
    file=("report.pdf", open("report.pdf","rb"), "application/pdf"),
    betas=["files-api-2025-04-14"],
)
# then reference f.id
```

---

## Skills

```python
client.beta.messages.create(
    betas=["skills-2025-10-02", "files-api-2025-04-14"],
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    container={"skills": [{"type": "anthropic", "skill_id": "xlsx"}]},
    ...
)
```

Pre-built: `pptx` `xlsx` `docx` `pdf`. Custom via `/v1/skills`, workspace-wide.

**API constraints:** no network access, no runtime package installs, pre-installed packages only.

---

## Streaming

```python
with client.messages.stream(model=M, max_tokens=2048, messages=[...]) as s:
    for t in s.text_stream:
        print(t, end="", flush=True)
final = s.get_final_message()
```

Events: `message_start` · `content_block_start` · `content_block_delta` · `content_block_stop` · `message_delta` · `message_stop`

---

## Batch

```python
batch = client.messages.batches.create(requests=[
    {"custom_id": ex["id"], "params": {...}} for ex in dataset
])
client.messages.batches.retrieve(batch.id)
client.messages.batches.results(batch.id)
```

Extended output to 300k tokens with `output-300k-2026-03-24` on supported models.

---

## Token counting

```python
client.messages.count_tokens(model="claude-sonnet-5", messages=[...])
```

Free.

---

## Production checklist

- [ ] `ANTHROPIC_API_KEY` in the environment, never in code
- [ ] Workspace with a budget per project
- [ ] Spend limit configured
- [ ] Every `stop_reason` handled
- [ ] All `usage` fields logged, including cache
- [ ] Prompt version logged
- [ ] Prompt caching verified working
- [ ] Structured outputs on anything parsed downstream
- [ ] Hard iteration and spend caps on agentic loops
- [ ] Eval set with a recorded baseline
- [ ] Model IDs pinned
