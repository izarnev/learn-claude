---
title: "05 · Artifacts and file creation"
---

# 05 · Artifacts and file creation

**What you'll learn:** the difference between an artifact and a real file, when each appears, and how to get Claude to produce genuinely useful deliverables.

---

## Two different things

**Artifacts** are substantial pieces of content that render in a panel beside the conversation instead of inline. Code, HTML pages, React components, markdown documents, SVG, Mermaid diagrams, PDFs. They're editable, versioned within the conversation, and publishable.

**File creation** produces real, downloadable files — `.docx`, `.xlsx`, `.pptx`, `.pdf` — by running actual code in a sandbox. This is what powers "make me a spreadsheet" and it requires a paid plan with code execution enabled.

---

## Artifacts

### When one appears

Claude creates an artifact when the content is substantial, self-contained, and something you'd want to use outside the conversation. Roughly: code over a few lines, documents over ~20 lines, anything renderable.

You can force it: *"Put that in an artifact."* Or prevent it: *"Just answer inline."*

### Types that render specially

| Extension | Renders as |
|---|---|
| `.md` | Formatted markdown |
| `.html` | A live web page |
| `.jsx` | A running React component |
| `.svg` | A vector image |
| `.mermaid` | A diagram |
| `.pdf` | A PDF preview |

### Working with them

- **Iterate in place.** "Make the header sticky", "add a dark mode toggle" — Claude edits the artifact rather than regenerating from scratch.
- **Versions are kept.** You can step back through revisions.
- **Copy or download** with the buttons in the artifact panel.
- **Publish and share** — artifacts can be made public via a link. See [Publish and share artifacts](https://support.claude.com/en/articles/9547008-publish-and-share-artifacts).

### What HTML/React artifacts can and can't do

They run in a sandboxed environment. Practical constraints:

- **No browser storage.** `localStorage` and `sessionStorage` are unavailable. Use in-memory state (React `useState`, or plain JS variables).
- **Single file.** Put HTML, CSS and JS together; don't split into separate files.
- **Limited libraries.** React artifacts can import React, Tailwind core utility classes, lucide-react, recharts, d3, three.js, Chart.js, Plotly, lodash, mathjs, Papaparse, SheetJS, Tone, and shadcn/ui. External scripts can come from `cdnjs.cloudflare.com`.
- **No arbitrary network access.**

If you hit these, the answer is usually "have Claude generate the code and run it yourself."

### What artifacts are genuinely great for

- Interactive prototypes and mockups you can click
- Data visualisations from data you paste in
- Small tools: calculators, converters, checklists, timers
- Diagrams (Mermaid for flowcharts and architecture)
- Long-form documents you'll take elsewhere

---

## File creation

Available on Pro, Max, Team and Enterprise with code execution enabled. Claude writes and runs code in a sandbox to produce a real file.

| Ask for | Get |
|---|---|
| "Make a spreadsheet of..." | `.xlsx` with real formulas, formatting, charts |
| "Write this up as a Word doc" | `.docx` with headings, TOC, page numbers |
| "Turn this into a deck" | `.pptx` with actual slides |
| "Give me a PDF report" | `.pdf` |

Under the hood, Anthropic's pre-built **Agent Skills** (`pptx`, `xlsx`, `docx`, `pdf`) do this work. They're active automatically when you create documents — no setup.

### Getting good documents rather than mediocre ones

The default output is competent and generic. Specify:

**For decks:**
> 12 slides. Audience is the exec team — they'll read this without me presenting, so each slide needs to stand alone. One idea per slide, headline states the takeaway rather than the topic. Include speaker notes.

**For spreadsheets:**
> Columns: Date, Category, Amount, Running Total. Running Total should be a real formula, not a hardcoded value. Freeze the header row. Add a summary sheet with a pivot by category.

**For documents:**
> Include a table of contents, numbered headings, and page numbers. Executive summary first, no longer than half a page.

**Universal:** ask for real formulas, real structure, and real formatting rather than accepting a flat dump. Claude will do it if you ask.

### Working iteratively

You can hand a file back for editing:

> Here's the deck. Slide 4 is too dense — split it into two. Make the colour scheme match the attached brand guide.

Claude reads the file, modifies it, and returns a new version.

---

## Visual and interactive content

Claude can generate custom visuals inline in chat and in Cowork — charts, diagrams, dashboards, illustrations — rendered as SVG or interactive HTML. Ask for what you want to *see*, not just what you want computed.

Claude can also generate images through image-generation capabilities where enabled; see [Can Claude produce images?](https://support.claude.com/en/articles/9002504-can-claude-produce-images).

---

## Try it

**Exercise 1 — Interactive prototype.**
Ask Claude to build a single-page HTML mortgage calculator with a live-updating amortisation chart. Then iterate three times: add a dark mode, add extra-payment modelling, make it mobile-friendly. Notice it's editing, not rewriting.

**Exercise 2 — Real spreadsheet.**
Give Claude 20 rows of made-up sales data as text. Ask for an `.xlsx` with a summary sheet, a pivot by region, a chart, and conditional formatting on anything below target. Open it in Excel and check the formulas are live.

**Exercise 3 — Deck, twice.**
Ask for "a presentation about our Q3 results" with no other guidance. Then ask again with audience, slide count, one-idea-per-slide, and speaker notes specified. Compare.

**Exercise 4 — Diagram.**
Describe a system you know in prose. Ask for a Mermaid diagram. Iterate until it's right. This is a much faster way to draw architecture than any diagramming tool.

**Exercise 5 — Round trip.**
Create a Word document. Download it. Re-upload it. Ask for three specific structural edits. Verify they landed.

---

## Checkpoint

- You know the difference between an artifact and a created file, and which needs a paid plan
- You can name three constraints on HTML/React artifacts
- Your document prompts specify structure, not just topic

---

## Going deeper

- [What are artifacts and how do I use them?](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them)
- [Publish and share artifacts](https://support.claude.com/en/articles/9547008-publish-and-share-artifacts)
- [Create and edit files with Claude](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)
- [Visual and interactive content](https://support.claude.com/en/articles/13641943-visual-and-interactive-content)
- [Custom visuals in chat and Cowork](https://support.claude.com/en/articles/13979539-custom-visuals-in-chat-and-cowork)
