---
title: "Skills in the API"
order: 10
---

# Skills in the API

**What you'll learn:** using Agent Skills programmatically — including the pre-built document skills that produce real Office files.

---

## How Skills work on the API

Skills run in the **code execution container**. That's the prerequisite: you must enable the code execution tool, and Skills run inside its container.

Two headers matter:

| Header | For |
|---|---|
| `skills-2025-10-02` | Enables Skills |
| `files-api-2025-04-14` | Needed to upload inputs or download files a Skill produces |

---

## Pre-built document Skills

Four ship ready to use:

| `skill_id` | Produces |
|---|---|
| `pptx` | PowerPoint presentations |
| `xlsx` | Excel spreadsheets with formulas and charts |
| `docx` | Word documents |
| `pdf` | Formatted PDF reports |

```python
response = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=8192,
    betas=["skills-2025-10-02", "files-api-2025-04-14", "code-execution-2025-05-22"],
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}],
    container={"skills": [{"type": "anthropic", "skill_id": "xlsx"}]},
    messages=[{
        "role": "user",
        "content": "Build a quarterly budget spreadsheet with these line items: ... "
                   "Include a summary sheet with totals by category and a chart. "
                   "Use real formulas, not hardcoded values.",
    }],
)
```

Retrieve the produced file via the Files API.

This is the fastest path from "I have data" to "I have a real .xlsx a finance team will accept."

---

## Custom Skills

Upload through the `/v1/skills` endpoints, then reference by `skill_id`:

```python
container={"skills": [{"type": "custom", "skill_id": "acme-report-format"}]}
```

**Custom Skills on the API are workspace-wide** — every workspace member can use them. (Contrast: claude.ai skills are per-user with no org-wide distribution.)

---

## Runtime constraints on the API

This is where people get caught out:

| Constraint | Detail |
|---|---|
| **No network access** | Skills can't make external API calls or reach the internet |
| **No runtime package installation** | Pre-installed packages only |
| **Pre-configured dependencies** | Check the [code execution tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) for what's available |

A Skill that fetches from a URL works in Claude Code (full network access) and **fails on the API**. Design for the surface you're targeting.

---

## Skills don't sync across surfaces

Worth repeating because it catches everyone:

- A Skill uploaded to claude.ai is **not** available on the API
- A Skill uploaded via the API is **not** available on claude.ai
- Claude Code Skills are filesystem-based and separate from both

Upload separately per surface.

---

## Writing a Skill for programmatic use

The same authoring rules from [Skills](../02-power-user/skills.md), plus:

**Be more explicit about output.** No human is there to say "actually, make it shorter." State the exact format, file name, and location.

**Handle missing data deterministically.** Say what to do: fail, use a default, or flag. Don't leave it to judgment.

**Prefer scripts over prose.** Bundled scripts run deterministically and their code never enters context. On the API, where you can't iterate interactively, this reliability matters more.

**Assume no network.** Bundle any reference data the Skill needs.

---

## Skills vs. tools vs. prompts

| | Use for |
|---|---|
| **Prompt** | One-off instructions for this request |
| **Skill** | A repeatable procedure, loaded on demand |
| **Tool** | An action against an external system |

A Skill can *instruct* Claude how to use your tools well. A tool can't carry a procedure. They compose: a "generate the monthly report" Skill might use your `query_database` tool and the `xlsx` skill together.

---

## Security

Same rules, higher stakes on the API because it's often production:

- Use Skills you wrote or that come from Anthropic
- Audit every file in a third-party Skill before uploading
- Custom Skills are workspace-wide — one person's upload affects everyone
- Skills are **not covered by zero data retention** arrangements; definitions and execution data follow standard retention

For org-scale governance and vetting, see [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise).

---

## Try it

**Exercise 1 — Real spreadsheet.**
Use the `xlsx` skill to generate a spreadsheet from data you supply. Download it. Open it in Excel. Verify the formulas are live.

**Exercise 2 — Report pipeline.**
Chain it: query a database (client tool) → analyse (code execution) → produce a formatted `.docx` (docx skill) → return via the Files API.

**Exercise 3 — Custom skill.**
Take a Skill you wrote for Claude Code. Adapt it for the API's constraints (no network, no package installs). Upload it. Note what you had to change.

**Exercise 4 — Constraint discovery.**
Deliberately write a Skill that needs network access. Watch it fail on the API. Now you'll never forget.

**Exercise 5 — Determinism.**
Write the same logic as prose in a Skill body and as a bundled script. Run each twenty times. Count variations.

---

## Checkpoint

- You've produced a real Office file via the API
- You know the three API runtime constraints on Skills
- You know Skills don't sync between surfaces

---

## Going deeper

- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)
- [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Agent Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction)
- [anthropics/skills on GitHub](https://github.com/anthropics/skills)
