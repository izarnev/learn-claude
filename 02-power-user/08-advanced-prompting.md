# 08 · Advanced prompting patterns

**What you'll learn:** the patterns that separate competent prompting from expert prompting — most of which are about *structuring the work*, not phrasing the request.

---

## Pattern 1 — Chain of critique

The highest-value pattern in this document. Three separate turns:

```
1. DRAFT     "Write X."
2. CRITIQUE  "Review the draft against these criteria: [...].
              List every problem. Do not rewrite anything."
3. REVISE    "Now rewrite, addressing every problem you listed."
```

Why the separation matters: when you ask for critique-and-revision in one message, Claude produces a mild critique that justifies minimal changes. Forced to critique *first*, with no ability to fix, it finds real problems.

Add a fourth step for hard work: **adversarial critique.**

```
4. "Now argue that the revision is still wrong. Take the position of a hostile
    reviewer who wants to reject it. What's the strongest case against it?"
```

---

## Pattern 2 — Make it ask first

```
Before you start, ask me up to five questions whose answers would materially
change your response. Don't ask questions you can answer from what I've given you.
```

That second sentence is important — without it you get five questions, three of which are already answered in your prompt.

Use for: anything ambiguous, anything where you're not sure what you want, anything with stakeholders.

---

## Pattern 3 — Force the alternatives

Claude will happily give you one answer. Making it give you three, then choose, produces better single answers.

```
Give me three genuinely different approaches to X. They must differ in kind,
not in degree — not three variations on the same idea.

For each: the approach, what it optimises for, what it sacrifices, and who it's
wrong for.

Then recommend one and say what would change your recommendation.
```

The "what would change your recommendation" clause is doing quiet work: it forces Claude to surface the assumptions its answer rests on.

---

## Pattern 4 — Rubric-first

Define what good looks like *before* generating.

```
Step 1: Write a rubric for what makes an excellent [thing]. Five criteria,
each with a concrete test I could apply.

[review the rubric, adjust]

Step 2: Now write the [thing], optimising for that rubric.

Step 3: Score your output against the rubric. Where it scores below 4/5, revise.
```

This is more work than one prompt and produces dramatically better output on anything you care about. It also gives you a reusable rubric — which is a Skill waiting to happen.

---

## Pattern 5 — Grounding and evidence

From [01-foundations/02](../01-foundations/02-prompting-fundamentals.md), but worth repeating because it's the main hallucination defence:

```
Step 1: Extract every passage from the source relevant to the question into
<quotes> tags, with locations.

Step 2: Answer using only those quotes, in <answer> tags.

Step 3: If the quotes don't support a complete answer, say what's missing
rather than filling the gap.
```

Step 3 is the one people leave out, and it's the one that stops confident invention.

---

## Pattern 6 — Persona ensemble

For decisions with multiple legitimate perspectives:

```
Analyse this proposal from four perspectives, each in its own section:

1. A CFO who cares about payback period and downside risk
2. A senior engineer who will have to maintain it
3. A customer who will use it
4. A competitor who wants us to make a mistake

Then synthesise: where do they agree, where do they conflict, and what would
resolve the conflicts?
```

The competitor perspective is unusually productive — it surfaces weaknesses friendly perspectives politely skip.

---

## Pattern 7 — Constraint stacking

Adding constraints usually *improves* output rather than restricting it, because it removes the space of generic answers.

```
Weak:   Write a product announcement.

Strong: Write a product announcement.
        - Under 150 words
        - No adjectives in the first sentence
        - Must include one specific number
        - Must state what it does NOT do
        - Reading level: someone skimming on a phone
        - No words from this list: seamless, powerful, revolutionary,
          leverage, robust, unlock, empower
```

The banned-word list alone transforms marketing copy.

---

## Pattern 8 — Negative examples

Positive examples show the target. Negative examples show the failure mode you keep hitting.

```xml
<good_example>
Fixed a race condition in the payment webhook handler that could double-charge
customers under high load. (PR #4412)
</good_example>

<bad_example reason="vague, no impact stated, passive voice">
Some improvements were made to webhook handling.
</bad_example>

<bad_example reason="too technical for the audience, no user impact">
Refactored WebhookDispatcher to use a mutex-guarded idempotency cache keyed on
Stripe event ID.
</bad_example>
```

The `reason` attribute is what makes these work. A bad example without a stated reason teaches ambiguously.

---

## Pattern 9 — Steering agentic behaviour

Relevant in Cowork, Claude Code, and any tool-using context. These are lifted from Anthropic's own guidance and work verbatim.

**Make Claude act rather than suggest:**

```
By default, implement changes rather than only suggesting them. If my intent is
unclear, infer the most useful likely action and proceed, using tools to discover
missing details instead of guessing.
```

**Make Claude research rather than act:**

```
Do not jump into implementation or change files unless clearly instructed. When
my intent is ambiguous, default to providing information, research, and
recommendations rather than taking action.
```

**Add a confirmation gate on risky actions:**

```
Consider the reversibility and potential impact of your actions. Take local,
reversible actions freely, but for actions that are hard to reverse, affect
shared systems, or could be destructive, ask me before proceeding.

Warrants confirmation: deleting files or branches, dropping tables, rm -rf,
git push --force, git reset --hard, amending published commits, pushing code,
commenting on PRs, sending messages, modifying shared infrastructure.

When you hit an obstacle, don't use destructive actions as a shortcut. Don't
bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be
in-progress work.
```

**Stop over-engineering:**

```
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary.

Scope: don't add features, refactor, or make "improvements" beyond what was
asked. A bug fix doesn't need surrounding code cleaned up.

Documentation: don't add docstrings, comments, or type annotations to code you
didn't change.

Defensive coding: don't add error handling or validation for scenarios that
can't happen. Only validate at system boundaries.

Abstractions: don't create helpers for one-time operations. Don't design for
hypothetical future requirements.
```

**Stop hallucination about code:**

```
Never speculate about code you have not opened. If I reference a specific file,
read it before answering. Investigate relevant files BEFORE answering questions
about the codebase.
```

---

## Pattern 10 — Long-horizon work

For tasks spanning multiple sessions or context windows:

```
This is a long task. Plan your work clearly.

Keep state in files:
- tests.json for structured status
- progress.txt for freeform notes on what you did and what's next

Use git as a checkpoint log.

Focus on incremental progress — advance a few things at a time rather than
attempting everything at once. Before you run low on context, save your
progress and state so a fresh session can continue.
```

And for the *next* session:

```
Run pwd. Review progress.txt, tests.json, and the git log. Run the integration
test manually before implementing anything new.
```

Anthropic's guidance notes that current models are extremely effective at discovering state from the filesystem — often more effective than resuming from a compacted context. Starting fresh with good state files can beat continuing.

---

## Anti-patterns

| Don't | Because |
|---|---|
| `CRITICAL: YOU MUST ALWAYS` | Current models over-trigger on aggressive language. Write normally. |
| `Do not use markdown` | Negative formatting instructions work poorly. Say what to do instead. |
| Arguing with Claude across five turns | Edit the original prompt and re-run. |
| `Be thorough` on Opus 5 | It already self-verifies. Adding this causes over-verification and wasted tokens. |
| One giant prompt for a ten-step task | Chain it. You can inspect and correct at each step. |
| Assuming a prompt that worked on an old model still works | Model behaviour genuinely changes. Retest on migration. |

---

## Try it

**Exercise 1 — The full chain.**
Take something you actually need to write. Run draft → critique → revise → adversarial critique → final. Time it. Judge whether the quality gain was worth the four extra minutes. (For anything you'll send to more than five people, it is.)

**Exercise 2 — Rubric-first.**
Same task, but build the rubric first. Compare against the chain-of-critique version.

**Exercise 3 — Banned words.**
Take a piece of your own writing. Extract the ten words you overuse. Add them as a banned list to your custom instructions. Live with it for a week.

**Exercise 4 — Three approaches.**
Apply pattern 3 to a real decision you're facing. Note whether Claude's recommendation matches your prior — and whether the "what would change my recommendation" clause surfaced an assumption you hadn't examined.

**Exercise 5 — Build your pattern library.**
Create `claude-practice/prompts/patterns.md`. Copy in the patterns from this module that you'll actually use. Add your own as you find them. This file is the deliverable of stage 02.

---

## Checkpoint

- You've run the chain of critique on real work and can say whether it's worth it
- You have a written pattern library
- You know at least three ways to steer agentic behaviour and when each applies

---

## Going deeper

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
- [Prompt library](https://code.claude.com/docs/en/prompt-library)
