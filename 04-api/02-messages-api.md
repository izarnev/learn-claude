---
title: "The Messages API in depth"
order: 2
---

# The Messages API in depth

**What you'll learn:** every part of a request and response you'll actually use, and the patterns that avoid the common mistakes.

---

## Message structure

```python
messages = [
    {"role": "user",      "content": "What's the capital of France?"},
    {"role": "assistant", "content": "Paris."},
    {"role": "user",      "content": "And its population?"},
]
```

Rules:

- Roles alternate: user, assistant, user, assistant...
- The first message must be `user`
- The **system prompt is a separate top-level parameter**, not a message
- **Prefilled assistant messages on the last turn are no longer supported** on Claude 4.6 and later — they return a 400 error

---

## Content blocks

`content` can be a plain string or an array of blocks. The array form is what you need for images, documents, tool results, and citations.

```python
{
    "role": "user",
    "content": [
        {"type": "text", "text": "What's in this image?"},
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64_data,
            },
        },
    ],
}
```

Block types you'll meet:

| Type | Direction | What |
|---|---|---|
| `text` | both | Plain text |
| `image` | input | Base64, URL, or Files API reference |
| `document` | input | PDFs and other documents |
| `thinking` | output | Claude's reasoning |
| `tool_use` | output | Claude requesting a tool call |
| `tool_result` | input | The result you send back |
| `search_result` | input | For citation-backed RAG |

---

## The system prompt

```python
client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are a senior security engineer reviewing code for a fintech company. You are blunt about risk.",
    messages=[...],
)
```

For caching (see [Prompt caching](07-prompt-caching.md)), pass it as an array of blocks:

```python
system=[
    {"type": "text", "text": SHORT_ROLE},
    {
        "type": "text",
        "text": LONG_REFERENCE_MATERIAL,
        "cache_control": {"type": "ephemeral"},
    },
]
```

**What belongs in the system prompt:** role, standing rules, reference material that doesn't change per request, output format requirements, tool usage guidance.

**What doesn't:** the actual request, per-request variables, anything that changes call to call — putting those in the system prompt destroys your cache hit rate.

---

## Mid-conversation system messages

You can change the system prompt or the tool set partway through a conversation. Useful for multi-phase agents — a research phase with search tools, then a writing phase with different instructions.

See [Mid-conversation system messages and tool changes](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages).

---

## Sampling parameters

| Parameter | Range | Use |
|---|---|---|
| `temperature` | 0–1 | Lower = more deterministic. Use 0 for extraction and classification; leave default for writing. |
| `top_p` | 0–1 | Nucleus sampling. **Don't set both this and temperature.** |
| `stop_sequences` | array of strings | Generation stops when one is produced |

Honest advice: **most people over-tune these.** A better prompt beats a temperature adjustment nearly every time. Set `temperature=0` for deterministic tasks and otherwise leave it alone.

---

## Conversation state

The API is stateless. You maintain the transcript.

```python
messages = []

def ask(question):
    messages.append({"role": "user", "content": question})
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=messages,
    )
    messages.append({"role": "assistant", "content": response.content})
    return response

ask("What's the capital of France?")
ask("And its population?")
```

Note: append `response.content` (the block array), not `response.content[0].text`. Dropping the block structure breaks tool use and thinking.

### The growth problem

Every turn resends everything. Three mitigations:

1. **Prompt caching** — the biggest win for a stable prefix ([Prompt caching](07-prompt-caching.md))
2. **Compaction** — the API offers built-in [compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
3. **Context editing** — programmatically remove old content, e.g. stale tool results ([context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing))

---

## Context awareness

Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5 and Haiku 4.5 can **track their own remaining context budget** during a conversation. This lets Claude plan work against the space it has.

If your harness compacts context or lets Claude save state to files, tell it:

```
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely from where you left off. Therefore,
do not stop tasks early due to token budget concerns. As you approach your token
budget limit, save your current progress and state to memory before the context
window refreshes. Never artificially stop any task early regardless of the
context remaining.
```

Without this, Claude may wrap up prematurely as it senses the limit approaching.

The [memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) pairs well with context awareness for managing these transitions.

---

## Refusals, stop reasons, and fallback

Handle these explicitly:

- **`stop_reason: "refusal"`** — Claude declined. See [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback).
- **Streaming refusals** need their own handling — see [Handle streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).
- **Fallback credit** exists for certain refusal cases — see [Fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit).

Full guidance: [Stop reasons and fallback](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons).

---

## Versioning and beta headers

```
anthropic-version: 2023-06-01
```

Required on every request. It's been stable for a long time; the SDKs set it for you.

Beta features need an extra header:

```python
client.beta.messages.create(
    betas=["skills-2025-10-02"],
    ...
)
```

Betas graduate to GA and the headers become unnecessary. Check [Beta headers](https://platform.claude.com/docs/en/api/beta-headers) before assuming one is still needed.

---

## Multilingual

Claude works across languages. If you need output in a specific language regardless of input language, say so explicitly in the system prompt. See [Multilingual support](https://platform.claude.com/docs/en/build-with-claude/multilingual-support).

---

## Try it

**Exercise 1 — Conversation loop.**
Build the `ask()` function above. Have a ten-turn conversation. Log `usage.input_tokens` each turn and plot the growth.

**Exercise 2 — System prompt effect.**
Same question, three system prompts (none, a role, a role plus detailed rules). Compare.

**Exercise 3 — Temperature ablation.**
Run the same extraction task ten times at `temperature=0` and ten at `1.0`. Count variations. Then do the same for a creative writing task. Note that the *right* answer differs.

**Exercise 4 — Truncation handler.**
Force `stop_reason: "max_tokens"`. Write a handler that either raises the limit and retries, or asks Claude to continue from where it stopped (via a *user* message — prefill is gone).

**Exercise 5 — Block structure.**
Build a conversation with thinking enabled. Verify you're appending the whole content array to history, and that the next turn works.

---

## Checkpoint

- You maintain conversation state correctly, appending whole content arrays
- Your system prompt contains nothing that changes per request
- You handle every `stop_reason` value

---

## Going deeper

- [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Create a Message (API reference)](https://platform.claude.com/docs/en/api/messages/create)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Compaction](https://platform.claude.com/docs/en/build-with-claude/compaction)
- [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing)
- [Stop reasons and fallback](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
- [Versions](https://platform.claude.com/docs/en/api/versioning)
