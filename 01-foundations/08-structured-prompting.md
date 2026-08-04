# 08 · Structured prompting with XML

**What you'll learn:** how to build reliable, reusable prompt templates using XML structure — the bridge between casual chat and production prompting.

---

## Why structure at all

A casual prompt is a paragraph. A structured prompt is a form. The difference matters as soon as:

- You reuse the prompt with different inputs
- The prompt mixes several kinds of content (instructions, data, examples, constraints)
- Someone else needs to maintain it
- You need to reliably parse the output

Claude parses XML-tagged prompts noticeably more accurately than prose-blob prompts, because the tags remove any question about which text is an instruction and which is data.

---

## The anatomy of a structured prompt

There's no fixed schema. These are conventions that work.

```xml
<role>
You are a technical editor for a developer documentation team.
</role>

<task>
Rewrite the draft below so a competent engineer unfamiliar with this system
can follow it. Preserve every factual claim exactly.
</task>

<style_guide>
- Second person, present tense
- Code identifiers in backticks
- No marketing language
- Each procedure step starts with a verb
</style_guide>

<examples>
  <example>
    <before>The system will then proceed to validate the provided token.</before>
    <after>The system validates the token.</after>
  </example>
  <example>
    <before>It is recommended that users configure the timeout value.</before>
    <after>Set `timeout` to the number of seconds you want to wait.</after>
  </example>
</examples>

<draft>
{{DRAFT_TEXT}}
</draft>

<output_format>
Return the rewritten draft only, in <rewritten> tags. After it, list any factual
claims you were unsure about in <flags> tags, one per line.
</output_format>
```

Every section earns its place: role sets the lens, task states the job, style_guide gives verifiable rules, examples show what description can't, draft is the variable input, output_format makes the response parseable.

---

## Ordering rules

The order is not arbitrary.

1. **Role** (if any) — first, so everything after is read through it
2. **Long reference material** — near the top, per the long-context rule
3. **Instructions and constraints**
4. **Examples**
5. **The variable input**
6. **Output format** — last, closest to where the model starts generating

The critical one: **long documents at the top, the actual question at the bottom.** Up to 30% quality improvement on complex multi-document inputs.

---

## Output tags: making responses parseable

Asking for XML output is the simplest reliable way to separate reasoning from result:

```xml
<output_format>
<analysis>Your reasoning. Not shown to the user.</analysis>
<answer>The final answer only.</answer>
<confidence>high | medium | low</confidence>
</output_format>
```

Then you extract `<answer>` and discard the rest. This works in chat and is the basis for a lot of production prompting. (In the API there's a stronger mechanism — [structured outputs](../04-api/06-structured-outputs.md) — but XML tags work everywhere and require no special support.)

---

## Templating: variables and reuse

Use a placeholder convention and stay consistent. `{{DOUBLE_BRACES}}` is common because it never collides with anything Claude produces naturally.

```xml
<context>
Company: {{COMPANY_NAME}}
Industry: {{INDUSTRY}}
Audience: {{AUDIENCE}}
</context>

<task>
Write a {{LENGTH}}-word {{DOCUMENT_TYPE}} about {{TOPIC}}.
</task>
```

Now this is a reusable asset. Fill it in by hand in chat, or programmatically in code. Once you have three or four of these, you have a prompt library — and that's exactly the thing that becomes a **Skill** in [02-power-user/02](../02-power-user/02-skills.md).

---

## Common structured patterns

### Extraction

```xml
<document>{{TEXT}}</document>

<task>Extract every commitment made in the document above.</task>

<output_format>
One line per commitment, pipe-delimited:
who | what | by_when | source_quote

If a field is absent, write UNKNOWN. Do not infer.
</output_format>
```

The `do not infer` is doing real work — without it, Claude fills gaps helpfully and you get invented deadlines.

### Grounded analysis

```xml
<documents>{{DOCS}}</documents>

<task>{{QUESTION}}</task>

<method>
1. Extract quotes relevant to the question into <quotes> tags, with source labels.
2. Answer using only those quotes, in <answer> tags.
3. If the quotes are insufficient, say so in <answer> instead of speculating.
</method>
```

### Evaluation / rubric

```xml
<rubric>
- Clarity (1-5): can a new reader follow it without rereading?
- Accuracy (1-5): are all claims supported?
- Concision (1-5): could 20% be cut without loss?
</rubric>

<submission>{{TEXT}}</submission>

<output_format>
<scores>criterion: score — one-sentence justification</scores>
<top_fix>The single highest-impact change.</top_fix>
</output_format>
```

### Chained self-correction

Not a single prompt but a three-step pattern, and the most reliable quality boost available:

1. **Draft** — generate
2. **Critique** — "Review the draft against these criteria. List every problem. Do not rewrite."
3. **Revise** — "Now rewrite addressing every problem you listed."

Separating critique from revision matters. When you ask for both at once, Claude tends to produce a mild critique that justifies minimal changes.

---

## What *not* to do

**Don't over-structure trivial prompts.** "Summarise this in three bullets" doesn't need XML.

**Don't invent tags Claude has to guess at.** `<x>` and `<data2>` help nobody. Use names that describe content.

**Don't nest four levels deep.** Two is almost always enough.

**Don't shout.** `CRITICAL: YOU MUST ALWAYS` was necessary for older models. Current models over-trigger on it. Write normally.

---

## Try it

**Exercise 1 — Build a template.**
Take a task you do repeatedly. Write it as a structured prompt with role, task, constraints, examples, input placeholder, and output format. Run it on three different inputs. Refine.

**Exercise 2 — Parseable output.**
Rewrite one of your existing prompts to return `<answer>` and `<confidence>` tags. Notice how much easier it is to use the result.

**Exercise 3 — The self-correction chain.**
Write something with Claude. Then run the three-step chain. Compare draft to final. Then try asking for critique-and-revision in one message and compare that too — you'll see why separation matters.

**Exercise 4 — Extraction with a no-infer rule.**
Extract structured data from a messy document twice: once without `do not infer`, once with. Count the invented fields in the first.

**Exercise 5 — Start your prompt library.**
Create `claude-practice/prompts/` and save every template you've built so far as its own file. You'll convert these to Skills in the next stage.

---

## Checkpoint

- You can build a structured prompt from scratch with the six standard sections in the right order
- You know why long input goes at the top and the question at the bottom
- You've run the draft → critique → revise chain and seen the difference

---

## Going deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
