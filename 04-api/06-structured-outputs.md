# 06 · Structured outputs

**What you'll learn:** how to guarantee Claude returns JSON matching your schema, so you can stop writing parsers and retry loops.

---

## Two features

| Feature | Parameter | Guarantees |
|---|---|---|
| **JSON outputs** | `output_config.format` | Claude's *response* matches your schema |
| **Strict tool use** | `strict: true` on a tool | Tool *names and inputs* match their schemas |

Use them independently or together.

Both work through **constrained decoding** — the model literally cannot produce output that violates the schema. This is different from asking nicely and validating afterwards.

> Generally available on the Claude API for Claude 4.5 and later. Availability varies by cloud provider — check the [docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) if you're on Bedrock, Google Cloud, or Foundry.
>
> **Migrating from beta?** `output_format` moved to `output_config.format`, and beta headers are no longer required. The old shape works for a transition period.

---

## JSON outputs

```python
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
    }],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "plan_interest": {"type": "string"},
                    "demo_requested": {"type": "boolean"},
                },
                "required": ["name", "email", "plan_interest", "demo_requested"],
                "additionalProperties": False,
            },
        }
    },
)
```

The text block contains valid JSON matching the schema. Always. No `try/except json.JSONDecodeError`.

---

## What this replaces

Before structured outputs, people used:

- **Prefilled assistant messages** (`{"role": "assistant", "content": "{"`) — **no longer supported** on Claude 4.6+; returns a 400 error
- **Tool use as a schema hack** — `tool_choice: {"type": "tool", "name": "extract"}` with the schema as the tool's input schema. Still works, but structured outputs is cleaner.
- **Prompt-and-pray plus retry loops** — asking for JSON and validating afterwards

If you're maintaining any of these patterns, migrate.

---

## Schema design that works

**Use enums for anything categorical:**

```json
{"severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]}}
```

This makes classification exact rather than approximate. No more mapping "High", "high-severity", and "HIGH" to the same bucket.

**Set `additionalProperties: false`** unless you genuinely want extra fields.

**Mark everything you need as `required`.** Optional fields will sometimes be absent.

**Use `description` on fields.** They're read by the model and disambiguate:

```json
{
  "due_date": {
    "type": "string",
    "description": "ISO 8601 date (YYYY-MM-DD). Use null if no date is stated. Do not infer a date from vague phrases like 'soon'."
  }
}
```

**Add a field for uncertainty:**

```json
{
  "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
  "unclear_fields": {"type": "array", "items": {"type": "string"}}
}
```

Constrained decoding guarantees the *shape*, not the *truth*. Giving the model a place to express uncertainty is much better than forcing confident nonsense into a required field.

---

## Strict tool use

```python
tools = [{
    "name": "create_ticket",
    "description": "Create a support ticket. Use when the user reports a problem needing tracking.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "priority": {"type": "string", "enum": ["p0", "p1", "p2", "p3"]},
            "component": {"type": "string", "enum": ["api", "web", "mobile", "billing"]},
        },
        "required": ["title", "priority", "component"],
        "additionalProperties": False,
    },
}]
```

Guarantees the tool name and input validate against the schema. Use it on anything where malformed input would break something downstream — which is most tools that write.

---

## Where this fits in a pipeline

Structured outputs is what makes Claude a **component** rather than a chat interface:

```
raw text  →  Claude (schema-constrained)  →  typed object  →  your business logic
```

Combine with Pydantic (Python) or Zod (TypeScript) to get types on both sides:

```python
from pydantic import BaseModel

class Extraction(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool

response = client.messages.create(
    ...,
    output_config={"format": {"type": "json_schema", "schema": Extraction.model_json_schema()}},
)
result = Extraction.model_validate_json(text_of(response))
```

One schema definition, used for both the constraint and the validation.

---

## Structured outputs in agent workflows

For agents that do multi-turn tool use and *then* need to return a typed result, both the Agent SDK and the Claude Code CLI support it:

```bash
claude -p --json-schema '{"type":"object","properties":{...}}' "assess the risk"
```

See [Get structured output from agents](https://code.claude.com/docs/en/agent-sdk/structured-outputs).

---

## Try it

**Exercise 1 — Extraction.**
Take twenty messy real-world texts (emails, support tickets, meeting notes). Define a schema. Extract from all twenty. Count schema violations. (Should be zero.)

**Exercise 2 — Enum classification.**
Build a classifier with an enum-constrained output. Compare against the same task with a free-text output — count how many normalisation cases you had to handle in the free-text version.

**Exercise 3 — Uncertainty fields.**
Add `confidence` and `unclear_fields` to a schema. Run it on deliberately ambiguous inputs. Note whether the model uses them honestly.

**Exercise 4 — Typed round trip.**
Generate the schema from a Pydantic or Zod model and validate the result back into it. One definition, both ends.

**Exercise 5 — Migration.**
If you have any code using prefill or the tool-as-schema hack, migrate it to `output_config.format`.

**Exercise 6 — Strict tools.**
Add `strict: True` to a write tool. Try to get Claude to produce invalid input.

---

## Checkpoint

- You use `output_config.format` rather than prompting for JSON and hoping
- Your schemas use enums for categoricals and have a place for uncertainty
- You generate schemas from your type definitions rather than duplicating them

---

## Going deeper

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
- [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Structured outputs in the Agent SDK](https://code.claude.com/docs/en/agent-sdk/structured-outputs)
