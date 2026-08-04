# 01 · Setup and your first API call

**What you'll learn:** get an API key, make a call, and understand exactly what came back.

---

## Setup

1. Go to [platform.claude.com](https://platform.claude.com) and create an account
2. Add credits (start with $5–10 for this stage)
3. Create an API key under **API Keys**
4. Store it as an environment variable — never in code

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Add it to your shell profile so it persists.

> **Workspaces.** Before you build anything real, create a workspace per project in the Console. Each gets its own keys, budget, and rate limits — so a runaway loop in one project can't drain another's budget.

---

## Install an SDK

```bash
pip install anthropic          # Python
npm install @anthropic-ai/sdk  # TypeScript
```

Official SDKs also exist for Go, Java, C#, PHP and Ruby, plus an OpenAI-compatibility shim and a first-party CLI (`ant`).

---

## Your first call

**Python:**

```python
import anthropic

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain the CAP theorem in three sentences."}
    ],
)

print(message.content[0].text)
```

**TypeScript:**

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Explain the CAP theorem in three sentences." }],
});

console.log(message.content[0].text);
```

**cURL:**

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Explain the CAP theorem in three sentences."}]
  }'
```

---

## Reading the response

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-5",
  "content": [
    { "type": "text", "text": "The CAP theorem states that..." }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 18,
    "output_tokens": 94
  }
}
```

Three fields you'll use constantly:

**`content`** is an **array of blocks**, not a string. Blocks can be `text`, `thinking`, `tool_use`, and others. Never assume `content[0]` is text — with thinking enabled it often isn't. Filter by type.

```python
text = "".join(b.text for b in message.content if b.type == "text")
```

**`stop_reason`** tells you why generation ended:

| Value | Meaning | What to do |
|---|---|---|
| `end_turn` | Claude finished naturally | Normal |
| `max_tokens` | Hit your `max_tokens` limit | **The response is truncated.** Raise the limit or handle it |
| `tool_use` | Claude wants to call a tool | Execute it and continue the loop |
| `stop_sequence` | Hit one of your stop sequences | Normal |
| `refusal` | Claude declined | Handle gracefully |

Ignoring `stop_reason` is one of the most common production bugs. A truncated JSON response looks like a parsing error, not a token-limit error.

**`usage`** gives token counts for billing and monitoring. Log it from day one.

---

## The required parameters

| Parameter | Notes |
|---|---|
| `model` | Pinned snapshot ID. See the [model cheat sheet](../99-reference/model-cheatsheet.md) |
| `max_tokens` | **Required.** Maximum output tokens. Not a target — a ceiling. |
| `messages` | Array of `{role, content}`, alternating user and assistant |

And the ones you'll add almost immediately:

| Parameter | Notes |
|---|---|
| `system` | System prompt. A top-level string, **not** a message with `role: "system"` |
| `temperature` | 0–1. Lower is more deterministic. Default is usually fine. |
| `stop_sequences` | Strings that end generation |
| `thinking` | `{"type": "adaptive"}` |
| `output_config` | `{"effort": "high"}`, `{"format": {...}}` |
| `tools` | Tool definitions |
| `stream` | Boolean |

---

## Error handling

```python
import anthropic
from anthropic import APIError, RateLimitError, APIConnectionError

try:
    message = client.messages.create(...)
except RateLimitError as e:
    # 429 — respect retry-after, back off
    ...
except APIConnectionError as e:
    # network — retry
    ...
except APIError as e:
    print(e.status_code, e.message)
```

Key status codes:

| Code | Meaning |
|---|---|
| 400 | Invalid request — bad parameters, unsupported feature for this model |
| 401 | Bad API key |
| 403 | Not permitted |
| 404 | Not found |
| 413 | Request too large |
| 429 | Rate limited — check `retry-after` |
| 500 | Server error — retry |
| 529 | Overloaded — retry with backoff |

The SDKs retry automatically on retryable errors with sensible backoff. Don't build your own retry loop on top without checking what the SDK already does.

---

## Counting tokens before you send

```python
count = client.messages.count_tokens(
    model="claude-sonnet-5",
    messages=[{"role": "user", "content": long_document}],
)
print(count.input_tokens)
```

Free. Use it to check you're inside the context window and to estimate cost before a large batch.

---

## Cost control from day one

Four things to set up before you write a real loop:

1. **A workspace** with a budget in the Console
2. **Spend limits** — Console, or the [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api)
3. **Usage logging** — record `usage.input_tokens` and `usage.output_tokens` on every call
4. **A hard iteration cap** in any agentic loop you write

The failure mode is never one expensive call. It's a loop that didn't terminate.

---

## Try it

**Exercise 1 — Hello, API.**
Make the call above. Print the whole response object, not just the text. Read every field.

**Exercise 2 — Content blocks.**
Enable thinking (`thinking={"type": "adaptive"}`). Print `[b.type for b in message.content]`. Note that `content[0]` is no longer text.

**Exercise 3 — Truncation.**
Ask for a 2,000-word essay with `max_tokens=100`. Check `stop_reason`. Write the handler you'd need in production.

**Exercise 4 — Cost meter.**
Write a wrapper that logs tokens and computes cost per call from the pricing table. Use it for the rest of this stage.

**Exercise 5 — Token counting.**
Count tokens for a large document before sending it. Compare against `usage.input_tokens` afterwards.

**Exercise 6 — Multi-language.**
Make the same call from a second SDK (TypeScript if you started in Python). Note what's identical and what's idiomatic.

---

## Checkpoint

- You can make an API call and correctly extract text from a multi-block response
- You handle `stop_reason == "max_tokens"`
- You log token usage on every call
- You have a spend limit configured

---

## Going deeper

- [Quickstart](https://platform.claude.com/docs/en/get-started)
- [Get your API key](https://platform.claude.com/docs/en/get-api-key)
- [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Errors](https://platform.claude.com/docs/en/api/errors)
- [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces)
- [SDKs and libraries](https://platform.claude.com/docs/en/cli-sdks-libraries/overview)
