# 01 · Projects

**What you'll learn:** how to use Projects to stop re-explaining yourself, and how project knowledge actually gets retrieved.

*Requires a paid plan.*

---

## What a Project is

A Project is a container that holds:

- **Custom instructions** — standing directions for every conversation in the project
- **A knowledge base** — files and text Claude can draw on
- **Conversations** — all chats started inside the project

The point: everything Claude needs to know about a recurring context is set up once, not re-pasted every time.

---

## When to make one

Make a Project when you find yourself **re-explaining the same background**.

Good candidates:

| Project | Instructions | Knowledge |
|---|---|---|
| A product you work on | Your role, the audience, the tone | Specs, roadmap, past decisions, glossary |
| Client work | The client's context and constraints | Brand guide, past deliverables, contracts |
| A codebase | Architecture, conventions, tech stack | Key source files, ADRs, API docs |
| Writing in your voice | Voice rules, structural preferences | 10–20 things you've written |
| A research area | The question, what's already ruled out | Papers, notes, data |

Bad candidates: one-off tasks, anything where the "context" is a single file you can just attach.

---

## Custom instructions: what to put in them

This is where most of the value is, and most people underuse it.

Include:

1. **Who you are and what you're doing** — role, company, what this project is for
2. **Who the output is for** — this changes everything
3. **Standing format rules** — length, structure, markdown or prose
4. **Vocabulary** — terms of art, product names, things never to call something
5. **Standing constraints** — "never suggest solutions requiring a database migration", "all code must be Python 3.11 compatible"
6. **How to handle ambiguity** — "ask before assuming" or "make a reasonable assumption and flag it"

Example:

```
This project is for the Payments team at Acme, a B2B invoicing SaaS.

I'm the tech lead. Output is usually read by engineers or by our PM, Sarah,
who is non-technical.

Conventions:
- Our service is called "Ledger". Never call it "the payments service".
- We're on Python 3.11, FastAPI, Postgres 15. Don't suggest anything else
  without flagging it as a stack change.
- All money is stored in minor units as integers. Never suggest floats.

Style: direct, no preamble. When you give an opinion, give the trade-off too.
If a question is ambiguous in a way that changes the answer, ask first.
```

Notice everything is *verifiable*. "Be helpful" isn't an instruction; "never suggest floats for money" is.

---

## The knowledge base and RAG

Project knowledge doesn't all sit in the context window. Above a certain size, Claude uses **retrieval-augmented generation (RAG)**: your files are indexed, and for each message Claude retrieves the relevant chunks and puts *those* in context.

This has consequences you should design around:

**Retrieval is based on relevance to your message.** If your question doesn't lexically or semantically resemble the relevant document, it may not get retrieved. Naming the document helps: *"According to the Q3 architecture review, ..."*

**Structure your documents for retrieval.** A well-headed document with descriptive section titles retrieves better than a wall of text. Split genuinely distinct topics into separate files with clear names.

**Small projects may not use RAG at all.** Below the threshold, everything is just loaded. This is why a small project sometimes feels more accurate than a large one.

**Stale knowledge is worse than no knowledge.** Claude has no way to know your uploaded spec is six months out of date. Prune actively.

### What to put in

Do include: reference docs, style guides, specs, glossaries, past deliverables, decisions and their rationale, examples of good output.

Don't include: enormous logs, entire codebases (use Claude Code), anything you wouldn't want retrieved into an answer, duplicates and near-duplicates (they compete with each other in retrieval).

---

## Working in a Project

- **Start conversations inside it**, not outside. Instructions and knowledge only apply within.
- **You can still attach files** to individual conversations for one-off material.
- **Conversations don't share context with each other.** Two chats in the same project are independent; they share instructions and knowledge, not history.
- **Team plans** allow shared projects, so instructions and knowledge become a team asset.

---

## Projects in Cowork

Cowork has its own project concept: workspaces that group related tasks with their own files, links, instructions, and **memory**. Notably, memory in Cowork is currently supported *in projects only*. See [module 04](04-cowork.md).

---

## Project vs. Skill vs. custom instructions

A frequent confusion. The distinction:

| | Scope | Contains | Use for |
|---|---|---|---|
| **Custom instructions** (Settings) | Every conversation, everywhere | Your global preferences | "Be concise", "use TypeScript" |
| **Project instructions** | Every conversation in that project | Context for a domain | "This is the Ledger service, here's the stack" |
| **Skill** | Loaded on demand, anywhere | A *procedure* | "How to write our release notes" |

Rule of thumb: **facts and context → project. Procedures → skill. Preferences → settings.**

---

## Try it

**Exercise 1 — Build a real project.**
Pick the thing you use Claude for most. Create a project. Write instructions covering all six categories above. Upload 3–5 genuinely useful reference documents. Use it for a week.

**Exercise 2 — Prove RAG is happening.**
Upload a document with a distinctive, obscure fact buried in the middle. Ask a question that clearly relates to it. Then ask a question that relates to it only obliquely. Note whether Claude retrieved it both times.

**Exercise 3 — Instruction ablation.**
Ask the same question inside your project and in a fresh chat outside it. The difference is the value of your instructions. If there's no difference, your instructions are too vague — rewrite them to be verifiable and try again.

**Exercise 4 — Prune.**
Take an existing project (or your new one after a week) and delete a third of the knowledge base — the least-used, most-redundant, most-stale third. Note whether anything got worse.

**Exercise 5 — Voice project.**
Create a project whose knowledge base is 10–20 things you've written and whose instructions describe your voice. Use it for all your drafting for a week. This is the highest-ROI project most people can build.

---

## Checkpoint

- You can explain why a large knowledge base sometimes performs worse than a small one
- Your project instructions contain nothing you couldn't check compliance with
- You know when something belongs in a project vs. a skill vs. global settings

---

## Going deeper

- [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- [Retrieval augmented generation (RAG) for projects](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)
- [Organize your tasks with projects in Cowork](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-cowork)
