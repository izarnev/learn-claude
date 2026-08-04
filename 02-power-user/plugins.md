---
title: "Plugins"
order: 7
---

# Plugins

**What you'll learn:** what a plugin bundles, where to find good ones, and when to build your own.

---

## What a plugin is

A plugin is a single installable package that can contain:

- **Skills** — instructions and workflows
- **Subagents** — specialised workers with their own context
- **Hooks** — automation triggered by lifecycle events (Claude Code)
- **MCP servers** — connections to external systems
- **Commands** — invocable entry points
- **Colour themes** (Claude Code)

The point is distribution. Everything above can be set up individually; a plugin makes "here's our team's whole Claude setup" one install.

Plugins work in **Claude Code** and in **Cowork**.

---

## Installing one

**In Cowork:** find plugins in the plugin directory. Install, and the bundled skills, connectors and subagents become available.

**In Claude Code:** plugins come from **marketplaces**. Add a marketplace, browse, install. `/plugin list` shows what's installed. Plugins can also be loaded from `.zip` archives and URLs.

Note: plugins that include **local MCP servers work through the desktop app only** in Cowork.

---

## Namespacing

Plugin skills are namespaced — `/my-plugin:review` rather than `/review` — so multiple plugins can coexist without clobbering each other. This matters more than it sounds once you have several installed.

---

## What good plugins exist

Anthropic and the community publish plugins for common needs. Two worth knowing:

**security-guidance** — has Claude review its own code changes for vulnerabilities and fix them in the same session. If you write code with Claude and ship it, install this. See [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance).

**Code intelligence plugins** — connect Claude to a language server for your language, giving symbol-level navigation and live type errors instead of grep. Substantially better on large typed codebases. See [Discover plugins](https://code.claude.com/docs/en/discover-plugins#code-intelligence).

Browse everything in the [skills, connectors and plugins directory](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory).

---

## When to build your own

Build a plugin when **a second person or a second repository needs the same setup.**

Before that point, individual skills and MCP configs are simpler. The progression is:

```
Correct Claude in chat
  → the same correction twice → write it into instructions / CLAUDE.md
  → the same procedure three times → make it a Skill
  → a second repo needs it → make it a Plugin
  → a second team needs it → publish to a Marketplace
```

Don't skip steps. A plugin built before you've used the underlying skills for real is a plugin full of guesses.

Building plugins is covered in [Plugins and marketplaces](../03-claude-code/plugins-and-marketplaces.md).

---

## Security

Same rules as Skills, but more so — a plugin can bundle MCP servers and hooks, which is a broader capability surface than instructions alone.

- Install from sources you trust
- Read what's in it before installing: what skills, what MCP servers, what hooks, what network access
- A hook can run arbitrary shell commands. An MCP server can reach external systems. Treat a plugin install with the seriousness you'd treat `npm install` of an unfamiliar package in a repo with production credentials.
- On Team/Enterprise, admins can constrain which MCP servers users may connect to — see [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp).

---

## Try it

**Exercise 1 — Browse.**
Open the plugin directory. Read the descriptions of ten plugins. Note which two are relevant to your actual work.

**Exercise 2 — Install one, deliberately.**
Install a single plugin. Before you do, write down what you expect it to add. After, check `/plugin list` (Claude Code) or the plugin's page and see whether you were right.

**Exercise 3 — Audit.**
For a plugin you're considering, enumerate: skills, subagents, hooks, MCP servers. For each hook, what command does it run? If you can't find out, don't install it.

**Exercise 4 — Plan your own.**
Write down what would go in a plugin for your team. Skills? MCP servers? A hook? You don't have to build it — but knowing the shape tells you what to build first.

---

## Checkpoint

- You can name the five things a plugin can bundle
- You know why plugin skills are namespaced
- You know the progression from chat correction to published marketplace, and where you currently are on it

---

## Going deeper

- [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)
- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Browse skills, connectors, and plugins in one directory](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)
