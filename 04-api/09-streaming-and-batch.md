---
title: "Streaming and batch processing"
order: 9
---

# Streaming and batch processing

**What you'll learn:** the two ways to change *when* you get results — one for perceived speed, one for cost.

---

## Streaming

```python
with client.messages.stream(
    model="claude-sonnet-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": "Write a short essay on..."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

message = stream.get_final_message()
```

Streaming doesn't make generation faster. It makes it *feel* faster, because the first token arrives in a fraction of a second instead of after the whole response.

**Use it for:** anything a human is watching.
**Skip it for:** batch jobs, pipelines, anything parsed as a whole.

### Event types

The raw stream is server-sent events:

| Event | Meaning |
|---|---|
| `message_start` | Message metadata, including initial usage |
| `content_block_start` | A new block begins (text, thinking, tool_use) |
| `content_block_delta` | Incremental content |
| `content_block_stop` | Block complete |
| `message_delta` | Top-level updates — `stop_reason`, final usage |
| `message_stop` | Done |

The SDK helpers (`stream.text_stream`) handle the assembly. Drop to raw events when you need to react to block boundaries — for example, showing a "thinking..." indicator while `thinking` blocks stream and switching to output when `text` starts.

### Streaming with tools

Tool inputs stream too. For long tool inputs, [fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming) reduces the wait before you can start acting.

### Streaming refusals

A refusal mid-stream needs its own handling — you may have already shown the user partial output. See [Handle streaming refusals](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

### Long requests

Very long generations may **require** streaming — non-streaming requests can hit timeouts. If you're generating tens of thousands of output tokens, stream.

---

## Batch processing

Submit many requests asynchronously for a substantial discount.

```python
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"ticket-{t.id}",
            "params": {
                "model": "claude-haiku-4-5",
                "max_tokens": 512,
                "messages": [{"role": "user", "content": classify_prompt(t)}],
            },
        }
        for t in tickets
    ]
)

# Poll
status = client.messages.batches.retrieve(batch.id)

# Retrieve results when ended
for result in client.messages.batches.results(batch.id):
    print(result.custom_id, result.result)
```

Results are keyed by your `custom_id` and can arrive in any order.

### When to use it

**Yes:**

- Evaluation runs (this is the big one — evals are naturally batchable)
- Bulk classification, extraction, tagging
- Offline document processing
- Backfills and migrations
- Synthetic data generation

**No:**

- Anything a user is waiting for
- Anything where the next request depends on the previous result

### Extended output

On the Batches API, Claude Opus 5, Opus 4.8, 4.7, 4.6, Sonnet 5 and Sonnet 4.6 support up to **300k output tokens** using the `output-300k-2026-03-24` beta header — well beyond the 128k synchronous limit.

### Batch + caching

Combine them. If every request in a batch shares a large prefix, cache it. Classifying 10,000 tickets against the same 30k-token taxonomy is dramatically cheaper with both than with neither.

---

## Service tiers

Beyond streaming and batch, **service tiers** let you trade latency against throughput and priority. Worth reviewing before you architect around latency assumptions.

See [Service tiers](https://platform.claude.com/docs/en/api/service-tiers).

---

## Latency reduction, generally

If response time is your problem, in rough order of impact:

1. **Use a smaller model.** Haiku is dramatically faster than Opus.
2. **Lower the effort setting.** Less thinking, faster response.
3. **Stream.** Doesn't reduce total time, transforms perceived time.
4. **Cache.** A cache hit skips reprocessing the prefix.
5. **Shorten the prompt.** Fewer input tokens, faster time-to-first-token.
6. **Reduce `max_tokens`** if you're generating more than you need.
7. **Parallelise** independent calls rather than chaining them.

Anthropic's guide: [Reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency).

---

## Rate limits in practice

Batch and streaming both interact with rate limits.

- Respect `retry-after` on 429s
- Exponential backoff with jitter
- The SDKs retry automatically — check what yours does before adding your own
- The Batch API is the correct answer to "I keep hitting rate limits on bulk work"
- Query current limits via the [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api)

---

## Try it

**Exercise 1 — Perceived latency.**
Build the same endpoint streaming and non-streaming. Time to first token vs. time to complete. Note the numbers are very different and that only one of them is what users experience.

**Exercise 2 — Raw events.**
Handle raw stream events. Show a "thinking" indicator during `thinking` blocks and switch when `text` begins.

**Exercise 3 — Batch classification.**
Classify 200 items via the Batch API. Compare cost and wall-clock time against 200 synchronous calls.

**Exercise 4 — Batch + cache.**
Add a large shared prefix with caching to your batch. Measure the combined saving.

**Exercise 5 — Latency ladder.**
Take a slow endpoint. Apply the seven latency techniques one at a time, measuring after each. Find which two actually mattered for your workload.

---

## Checkpoint

- Anything user-facing streams
- Anything offline and bulk goes through the Batch API
- You know your workload's actual latency bottleneck rather than guessing

---

## Going deeper

- [Streaming Messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
- [Service tiers](https://platform.claude.com/docs/en/api/service-tiers)
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency)
