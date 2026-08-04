# 05 · Claude inside your apps

**What you'll learn:** every place Claude shows up outside claude.ai, and which one to reach for.

---

## The Office agents

Claude embedded in the Microsoft applications, working on the live document rather than a copy.

| Agent | What it does |
|---|---|
| **Claude for Excel** | Reads and writes the actual workbook — formulas, multiple sheets, pivots, charts. Understands structure, not just cell values. |
| **Claude for Word** | Drafts, edits and restructures documents in place |
| **Claude for PowerPoint** | Builds and edits decks |
| **Claude for Outlook** | Drafts and triages mail |
| **Microsoft 365** | Works across M365 apps, and with [third-party platforms](https://support.claude.com/en/articles/13945233-use-claude-for-microsoft-365-with-third-party-platforms) |

**Why use these over uploading a file to chat:** when you upload a spreadsheet to chat, Claude gets a text representation and loses formulas, formatting, and cross-sheet relationships. The Excel agent works on the real object.

**Dictation** is supported in the Office agents — see [Use dictation in Office agents](https://support.claude.com/en/articles/14479591-use-dictation-in-office-agents).

### When to use which

| Situation | Use |
|---|---|
| The data already lives in a workbook you'll keep working in | Claude for Excel |
| You need a *new* spreadsheet built from scratch | Chat or Cowork file creation |
| Restructuring a long Word document | Claude for Word |
| Building a deck from raw notes | Cowork, then refine in Claude for PowerPoint |

---

## Claude in Chrome

A browser extension that lets Claude navigate, click, type, fill forms, extract data, and debug web applications.

**Genuinely useful for:**

- Web apps with no API — Claude can drive the UI
- Repetitive form filling
- Extracting structured data from pages that resist copy-paste
- Debugging your own web app: Claude can read the console, network requests, and DOM
- Client-side-rendered pages that a plain fetch can't read

**Safety notes that matter:**

- **Links in emails and messages are suspicious by default.** Verify the real destination URL before letting Claude follow one.
- Prompt injection is a live risk — a webpage can contain instructions aimed at Claude.
- Team/Enterprise admins can control the extension via Organization settings → Claude in Chrome.

Cowork can also drive Chrome for tasks that touch websites.

---

## Claude in Slack

Mention `@Claude` in a channel or DM. It reads the thread context and responds there.

The interesting version is the Claude Code integration: report a bug in Slack, get a pull request back. Setup is via `/install-slack-app`. See [Claude Code in Slack](https://code.claude.com/docs/en/slack).

Good uses: triaging bug reports from non-engineers, answering questions with context from the thread, kicking off coding tasks from wherever the conversation is happening.

---

## Claude in Xcode

Apple-platform development inside Xcode. See [Use Claude in Xcode](https://support.claude.com/en/articles/12293051-use-claude-in-xcode).

---

## Claude Design

A canvas and design toolset where Claude generates and iterates on designs interactively — rather than emitting a static mockup you then have to describe changes to.

You can also set up your design system so output matches your tokens, components, and conventions:

- [Get started with Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- [Set up your design system in Claude Design](https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design)

Related: if you're generating frontends via chat or the API, Anthropic publishes a [frontend design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) and guidance on avoiding generic "AI slop" aesthetics. The short version: specify typography, commit to a cohesive colour theme, use motion at high-impact moments, and give backgrounds depth. Left unguided, models converge on the same handful of safe choices.

---

## Claude Security

Security-focused workflows. See [Use Claude Security](https://support.claude.com/en/articles/14661296-use-claude-security).

For developers, the related tool is the **security-guidance plugin** for Claude Code, which has Claude review its own code changes for vulnerabilities and fix them in the same session — covered in [03-claude-code/10](../03-claude-code/10-plugins-and-marketplaces.md).

---

## Choosing between all of these

The general rule: **use the integration that works on the native object.**

Editing a spreadsheet? Excel agent, not a chat upload. Working in a repo? Claude Code, not pasted files. Doing something on a website repeatedly? Chrome extension, not screenshots. Triaging in Slack? Slack integration, not copy-paste.

The exception is when you need Claude to reason across *several* systems at once — then chat with connectors, or Cowork, is the right container because it can see all of them.

---

## Try it

**Exercise 1 — Excel, native vs upload.**
Take a workbook with real formulas across two sheets. Ask a structural question ("what feeds cell D14 on Summary?") in chat after uploading, then via Claude for Excel. The difference is stark.

**Exercise 2 — Chrome extraction.**
Find a web page with data that resists copy-paste — a paginated table, a dashboard. Have Claude in Chrome extract it into a table.

**Exercise 3 — Chrome debugging.**
Open a web app you're building (or any site) and have Claude read the console and network tab and explain what's happening.

**Exercise 4 — Design system.**
If you have brand guidelines, set them up in Claude Design and generate something. Compare against the same request with no design system configured.

**Exercise 5 — Map your stack.**
List every application you spend more than an hour a week in. For each, note whether Claude has a native integration, and whether you'd use it. This is your adoption roadmap.

---

## Checkpoint

- You can articulate why the Excel agent beats uploading an .xlsx
- You know the two main safety concerns with Claude in Chrome
- You've decided which one integration you'll actually adopt this month

---

## Going deeper

- [Use Claude for Excel](https://support.claude.com/en/articles/12650343-use-claude-for-excel)
- [Use Claude for Word](https://support.claude.com/en/articles/14465370-use-claude-for-word)
- [Use Claude for PowerPoint](https://support.claude.com/en/articles/13521390-use-claude-for-powerpoint)
- [Use Claude for Outlook](https://support.claude.com/en/articles/14855664-use-claude-for-outlook)
- [Work across Microsoft 365 apps](https://support.claude.com/en/articles/13892150-work-across-microsoft-365-apps)
- [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- [Use Claude in Xcode](https://support.claude.com/en/articles/12293051-use-claude-in-xcode)
- [Claude Code in Slack](https://code.claude.com/docs/en/slack)
