---
title: "07 · Prompt caching"
---

# 07 · Prompt caching

**What you'll learn:** the single biggest cost optimisation available on the API, and how to avoid the mistakes that silently disable it.

---

## What it does

If you send the same prefix repeatedly — a long system prompt, tool definitions, a reference document — caching stores it server-side. Subsequent requests reading that cache cost a fraction of normal input tokens.

For agents and chat applications that resend a stable prefix every turn, savings of 70–90% on input cost are routine.

---

## How to use it

Mark the end of your stable prefix with `cache_control`:

```python
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "You are a support agent for Acme Corp."},
        {
            "type": "text",
            "text": ENTIRE_PRODUCT_MANUAL,        # 50,000 tokens
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[{"role": "user", "content": user_question}],
)
```

Everything **up to and including** the marked block is cached. The user question isn't — it changes every time, which is exactly right.

---

## The cache-friendly request layout

Order matters, because the cache is a prefix match. Put stable content first:

```
1. System prompt              ← stable
2. Tool definitions           ← stable
3. Long reference documents   ← stable
   ─── cache_control here ───
4. Conversation history       ← grows
5. The current user message   ← changes
```

Get this wrong — put a timestamp or a user ID at the top of your system prompt — and **nothing caches, ever.** This is the most common failure, and it's silent: everything works, it just costs full price.

---

## Cache breakpoints

You can set up to four `cache_control` markers, creating nested cache segments. Useful when different parts of your prefix change at different rates:

```
[ system prompt ]           ← changes monthly       — breakpoint 1
[ tool definitions ]        ← changes weekly        — breakpoint 2
[ conversation history ]    ← grows each turn       — breakpoint 3
[ current message ]         ← changes every request
```

For a growing conversation, move the last breakpoint forward as the conversation grows so each turn caches the previous turns.

---

## TTL

The default cache lifetime is short (minutes) and refreshes on each hit. Longer TTL options exist at different pricing — see the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing).

The practical implication: caching helps most with **sustained traffic**. A prefix used once an hour won't stay warm. A prefix used every few seconds will.

---

## Reading the numbers

```python
print(response.usage)
# input_tokens: 12
# cache_creation_input_tokens: 50134
# cache_read_input_tokens: 0
```

First call: `cache_creation_input_tokens` is high (writing costs slightly *more* than normal input).

```python
# input_tokens: 15
# cache_creation_input_tokens: 0
# cache_read_input_tokens: 50134
```

Subsequent calls: `cache_read_input_tokens` is high and costs a fraction.

**If `cache_read_input_tokens` stays 0 across repeated calls, your cache is broken.** Something in the prefix is changing.

Anthropic also ships [cache diagnostics](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics) (beta) for debugging this properly.

---

## When it pays

**Great fit:**

- Chatbots with a large system prompt
- Agents with many tool definitions
- Document QA over the same document repeatedly
- Few-shot prompts with many examples
- Anything with a prefix over ~2,000 tokens used more than a few times

**Poor fit:**

- Prefix under the minimum cacheable size
- One-off requests
- Every request has a genuinely different prefix

---

## The classic mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Timestamp or request ID at the top of the system prompt | Nothing ever caches | Move it to the user message |
| User-specific data in the cached prefix | Cache per user instead of shared | Move it after the breakpoint |
| Changing tool definitions between calls | Cache invalidated | Keep them stable; version them |
| Reordering messages | Prefix no longer matches | Append only |
| Switching models mid-conversation | Cache invalidated | Expected; one slow turn |
| Never checking `usage` | You don't know it's broken | Log cache fields |

That last row is the real lesson: **caching fails silently.** Log `cache_read_input_tokens` from the start.

---

## Multi-user cache sharing

If many users run the same task with the same prefix, you want one shared cache rather than one per user. That means keeping anything per-user *out* of the prefix.

Claude Code offers `--exclude-dynamic-system-prompt-sections` for exactly this — it moves per-machine details (working directory, environment info, memory paths) out of the system prompt and into the first user message, so the cached prefix is identical across users and machines.

The same principle applies to your own applications: **the prefix should describe the task, not the requester.**

---

## Combining with tools

Tool definitions are usually your most stable large block. Cache them:

```python
tools = [
    {...},
    {..., "cache_control": {"type": "ephemeral"}},   # on the last tool
]
```

See [Tool use with prompt caching](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching).

---

## Try it

**Exercise 1 — Measure it.**
Build a QA endpoint over a 20,000-token document. Ask ten questions without caching, logging cost. Add caching. Ask the same ten. Compute the saving.

**Exercise 2 — Break it deliberately.**
Add a timestamp to the top of a cached system prompt. Watch `cache_read_input_tokens` drop to zero. Remove it. This is the failure you'll hit in production; feel it once now.

**Exercise 3 — Growing conversation.**
Build a chat loop that moves the cache breakpoint forward each turn. Log cache reads. Compare against a fixed breakpoint.

**Exercise 4 — Multi-breakpoint.**
Structure a request with three breakpoints at different change rates. Verify with `usage` that each level caches.

**Exercise 5 — Instrument it.**
Add cache hit rate to your logging wrapper from module 01. Watch it for a week of real traffic.

---

## Checkpoint

- You log `cache_creation_input_tokens` and `cache_read_input_tokens` on every call
- Nothing per-request appears before your cache breakpoint
- You've measured a real cost saving rather than assuming one

---

## Going deeper

- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Cache diagnostics (beta)](https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics)
- [Tool use with prompt caching](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-use-with-prompt-caching)
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- [How Claude Code uses prompt caching](https://code.claude.com/docs/en/prompt-caching)
