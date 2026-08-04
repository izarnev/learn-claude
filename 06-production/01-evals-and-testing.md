---
title: "01 · Evals and testing"
---

# 01 · Evals and testing

**What you'll learn:** how to know whether a change made things better — the discipline that separates shipping from guessing.

---

## Why this comes before optimisation

Without evals you are tuning prompts based on vibes and the last three examples you happened to look at. Everyone does this at first. It stops working the moment you have more than one use case.

**The rule: define success criteria before you write the prompt.**

---

## Success criteria that work

A usable criterion is:

- **Specific** — "accuracy on the ticket-classification set", not "quality"
- **Measurable** — a number, or a rubric a judge can apply consistently
- **Achievable** — benchmarked against something (a human baseline, the current system)
- **Relevant** — it matters to your actual users

**Multidimensional.** Nearly every real system needs several: accuracy, latency, cost, safety, format compliance. Optimising one alone will degrade another. Write them all down.

---

## Building an eval set

### Start small and real

**Twenty real examples beat two hundred synthetic ones.** Pull them from actual usage, actual tickets, actual documents.

### Cover the distribution, not just the middle

| Category | Include |
|---|---|
| **Typical** | The 80% case |
| **Edge cases** | Empty input, enormous input, malformed input, unusual formats |
| **Adversarial** | Prompt injection attempts, jailbreak attempts, off-topic requests |
| **Known failures** | Every bug you've ever fixed, permanently |

That last row is your regression suite. Every time you fix something, add the failing case.

### Store it as data

```json
{
  "id": "ticket-042",
  "input": "...",
  "expected": {"severity": "high", "component": "billing"},
  "tags": ["edge-case", "multi-issue"],
  "added_because": "regression: v2 misclassified multi-issue tickets"
}
```

Version it in git alongside your prompts.

---

## Grading methods

| Method | Use for | Cost |
|---|---|---|
| **Exact match** | Classification, extraction with a known answer | Free |
| **Schema validation** | Structured outputs | Free |
| **Programmatic checks** | Format rules, length, forbidden words, JSON validity | Free |
| **Code execution** | Generated code — does it run, do the tests pass? | Cheap |
| **LLM-as-judge** | Quality, tone, helpfulness | Model call |
| **Human review** | The final arbiter; calibrating your judge | Expensive |

**Order of preference: prefer the cheapest method that actually measures what you care about.** Most teams reach for LLM-as-judge too early, when a schema check and a regex would have caught the real failures.

### LLM-as-judge, done properly

```python
JUDGE_PROMPT = """
<rubric>
1. Accuracy (1-5): every factual claim is supported by the source. Any
   unsupported claim caps this at 2.
2. Completeness (1-5): addresses every part of the question.
3. Format (pass/fail): matches the required structure exactly.
</rubric>

<source>{source}</source>
<question>{question}</question>
<response>{response}</response>

Score against the rubric. For each criterion give the score and a one-sentence
justification quoting the specific text that determined it.

Output JSON: {{"accuracy": n, "completeness": n, "format": "pass"|"fail",
"justifications": {{...}}}}
"""
```

Rules for judges:

- **Concrete rubrics with anchors.** "1-5 on quality" produces noise; "any unsupported claim caps this at 2" produces signal.
- **Require justification with quotes.** Improves consistency and lets you audit the judge.
- **Use structured outputs** so results are parseable.
- **Calibrate against humans.** Score 30 examples by hand, compare against the judge, fix the rubric where they disagree. Do this before you trust it.
- **Use a strong model as judge**, even if production runs on a cheap one.

---

## Running evals

Use the **Batch API**. Evals are the canonical batchable workload — no user is waiting, and the discount is substantial.

```python
batch = client.messages.batches.create(
    requests=[
        {"custom_id": ex["id"], "params": {...build_request(ex)...}}
        for ex in eval_set
    ]
)
```

Combine with prompt caching if every case shares a large prefix.

Report:

| | |
|---|---|
| Score per dimension | Mean and distribution, not just mean |
| Failures | Listed individually, with input and output |
| Cost and latency | Per example |
| Diff vs. previous run | **The most important output** |

The diff is what tells you whether your change helped. A single absolute score tells you almost nothing.

---

## The workflow

```
1. Define success criteria
2. Build an eval set from real data
3. Write a baseline prompt
4. Run the eval → record the number
5. Change ONE thing
6. Run again → compare
7. Keep or revert
8. Add every new failure to the eval set
```

**One change at a time.** Changing the prompt, the model, and the temperature together tells you nothing about which mattered.

---

## Testing agents

Agents need everything above plus:

**Trajectory evaluation.** Grade not just the final answer but the path: did it call the right tools? In a sensible order? Did it verify before claiming success? A correct answer reached by luck is a bug you haven't found yet.

**Deterministic tool mocks.** Real tools make eval runs non-reproducible. Mock them for evals; test the real integration separately.

**Failure injection.** Make a tool error. Make it time out. Return nonsense. See what happens. Agents that have never seen a tool failure handle their first one in production badly.

**Cost and turn distribution.** Report p50 and p95 turns and cost, not just the mean. The mean hides the runaway.

**Termination testing.** Give it a task it cannot complete. Confirm it stops cleanly and says why.

---

## The Console

The Claude Console includes a prompt workbench and evaluation tooling — a reasonable place to start before building your own harness.

---

## Try it

**Exercise 1 — Twenty real examples.**
For something you're actually building, collect twenty real inputs with expected outputs. This is the exercise; everything else is easy afterwards.

**Exercise 2 — Baseline.**
Run your current prompt against them. Record the number. You now have a baseline you didn't have.

**Exercise 3 — One change.**
Change one thing. Rerun. Compare. Notice how often your intuition about what would help was wrong.

**Exercise 4 — Judge calibration.**
Build an LLM judge. Score 30 examples by hand. Compare. Fix the rubric. Repeat until agreement is high.

**Exercise 5 — Regression suite.**
Take every bug you've fixed in this project. Add each as an eval case. Run the suite.

**Exercise 6 — Failure injection.**
Make a tool in your agent fail. Watch what happens. Fix it. Add it to the eval set.

---

## Checkpoint

- You have an eval set of real examples, versioned in git
- You have a baseline number
- Every bug you fix becomes an eval case
- You change one thing at a time

---

## Going deeper

- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
- [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
