---
title: "Cowork"
order: 4
---

# Cowork

> **You are here** · Paths A, B, C · **Requires Pro or above** · Read 15 min · Exercises 50 min · Assumes [Skills](02-skills.md) and [Connectors](03-connectors-and-mcp.md). This is the flagship non-developer module.

**What you'll learn:** how to hand Claude a multi-step job and get finished work back — including the permission modes that decide how much you're in the loop.

---

## If you only read one thing

Cowork is where you stop having a conversation and start handing over a job. You point Claude at a folder, describe the outcome you want, and it works through the whole thing — reading files, running calculations, building the deliverable — while you do something else.

The two things that determine whether it goes well:

**Write a brief, not a prompt.** Say what the finished thing should be, where the inputs are, where the output goes, what Claude must not touch, and when it should stop and ask you. Every clause you add prevents a specific way it could go wrong.

**Pick the right permission mode.** *Manual* asks you before each action — use it for anything involving money, messages sent as you, or files you can't replace. *Auto* keeps working but safety-checks every action before taking it, and is the right default for most work. *Skip* does neither, and should be rare. Claude always asks before permanently deleting anything, in every mode.

One expectation to set: Cowork uses far more of your plan allowance than chatting does. Use it for jobs, not questions.

---

## What Cowork is

Cowork brings Claude Code's agentic architecture to knowledge work, with no terminal. Instead of one prompt at a time, Claude takes on complex multi-step tasks and executes them: reads your local files, runs code, coordinates subagents, and delivers finished deliverables.

You describe an outcome, step away, and come back to the work.

### Where it runs

Sessions run **in the cloud** (in beta) on Anthropic's servers in an isolated environment. Your sessions and files live with your Claude account and follow you across desktop, web and mobile.

When a task needs something on *your computer* — a local file, your browser — Claude reaches it through the Claude Desktop app on that machine. So:

- **Sessions keep running** when you close your laptop or it sleeps
- **But** if the task uses local files, your browser, or your computer, **keep the desktop app open**

Available on Claude Desktop (macOS, Windows, Linux beta), web at claude.ai, and the mobile apps. Chat and Cowork share one home — in the message box, select "Cowork" instead of "Chat".

---

## What it's actually good at

| Category | Examples |
|---|---|
| **File and document management** | Organise a Downloads folder by type and date; turn a folder of receipts into a formatted expense report; batch-rename to a consistent pattern |
| **Research and analysis** | Synthesise web sources, articles and your own notes into a report; extract themes and action items from transcripts; surface patterns across your notes |
| **Document creation** | Excel with working VLOOKUPs, conditional formatting and multiple tabs; decks from rough notes; reports from voice memos |
| **Data work** | Outlier detection, cross-tabs, time series; charts from your data; cleaning and transforming datasets |

The common thread: **multi-step work over files, where you'd otherwise spend an hour clicking.**

---

## Permission modes — the most important setting

Three modes control when Claude asks before acting. Change them any time from the mode selector in the chat box.

| Mode | Behaviour |
|---|---|
| **Manually approve** (Manual) | Claude pauses and asks for approval on actions. You choose Allow or Deny each time. |
| **Automatically approve** (Auto)\* | Claude keeps working, but reviews each action for safety — checking for data exfiltration and prompt injection — and blocks anything it judges unsafe. When blocked, it finds a safer route or asks you. Repeated blocks send it back to asking each step. |
| **Skip all approvals** (Skip) | No pausing, no automatic checking. |

\* Auto is currently Pro and Max only.

These interact with each connector's own permission setting (Always allow / Needs approval / Blocked). A connector set to **Blocked** is denied in every mode.

### How to choose

**Auto mode** is the default recommendation for most work. It gives you speed with an actual safety review of every action — which "Skip" does not. Anthropic tested it with external security researchers attempting to sneak dangerous actions past it.

Two caveats:

- **Auto consumes more of your usage limit**, because of the extra checking.
- **Auto won't approve certain sensitive actions regardless**: granting access to additional folders, deleting files, creating scheduled tasks, and others.

**Manual mode** for anything with real consequences — money, messages sent as you, important files. No mode replaces your judgment.

**Skip mode** only when you completely trust every action, connector, file and app involved.

### Deletion protection

Claude always requires explicit permission before permanently deleting any file, in every mode. You'll see a prompt and must select "Allow".

---

## Instructions: global and folder

### Global instructions

Standing directions for every Cowork session — tone, output format, your role. Set them at **Settings → Cowork → Global instructions**.

Good global instructions:

```
I'm a finance manager at a 200-person SaaS company. I'm not technical.

When you produce spreadsheets, use real formulas, not pasted values. Always
include a summary tab.

When you produce documents, plain language, no jargon, and put the conclusion
first.

Before starting anything that touches more than 20 files, tell me the plan and
wait for me to confirm.
```

That last line is worth stealing. It's a self-imposed checkpoint on the tasks most likely to go wrong.

### Folder instructions

Project-specific context attached to a local folder you've selected on desktop. Claude can also update these itself during a session — so a folder accumulates knowledge about how you like it handled.

---

## Projects in Cowork

Group related tasks into workspaces with their own files, links, instructions, and **memory**.

Note the current limitation: what Claude remembers about you in chat does **not** carry into Cowork, and within Cowork, memory is supported **in projects only**. If you want continuity across Cowork sessions, use a project.

---

## Plugins

Plugins bundle skills, connectors and subagents into one installable package, customised for your role or team. Install from the plugin directory. Some plugins include local MCP servers and work through the desktop app only.

Covered in [Plugins](07-plugins.md).

---

## Scheduled tasks

Type `/schedule` in any Cowork task, or use "Scheduled" in the left sidebar. Scheduled tasks run in the cloud — no device online, no desktop app open.

Covered in [Automation: scheduled tasks and routines](06-automation.md).

---

## Browser and computer use

Claude can open Chrome and work on websites — clicking, typing, navigating, filling forms. See [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome).

Claude can also use your computer more broadly in Cowork — screenshots and control of native apps. See [Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork).

Both require the desktop app and explicit permission grants.

---

## Prompting Cowork well

A Cowork task is not a chat prompt. It's a brief. Include:

1. **The outcome**, not the steps — "produce a formatted expense report" not "open each receipt"
2. **Where the inputs are** — the folder, the connector, the URL
3. **Where the output should go** — a folder, a file name, a format
4. **Constraints** — what not to touch, what to ask about
5. **Definition of done**

Example:

> In `~/Documents/receipts-2026-q2`, there are ~80 receipt images and PDFs.
>
> Produce `expense-report-q2.xlsx` in the same folder with columns: Date, Vendor, Category, Amount (EUR), Currency (original), Receipt filename. Convert non-EUR amounts using the rate on the receipt date; if there's no rate available, leave it blank and flag it.
>
> Add a summary tab with totals by category and a count of flagged rows.
>
> Do not move, rename, or delete any of the original files. If more than five receipts are unreadable, stop and tell me before continuing.

Every clause in that brief prevents a specific failure.

### Editing drafts in place

When Claude drafts a Markdown document, highlight the text you want changed, click "Edit with Claude", and type your request. It edits exactly where you marked, without you describing the section.

---

## Limitations to know about

- **Memory** from chat doesn't carry into Cowork; within Cowork it's projects-only
- **No session sharing.** (Team/Enterprise can share live artifacts within the org.)
- **Live artifacts and plugins with local MCP servers are desktop-only**
- **Usage.** Cowork consumes considerably more of your allocation than chat. Batch related work into single sessions and use plain chat for simple things.

---

## Try it

**Exercise 1 — File organisation.**
Point Cowork at a genuinely messy folder. Ask it to organise by type and date. Run it in Manual mode so you see every action. Notice how many discrete steps a "simple" task actually is.

**Exercise 2 — The brief.**
Write a Cowork task twice: once as a one-liner, once with all five brief components. Run both. The difference is the whole lesson of this module.

<details>
<summary>Worked example — with a checklist you can reuse</summary>

**The one-liner:**

> Sort out my receipts folder and make me an expense report.

This will produce *something*. It will also guess at the currency handling, invent a column layout, possibly rename your files, and not tell you which receipts it couldn't read.

**The brief.** Same job, with the five components labelled so you can see the pattern:

> **[outcome]** Produce a formatted expense report as a single spreadsheet.
>
> **[inputs]** The ~80 receipt images and PDFs in `~/Documents/receipts-2026-q2`.
>
> **[output]** `expense-report-q2.xlsx` in that same folder. Columns: Date, Vendor, Category, Amount (EUR), Currency (original), Receipt filename. Add a summary tab with totals by category.
>
> **[constraints]** Do not move, rename or delete any original file. Convert non-EUR amounts using the rate on the receipt date; if no rate is available, leave the cell blank and flag the row.
>
> **[definition of done]** Every receipt appears as a row, flagged rows are visibly marked, and the summary tab totals match the detail tab.

**Your reusable checklist.** Before starting any Cowork task, answer these five in one line each:

1. What is the finished thing?
2. Where is the raw material?
3. Where does the result go, and in what format?
4. What must Claude not do, and what should it ask about?
5. How will I know it worked?

**What to notice.** Component 4 is the one people skip and the one that saves them. "Do not rename the originals" and "flag rather than guess" are each preventing a specific, likely failure. Component 5 is what lets you check the output in thirty seconds instead of re-reading eighty receipts.

</details>

**Exercise 3 — Mode comparison.**
Run a moderate task in Manual, then the same class of task in Auto. Note the speed difference and how much you actually wanted to be asked.

**Exercise 4 — Real deliverable.**
Give Cowork a folder of raw material (notes, transcripts, data) and ask for a polished output — an .xlsx with formulas or a .pptx. Open the result in the native app and check it's real, not a flat dump.

**Exercise 5 — Global instructions.**
Write your global instructions including a self-imposed checkpoint ("tell me the plan before touching more than N files"). Use Cowork for a week. Revise.

---

## Checkpoint

- You can explain what Auto mode does that Skip mode doesn't
- You know why the desktop app needs to be open for some tasks and not others
- Your Cowork briefs specify output location and definition of done

---

## Going deeper

- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- [Use Claude Cowork safely](https://support.claude.com/en/articles/13364135-use-claude-cowork-safely)
- [Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- [Claude Cowork architecture overview](https://support.claude.com/en/articles/14479288-claude-cowork-architecture-overview)
- [Use Claude Cowork on Team and Enterprise plans](https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans)
- [Organize your tasks with projects in Cowork](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-cowork)
