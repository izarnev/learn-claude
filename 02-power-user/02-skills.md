# 02 · Skills

**What you'll learn:** what a Skill is, how progressive disclosure makes them nearly free, and how to write one that actually triggers.

*Available on Free, Pro, Max, Team and Enterprise plans. Requires [code execution](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude) to be enabled.*

---

## What a Skill is

A Skill is a folder containing a `SKILL.md` file — instructions Claude loads **on demand** when they're relevant — plus optional bundled files and scripts.

The core insight: a Skill is what you'd write to onboard a new team member to one specific task. Not facts about your company (that's a Project), but *how we do this thing here*.

```
release-notes/
├── SKILL.md          # main instructions
├── TEMPLATE.md       # the format we use
├── examples/
│   └── v2.4.0.md     # a good past example
└── scripts/
    └── fetch_prs.py  # utility Claude can run
```

---

## Progressive disclosure — why Skills are nearly free

This is the mechanism that makes Skills work at scale.

| Level | When it loads | Cost | What |
|---|---|---|---|
| **1 · Metadata** | Always, at startup | ~100 tokens per skill | `name` and `description` from the frontmatter |
| **2 · Instructions** | When the skill triggers | Under 5k tokens | The body of SKILL.md |
| **3 · Resources** | Only when referenced | Zero until accessed | Bundled files; scripts run via bash, only output enters context |

The consequence: **you can install dozens of Skills without a context penalty.** Until one triggers, it costs about a hundred tokens.

And bundled content is effectively unlimited. A Skill can ship a 500-page API reference, and if the task doesn't need it, it costs nothing.

Scripts are especially efficient: when Claude runs `validate.py`, the script's *code* never enters context — only its output. That makes scripts far cheaper and more deterministic than asking Claude to generate equivalent code on the fly.

---

## Anatomy of a SKILL.md

```markdown
---
name: release-notes
description: Write release notes for the Ledger service in our house format. Use when the user asks for release notes, a changelog, or a version announcement.
---

# Release notes

## Process

1. Ask which version and which date range of merged PRs to cover.
2. Group changes into: Breaking, Added, Fixed, Internal. Omit empty groups.
3. Each entry is one sentence in past tense, starting with a verb.
4. Breaking changes always come first and always include a migration note.
5. Link every entry to its PR.

## Format

Follow TEMPLATE.md exactly. See examples/v2.4.0.md for a good result.

## Rules

- Never invent a PR number. If you don't have it, write `(PR: TBC)`.
- Internal-only changes get one line, not a paragraph.
- No marketing language. Engineers read these.
```

### Field requirements

**`name`**
- Max 64 characters
- Lowercase letters, numbers, and hyphens only
- No XML tags
- Cannot contain the reserved words "anthropic" or "claude"

**`description`**
- Required, non-empty, max 1024 characters
- No XML tags

---

## Writing a description that triggers

**This is the single most important part of the whole skill**, because it's the only thing Claude sees until the skill fires. Claude matches your request against descriptions to decide what's relevant.

A good description says **both what the skill does and when to use it.**

| Bad | Why | Good |
|---|---|---|
| `Release notes helper` | No trigger conditions | `Write release notes for the Ledger service in our house format. Use when the user asks for release notes, a changelog, or a version announcement.` |
| `Handles documents` | Too broad — will over-trigger | `Convert meeting transcripts into structured decision logs. Use when given a transcript, meeting notes, or recording summary and asked for decisions or action items.` |
| `Use this for data` | Meaningless | `Clean and validate CSV exports from Salesforce, fixing date formats and deduplicating on email. Use when the user mentions a Salesforce export or a messy CSV.` |

**Include the words users actually say.** If your team says "changelog", "release notes", and "what shipped", put all three in the description.

**Be specific enough not to over-trigger.** A description like "handles documents" will fire on everything and crowd out better matches.

---

## The body: write it like a runbook

The description gets it loaded. The body determines whether the result is good.

**Do:**
- Number the steps
- Say what to do when information is missing (`ask` vs `write TBC` vs `infer`)
- State the format precisely, or point at a template file
- Include a good example
- List the specific mistakes you keep having to correct

**Don't:**
- Explain what the concept is (Claude knows what a changelog is)
- Write vague principles ("be thorough")
- Exceed ~5k tokens — push detail into bundled files and reference them

---

## Where Skills live, per surface

**Skills do not sync across surfaces.** Upload separately to each.

| Surface | How | Sharing |
|---|---|---|
| **claude.ai** | Customize → Skills, upload as `.zip` | Individual. Team/Enterprise **Owners can provision skills org-wide** — they appear in every member's list, enabled or disabled by default |
| **Cowork** | Same, plus via Plugins | Individual, or via plugin |
| **Claude Code** | `~/.claude/skills/` (personal) or `.claude/skills/` (project) | Project skills go in git; also shareable via plugins |
| **Claude API** | Upload via the `/v1/skills` endpoints | Workspace-wide |
| **Agent SDK / Managed Agents** | Configured in code | Per deployment |

### The four kinds of skill

| Kind | What |
|---|---|
| **Anthropic skills** | Built and maintained by Anthropic — PowerPoint, Excel, Word, PDF. Available to everyone, invoked automatically. Not available in Claude Code. |
| **Custom skills** | Yours: brand guidelines, email templates, team conventions, data workflows |
| **Organization-provisioned** | Team/Enterprise Owners push skills to everyone. See [Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization) |
| **Partner skills** | Professionally built by Notion, Figma, Atlassian and others, designed to pair with their MCP connectors |

Browse everything via **Customize → Skills → + → Browse skills**.

Skills follow the [Agent Skills open standard](https://agentskills.io), so the same format works across platforms that adopt it — you're not locked to Claude. A reference Python SDK exists for implementers.

---

## Runtime differences worth knowing

| Surface | Network | Package install |
|---|---|---|
| **claude.ai** | Varies by user/admin settings — full, partial, or none | — |
| **Claude API** | **None.** No external calls. | None. Pre-installed packages only. |
| **Claude Code** | Full — same as any program on your machine | Allowed, but install locally, not globally |

If you write a Skill that fetches from a URL, it will work in Claude Code and fail on the API. Plan for the surface you're targeting.

---

## Security

Treat installing a Skill like installing software.

A Skill gives Claude new instructions and executable code. A malicious one can direct Claude to invoke tools in ways that don't match its stated purpose — data exfiltration, unauthorised access, destructive operations.

**Rules:**

- Use Skills you wrote, or that come from Anthropic
- If you must use a third-party Skill, **audit every file**: SKILL.md, scripts, images, resources. Look for network calls, unusual file access, anything that doesn't match the stated purpose.
- Skills that fetch from external URLs are the highest risk — fetched content can carry instructions, and even a trustworthy skill can be compromised if its dependency changes
- Be especially careful in production systems with access to sensitive data

---

## Skill vs. Project vs. instruction

| | Loads | Best for |
|---|---|---|
| **Custom instructions** | Every conversation | Global preferences |
| **Project** | Every conversation in the project | Domain context and reference material |
| **Skill** | On demand, when relevant | A repeatable *procedure* |

**The trigger for creating a Skill:** you've pasted the same multi-step instructions into chat three times.

---

## Try it

**Exercise 1 — Convert a prompt into a Skill.**
Take the best template from your prompt library ([01-foundations/08](../01-foundations/08-structured-prompting.md)). Write it as a SKILL.md with proper frontmatter. Zip the folder. Upload it. Use it.

**Exercise 2 — Description A/B.**
Write two descriptions for the same skill: one vague, one specific with trigger words. Install each in turn and try five naturally-phrased requests. Count how often it fired.

**Exercise 3 — Progressive disclosure.**
Build a skill with a bundled reference file. Ask a question that needs the file and one that doesn't. Confirm Claude only reads it when relevant.

**Exercise 4 — Script over prose.**
Write a skill that includes a small Python script (e.g. validating a CSV). Compare against a version where the skill *describes* the validation in prose. The script version is more reliable and cheaper.

**Exercise 5 — Audit.**
Find a third-party skill in the [skills directory](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory). Read every file before installing. Practise the habit now, while nothing is at stake.

---

## Checkpoint

- You can state the three levels of progressive disclosure and roughly what each costs
- You can write a description that says both what *and* when
- You know why a skill that works in Claude Code might fail on the API

---

## Going deeper

- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Teach Claude your way of working using Skills](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)
- [Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization)
- [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Agent Skills open standard](https://agentskills.io)
