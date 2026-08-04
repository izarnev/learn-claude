---
title: "Prompting cheat sheet"
order: 3
---

# Prompting cheat sheet

Copy-paste patterns. Everything here is used in the modules; this is the lookup version.

---

## The golden rule

> Show your prompt to a colleague with minimal context and ask them to follow it. If they'd be confused, Claude will be too.

---

## The six fundamentals

| # | Technique | One line |
|---|---|---|
| 1 | Be clear and direct | Say the format, the constraints, and the level of ambition |
| 2 | Explain *why* | Motivation generalises; prohibition doesn't |
| 3 | Use examples | 3–5, relevant, diverse, wrapped in `<example>` tags |
| 4 | Structure with XML | Removes ambiguity between instruction and data |
| 5 | Give a role | One sentence in the system prompt shifts tone and focus |
| 6 | Long input at the top, question at the bottom | Up to 30% better on multi-document inputs |

---

## Structured prompt template

```xml
<role>You are a [specific role with relevant priorities].</role>

<task>[What to do, specifically.]</task>

<constraints>
- [Verifiable rule]
- [Verifiable rule]
</constraints>

<examples>
  <example><input>...</input><output>...</output></example>
  <example><input>...</input><output>...</output></example>
</examples>

<input>{{VARIABLE}}</input>

<output_format>
<analysis>Your reasoning.</analysis>
<answer>The answer only.</answer>
<confidence>high | medium | low</confidence>
</output_format>
```

Order: role → long reference material → instructions → examples → variable input → output format.

---

## Formatting control

**Tell it what to do, not what to avoid.**

| Doesn't work | Works |
|---|---|
| `Do not use markdown` | `Compose your response in smoothly flowing prose paragraphs.` |
| `Don't be verbose` | `Answer in under 100 words.` |
| `No bullet points` | `Write in complete paragraphs.` |

**Prose instead of bullet soup:**

```
When writing reports, explanations, or analyses, write in clear flowing prose
using complete paragraphs. Reserve markdown for inline code, code blocks, and
simple headings. Do not use ordered or unordered lists unless you're presenting
truly discrete items or I explicitly ask for one. Incorporate items naturally
into sentences instead.
```

**Plain text maths (models default to LaTeX):**

```
Format your response in plain text only. Do not use LaTeX, MathJax, or markup
such as \( \), $, or \frac{}{}. Write math using standard text characters.
```

Also: your prompt's style influences the output's style. Heavy markdown in, heavy markdown out.

---

## Workflow patterns

**Chain of critique** — the highest-value pattern here:

```
1. "Write X."
2. "Review the draft against these criteria: [...]. List every problem.
    Do not rewrite anything."
3. "Now rewrite, addressing every problem you listed."
4. (optional) "Now argue the revision is still wrong. Take the position of a
    hostile reviewer who wants to reject it."
```

**Ask first:**

```
Before you start, ask me up to five questions whose answers would materially
change your response. Don't ask questions you can answer from what I've given you.
```

**Force alternatives:**

```
Give me three genuinely different approaches. They must differ in kind, not
degree. For each: the approach, what it optimises for, what it sacrifices, and
who it's wrong for. Then recommend one and say what would change your
recommendation.
```

**Rubric first:**

```
Step 1: Write a rubric for what makes an excellent [thing]. Five criteria, each
with a concrete test.
Step 2: Now write the [thing], optimising for that rubric.
Step 3: Score your output against it. Where below 4/5, revise.
```

**Grounding:**

```
1. Extract every passage relevant to the question into <quotes> tags with locations.
2. Answer using only those quotes, in <answer> tags.
3. If the quotes are insufficient, say what's missing rather than filling the gap.
```

**Persona ensemble:**

```
Analyse from four perspectives, each in its own section: a CFO focused on
payback and downside risk; a senior engineer who'll maintain it; a customer who
uses it; a competitor who wants us to make a mistake. Then synthesise: where do
they agree, where do they conflict, what would resolve the conflicts?
```

**Constraint stacking** — adding constraints improves output by removing generic answers. Include a banned-word list.

**Negative examples** — always give the reason:

```xml
<bad_example reason="vague, no impact stated, passive voice">
Some improvements were made to webhook handling.
</bad_example>
```

---

## Agentic steering

**Act rather than suggest:**

```
By default, implement changes rather than only suggesting them. If my intent is
unclear, infer the most useful likely action and proceed, using tools to
discover missing details instead of guessing.
```

**Research rather than act:**

```
Do not jump into implementation or change files unless clearly instructed. When
my intent is ambiguous, default to information, research, and recommendations.
```

**Confirmation gate:**

```
Consider the reversibility and potential impact of your actions. Take local,
reversible actions freely, but for actions that are hard to reverse, affect
shared systems, or could be destructive, ask before proceeding.

Warrants confirmation: deleting files or branches, dropping tables, rm -rf,
git push --force, git reset --hard, amending published commits, pushing code,
commenting on PRs, sending messages, modifying shared infrastructure.

When you hit an obstacle, don't use destructive actions as a shortcut. Don't
bypass safety checks (e.g. --no-verify) or discard unfamiliar files.
```

**Stop over-engineering:**

```
Only make changes that are directly requested or clearly necessary.
Scope: don't add features, refactor, or make improvements beyond what was asked.
Documentation: don't add docstrings or comments to code you didn't change.
Defensive coding: don't add error handling for scenarios that can't happen.
Only validate at system boundaries.
Abstractions: don't create helpers for one-time operations. Don't design for
hypothetical future requirements.
```

**Don't cheat the tests:**

```
Write a high-quality, general-purpose solution. Don't hard-code values or write
solutions that only work for the test cases. Tests verify correctness; they
don't define the solution. If a test is wrong, tell me rather than working
around it.
```

**Don't hallucinate about code:**

```
Never speculate about code you have not opened. If I reference a specific file,
read it before answering. Investigate relevant files BEFORE answering questions
about the codebase.
```

**Clean up:**

```
If you create temporary files or scripts for iteration, remove them at the end.
```

---

## Parallel tool calls

**Maximise:**

```
If you intend to call multiple tools and there are no dependencies between them,
make all independent calls in parallel. When reading 3 files, run 3 tool calls
at once. If some calls depend on previous ones for their parameters, call those
sequentially. Never use placeholders or guess missing parameters.
```

**Reduce:**

```
Execute operations sequentially with brief pauses between each step.
```

---

## Thinking control

**Too much thinking:**

```
Thinking adds latency and should only be used when it will meaningfully improve
answer quality — typically for problems requiring multistep reasoning. When in
doubt, respond directly.
```

**More deliberation after tools:**

```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding.
```

**Stop over-exploring:**

```
When deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning.
```

---

## Long-horizon work

**During:**

```
This is a long task. Plan your work clearly.
Keep state in files: tests.json for structured status, progress.txt for notes.
Use git commits as checkpoints.
Focus on incremental progress. Before running low on context, save your progress
and state so a fresh session can continue.
It's encouraged to spend your entire output context on the task — just don't run
out with significant uncommitted work.
```

**Resuming fresh:**

```
Run pwd. Review progress.txt, tests.json, and the git log. Run the integration
test manually before implementing anything new.
```

**Persistence (if your harness compacts):**

```
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely from where you left off. Do not
stop tasks early due to token budget concerns. As you approach the limit, save
your progress and state before the context refreshes. Never artificially stop a
task early regardless of remaining context.
```

---

## Subagent damping

```
Use subagents when tasks can run in parallel, require isolated context, or
involve independent workstreams that don't need to share state. For simple
tasks, sequential operations, single-file edits, or tasks needing context
continuity, work directly rather than delegating.
```

---

## Frontend aesthetics

Models converge on generic choices without guidance. Specify:

```
Typography: choose beautiful, distinctive fonts. Avoid Inter, Roboto, Arial,
system fonts.
Colour: commit to a cohesive aesthetic. Use CSS variables. Dominant colours with
sharp accents beat timid even palettes. Avoid purple gradients on white.
Motion: high-impact moments. One well-orchestrated page load with staggered
reveals beats scattered micro-interactions.
Backgrounds: create atmosphere and depth. Layer gradients, patterns, contextual
effects.
Make unexpected choices that feel designed for this specific context.
```

---

## Anti-patterns

| Don't | Because |
|---|---|
| `CRITICAL: YOU MUST ALWAYS` | Current models over-trigger on aggressive language |
| `Do not use markdown` | Negative formatting instructions work poorly |
| Arguing across five turns | Edit the original prompt and re-run |
| `Be thorough` on Opus 5 | It already self-verifies; causes over-verification |
| Prefilled assistant messages | Unsupported on 4.6+; returns a 400 |
| One giant prompt for a ten-step task | Chain it; inspect and correct at each step |
| Assuming an old prompt still works on a new model | Model behaviour genuinely changes |

---

Source: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
