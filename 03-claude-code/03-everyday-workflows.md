# 03 · Everyday workflows

**What you'll learn:** the concrete patterns for the things you'll actually do with Claude Code every day.

---

## Exploring an unfamiliar codebase

Don't ask it to change anything yet.

```
1. give me a high-level map of this repo: what are the main modules and how do
   they relate?
2. where does a request enter the system, and what path does it take?
3. what are the three files I'd need to understand to make a change to auth?
4. what's unusual about this codebase — conventions someone new would get wrong?
```

That last question is unusually productive, and the answer is often the first entry in your CLAUDE.md.

For very large codebases, install a **code intelligence plugin** for your language — Claude gets symbol-level navigation via a language server instead of grepping, which is both faster and more accurate. See [Discover plugins](https://code.claude.com/docs/en/discover-plugins#code-intelligence).

---

## Fixing a bug

The pattern that works:

```
Here's the error:
[paste the stack trace]

Reproduce it, find the root cause, and fix it. Don't fix symptoms —
if the root cause is somewhere else, fix it there and tell me why.
Add a test that fails before your fix and passes after.
```

Three things that make this work:

1. **The stack trace.** Give it the actual error, not a description of the error.
2. **"Reproduce it."** Forces verification rather than plausible-looking guessing.
3. **"Add a failing test first."** This is the difference between a fix and a claim of a fix.

If you don't have a stack trace: describe the symptom, when it started, and what changed. Claude is good at bisecting through git history.

---

## Building a feature

Use plan mode. Genuinely.

```
Shift+Tab → plan
```

Then:

```
I want to add rate limiting to the public API.

Constraints: per-API-key, sliding window, must work across our three app
servers. We already run Redis.

Give me a plan. Include: files you'd touch, the approach, what you'd test,
and anything you're unsure about.
```

Read the plan. Correct it. *Then* let it execute. The five minutes you spend reading a plan saves an hour of unwinding a wrong approach.

For large features, `/ultraplan` drafts the plan in the cloud with more thorough exploration, and you can execute it remotely or back in your terminal.

---

## Refactoring

Refactors go wrong when Claude changes behaviour while changing structure. Anchor it:

```
Refactor the payment module to use async/await instead of callbacks.

Before you start: run the test suite and record what passes.
After: run it again. The same tests must pass. No behaviour changes.
If a test was already failing, leave it failing — don't fix it as part of this.

Work file by file and show me the diff for each before moving on.
```

For very large migrations, use **dynamic workflows** — Claude writes a script that orchestrates many subagents, which you can inspect and rerun. See [Orchestrate subagents at scale](https://code.claude.com/docs/en/workflows).

---

## Writing tests

```
Write unit tests for src/billing/proration.ts.

Cover: the happy path, the three edge cases in the comments, and what happens
with a zero-length billing period.

Do not modify the source file. If you find a bug while writing tests, tell me
rather than fixing it.
```

That last line is important. Left alone, Claude will helpfully "fix" the code to make its tests pass, which is exactly backwards.

---

## Code review

Two options:

**In-session:** `/code-review` reviews your working diff. `/code-review ultra` runs a deep multi-agent review in the cloud (`/ultrareview`), which finds and verifies bugs before you merge.

**On PRs:** `/review` reviews a GitHub PR. For automated review on every PR, set up [GitHub Code Review](https://code.claude.com/docs/en/code-review).

**Ad hoc:**

```bash
git diff main --name-only | claude -p "review these changed files for security issues"
```

---

## Commits and PRs

```
commit my changes with a descriptive message
```

Claude reads the diff, writes a message that describes *why* not just what, stages, and commits.

```
open a PR for this branch. Description should cover: what changed, why,
how to test it, and anything a reviewer should look at closely.
```

---

## The Unix-composable patterns

Claude Code follows the Unix philosophy. These are worth internalising:

```bash
# Analyse logs
tail -200 app.log | claude -p "flag any anomalies"

# Review a diff
git diff main --name-only | claude -p "review these for security issues"

# Bulk operations in CI
claude -p "translate new strings into French and raise a PR for review"

# One-off, no session persistence, fast startup
claude --bare -p "what does this regex do: $REGEX"

# Structured output for scripting
claude -p "list the exported functions in src/" --output-format json
```

`--bare` skips auto-discovery of hooks, skills, plugins, MCP servers, auto memory and CLAUDE.md, which makes scripted calls start much faster.

---

## Parallel work

Three mechanisms, escalating:

**Worktrees** — isolate parallel sessions so changes don't collide:

```bash
claude -w feature-auth       # session in .claude/worktrees/feature-auth
claude -w feature-auth --tmux
```

**Background sessions** — start and walk away:

```bash
claude --bg "investigate the flaky test in test_billing.py"
claude agents                # agent view: monitor everything from one screen
claude logs 7c5dcf5d         # check on one
claude attach 7c5dcf5d       # take it over
```

**Subagents and agent teams** — covered in [module 07](07-subagents-and-parallelism.md).

---

## Goal-driven work

`/goal` sets a completion condition, and Claude keeps working across turns until it's met:

```
/goal all tests in the billing suite pass and coverage is above 80%
```

Related: `/loop` repeats a prompt within a session — useful for polling a build or a deploy.

---

## Prompting patterns specific to Claude Code

**Investigate before answering:**

```
Never speculate about code you haven't opened. If I reference a specific file,
read it before answering.
```

**Stop over-engineering:**

```
Only make changes that are directly requested or clearly necessary. Don't add
features, refactor surrounding code, add docstrings to code you didn't change,
or create abstractions for one-time operations.
```

**Confirm before destructive actions:**

```
Take local, reversible actions freely. For anything hard to reverse, affecting
shared systems, or destructive, ask me first: deleting files or branches,
git push --force, git reset --hard, amending published commits, pushing code,
commenting on PRs.

Never bypass safety checks (--no-verify) as a shortcut.
```

**Don't cheat the tests:**

```
Write a high-quality, general-purpose solution. Don't hard-code values or write
solutions that only work for the test cases. Tests verify correctness; they
don't define the solution. If a test is wrong, tell me rather than working
around it.
```

**Clean up scratch files:**

```
If you create temporary files or scripts for iteration, remove them at the end.
```

Put the ones you always want in CLAUDE.md. Put the situational ones in your prompt.

---

## Try it

**Exercise 1 — Orientation on unfamiliar code.**
Clone an open-source project you've never seen. Run the four exploration questions. Then find a `good-first-issue` and fix it.

**Exercise 2 — Bug with a failing test.**
Introduce a subtle bug in your own code. In a fresh session, give Claude only the symptom. Require a failing test before the fix.

**Exercise 3 — Plan mode discipline.**
For your next real feature, use plan mode and *do not skip reading the plan*. Note every correction you made. Those corrections are CLAUDE.md entries.

**Exercise 4 — Refactor with a test anchor.**
Refactor something with the "same tests must pass" constraint. Verify by actually running the tests yourself afterwards.

**Exercise 5 — Pipe pattern.**
Build one shell one-liner that pipes real data into `claude -p` and produces something useful. Add it to your shell aliases.

**Exercise 6 — Background session.**
Kick off `claude --bg` on a slow investigation. Do something else. Come back with `claude logs`.

---

## Checkpoint

- Plan mode is a habit, not something you remember afterwards
- Your bug-fix prompts always ask for a failing test first
- You've composed Claude Code into at least one shell pipeline

---

## Going deeper

- [Common workflows](https://code.claude.com/docs/en/common-workflows)
- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Prompt library](https://code.claude.com/docs/en/prompt-library)
- [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees)
- [Manage multiple agents with agent view](https://code.claude.com/docs/en/agent-view)
- [Plan in the cloud with ultraplan](https://code.claude.com/docs/en/ultraplan)
- [Find bugs with ultrareview](https://code.claude.com/docs/en/ultrareview)
- [Set up Claude Code in a monorepo](https://code.claude.com/docs/en/large-codebases)
