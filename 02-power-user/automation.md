---
title: "Automation: scheduled tasks and routines"
order: 6
---

# Automation: scheduled tasks and routines

**What you'll learn:** how to make Claude do work on a schedule, and how to tell the difference between the several scheduling mechanisms.

---

## Four ways to run Claude on a schedule

| Mechanism | Where it runs | Needs your machine? | Best for |
|---|---|---|---|
| **Cowork scheduled tasks** | Anthropic's cloud | No | Recurring knowledge work: digests, reports, monitoring |
| **Desktop scheduled tasks** | Your machine | Yes | Work that needs local files or local tools |
| **Routines** (Claude Code) | Anthropic-managed infra | No | Recurring dev work; also triggerable by API call or GitHub event |
| **`/loop`** (Claude Code) | Your session | Yes | Repeating a prompt *within* a session; polling |

If you just want "every weekday morning, do X", the first one is almost always the answer.

---

## Cowork scheduled tasks

Type `/schedule` in any Cowork task, or click **Scheduled** in the left sidebar to view, create and manage them.

These run in the cloud. Your computer can be off. The desktop app doesn't need to be open — *unless* the task needs local files or your browser, in which case it does.

### What actually works well on a schedule

The pattern that works: **a task whose inputs change but whose procedure doesn't.**

| Schedule | Task |
|---|---|
| Weekday 7am | Summarise overnight email, flag anything needing a reply today |
| Monday 9am | Pull last week's metrics, compare to the four-week trend, write a short update |
| Daily 6pm | Check the competitor pages I care about, tell me only if something changed |
| Friday 4pm | Read this week's meeting notes folder, extract every commitment and its owner |
| Monthly | Reconcile the receipts folder into an expense report |

### What doesn't work well

- Anything needing a judgment call you'd want to make yourself
- Anything with irreversible consequences (sending, paying, deleting) unless you're very confident
- Anything where "no news" and "the task failed" look the same to you

### Writing a scheduled task prompt

Different from an interactive prompt in three ways:

1. **You won't be there to clarify.** Every ambiguity must be resolved in advance, including "what if there's nothing to report".
2. **State the no-op behaviour explicitly.** "If nothing has changed, say exactly: *No changes.* Don't pad."
3. **Say where output goes.** A file, a location, a format.

Example:

```
Every weekday at 07:00.

Check my calendar for today and tomorrow, and my unread email from the last
16 hours.

Produce a brief with three sections:
1. Today — meetings with times, and for each, anything in my email that relates
   to it.
2. Needs a reply today — emails where someone is waiting on me. Include who and
   what they asked. Skip newsletters, notifications, and anything automated.
3. Tomorrow — just the meeting list.

If a section is empty, write "Nothing." and move on. Do not pad. Do not
editorialise. Under 300 words total.

Do not send, archive, or reply to anything.
```

That last line is the important one. **Scheduled tasks should be read-only unless you have a very good reason.**

---

## Routines (Claude Code)

Routines run on Anthropic-managed cloud infrastructure and keep running with your computer off. Beyond a schedule, they can also trigger:

- On an API call
- On a GitHub event

Create them from the web, the Desktop app, or by running `/schedule` in the CLI.

Good routine candidates: morning PR reviews, overnight CI failure analysis, weekly dependency audits, syncing docs after PRs merge, triaging new issues.

See [Routines](https://code.claude.com/docs/en/routines).

---

## Desktop scheduled tasks

Run on your machine, with direct access to local files and tools. Use when the work genuinely needs your computer — local repositories, local databases, applications only installed locally.

See [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks).

---

## `/loop`

Repeats a prompt within a running Claude Code session. Not scheduling in the "wake up tomorrow" sense — it's polling. Use for watching a build, waiting for a deploy, or iterating until a condition holds.

Related: `/goal` sets a completion condition and Claude keeps working across turns until it's met.

See [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) and [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal).

---

## Designing automation that doesn't rot

Three failure modes to design against.

### 1. Silent failure

A task that errors quietly is worse than no task, because you stop checking manually. Build in a heartbeat: have the task always produce output, even if that output is "nothing to report". Then silence means failure.

### 2. Drift

The task was written against a world that has since changed — a folder moved, a report format changed, a system was replaced. Review scheduled tasks quarterly. Delete the ones you no longer read.

### 3. Alert fatigue

If a daily digest is 80% noise, you'll stop reading it within a fortnight. Be aggressive about what gets filtered out. A three-line brief you read every day beats a two-page one you skim.

**The test:** after two weeks, do you still open it? If not, either fix it or delete it.

---

## Cost

Scheduled tasks consume usage exactly like interactive ones — and they run whether or not you needed them that day. A daily Opus task on a large context is a real ongoing cost against your limits.

Mitigations: run less often than feels natural (weekly beats daily for most things), scope the input tightly, and prefer a cheaper model where the task is mechanical.

---

## Try it

**Exercise 1 — Morning brief.**
Set up the morning brief above, adapted to your systems. Run it for a week. On day 7, rewrite it based on which sections you actually read.

**Exercise 2 — The no-op test.**
Deliberately create a day where your scheduled task should have nothing to report. Confirm it says so rather than inventing content. If it padded, your prompt needs the explicit no-op instruction.

**Exercise 3 — Weekly digest.**
Pick something you currently check manually every week. Automate it. Compare the time cost of setup against a month of manual checks.

**Exercise 4 — Read-only audit.**
List every scheduled task you have. For each, confirm it cannot send, delete, or pay. Where it can, confirm you meant that.

**Exercise 5 — Two-week review.**
In two weeks, come back to whatever you set up. Delete anything you're not reading. This is the exercise most people skip and most need.

---

## Checkpoint

- You know which of the four scheduling mechanisms fits a given task
- Your scheduled prompts state the no-op behaviour explicitly
- Everything you've scheduled is read-only, or deliberately isn't

---

## Going deeper

- [Schedule recurring tasks in Cowork](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-cowork)
- [Routines](https://code.claude.com/docs/en/routines)
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)
- [Scheduled deployments (Managed Agents)](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments)
