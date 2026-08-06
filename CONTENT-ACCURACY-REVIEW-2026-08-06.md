---
title: "Content accuracy review — 6 August 2026"
date: 2026-08-06
---

# Content accuracy review — learn-claude

**Review date: 6 August 2026.**
Verified against platform.claude.com, code.claude.com, and the Anthropic model and migration documentation as published on that date.

Scope: all 63 Markdown files (~13,750 lines), at commit `2e6e3ae`.

> This is a point-in-time snapshot. Anthropic ships model and tool changes frequently, and several findings below exist precisely because the docs moved after this content was written. Re-run the review rather than trusting these results after a model or tool release.

---

## Verdict

The track is in **good factual shape**. Model data, pricing, thinking semantics, and the Claude Code surface are accurate and current — noticeably more so than most third-party Claude material. Every one of the 262 `platform.claude.com` / `code.claude.com` deep links resolves.

The problems cluster in one place: **the API sections have drifted about one tool generation behind the docs.** Two of the findings below will produce a hard `400` for any reader who copies the code as written. Everything else is a correctness or completeness gap rather than a fabrication.

There is very little invented content. No hallucinated model IDs, no invented endpoints, no fabricated statistics — the one heavily-repeated quantitative claim ("up to 30%") is real and correctly attributed.

| Severity | Count | Meaning |
|---|---|---|
| Critical | 2 | Reader copies the code, gets a 400 |
| High | 4 | Materially wrong guidance or classification |
| Medium | 6 | Incomplete or internally contradictory |
| Low | 3 | Editorial / consistency |

---

## Method

1. Read every file; extracted all model IDs, tool `type` strings, beta headers, API parameters, and quantitative claims.
2. Link-checked all 354 unique external URLs. The docs sites return HTTP 200 for missing pages (SPA shell), so each of the 262 documentation URLs was re-checked against its `<title>` versus the generic fallback title.
3. Verified contested claims against the live source pages: models overview, migration guide, prompt caching, context windows, mid-conversation system messages, code execution tool, web search tool, server tools, prompting best practices, Claude Code CLI reference.

---

## Critical

### C1 — `temperature` and `top_p` are taught as working parameters. They return a 400 on every model the track recommends.

**Where**

| File | Line | Content |
|---|---|---|
| `99-reference/api-cheatsheet.md` | 42 | `` `temperature` `` \| 0–1. Don't set alongside `top_p`. |
| `04-api/02-messages-api.md` | 106–112 | "Sampling parameters" table + "Set `temperature=0` for deterministic tasks" |
| `04-api/02-messages-api.md` | 218 | Exercise 3 — "Run the same extraction task ten times at `temperature=0`" |
| `04-api/01-setup-and-first-call.md` | 149 | `` `temperature` `` \| 0–1. Lower is more deterministic. |
| `06-production/02-guardrails.md` | 135 | "For semantic consistency: `temperature=0`" |
| `06-production/01-evals-and-testing.md` | 153 | "Changing the prompt, the model, and the temperature together" |

**Why it's wrong.** The migration guide is explicit:

> Setting `temperature`, `top_p`, or `top_k` to a non-default value on Claude Opus 4.7 or later models, including Claude Opus 5, returns a 400 error.
> […] The safest migration path is to omit these parameters entirely from request payloads. Prompting is the recommended way to guide model behavior on Claude Opus 5.

This covers Opus 5, Opus 4.8, Opus 4.7, Sonnet 5, Fable 5, and Mythos 5 — i.e. every model the track tells readers to use. Only Haiku 4.5 and Sonnet 4.5-and-older still accept them. The running example model in `04-api/02-messages-api.md` is `claude-sonnet-5`, so Exercise 3 as written cannot be completed.

This is the most consequential error in the repo: it is taught in a reference table, repeated in a beginner setup file, built into an exercise, and relied on for production guardrails advice.

**Proposed fix**

- Replace both parameter-table rows with a single note: *sampling parameters are removed on current models; setting them to a non-default value returns a 400. Steer behaviour with prompting, or `output_config.format` for determinism of shape.*
- Rewrite `04-api/02-messages-api.md` Exercise 3. A direct replacement that teaches the same lesson: run the same extraction task twenty times unchanged and count variations, then add a `json_schema` via `output_config.format` and count again. That demonstrates "constrain the output, don't tune the sampler," which is the current-model answer.
- In `06-production/02-guardrails.md:135`, replace `temperature=0` with structured outputs (`output_config.format` with `strict: true` on tools) plus few-shot examples — the same paragraph already recommends the other two.
- In `06-production/01-evals-and-testing.md:153`, change "the temperature" to "the effort level," which is the current knob and keeps the point about one-change-at-a-time intact.

---

### C2 — The legacy, Python-only code execution tool is taught throughout, along with a beta header that is no longer required.

**Where**

| File | Line | Content |
|---|---|---|
| `99-reference/api-cheatsheet.md` | 181 | `{"type": "code_execution_20250522", ...}` |
| `99-reference/api-cheatsheet.md` | 247–248 | `betas=[... "code-execution-2025-05-22"]` + `code_execution_20250522` |
| `04-api/05-server-tools-and-mcp.md` | 71–72 | `code_execution_20250522` + `betas=["code-execution-2025-05-22"]` |
| `04-api/05-server-tools-and-mcp.md` | 148 | `code_execution_20250522` in the combined-tools example |
| `04-api/10-skills-in-the-api.md` | 40–41 | Same pair, in the Skills request |

**Why it's wrong.** The code execution tool page lists exactly three current versions — `code_execution_20250825`, `code_execution_20260120`, `code_execution_20260521` — and treats `code_execution_20250522` as the thing you migrate *off*:

> If you're still using the legacy `code_execution_20250522` (Python only), see Upgrade to latest tool version to migrate from it.

and

> All three tool versions are generally available and don't require an `anthropic-beta` header.

Its own migration table maps `Beta header: code-execution-2025-05-22` → `None required`, and `Tool type: code_execution_20250522` → `code_execution_20250825 or later`.

Three knock-on consequences in the track:

1. The `betas=["code-execution-2025-05-22"]` entries are unnecessary on current versions.
2. `04-api/05:31` describes code execution as "Run Python in a sandbox" — true of the legacy version only. Current versions run bash commands and file operations too, which is also what makes the "Bash" and "Text editor" rows two lines below coherent.
3. Response block types differ: legacy returns `code_execution_result`, current returns `bash_code_execution_result` / `text_editor_code_execution_*_result`. Any reader parsing responses against the track's description will miss.

**Proposed fix**

- Replace all five `code_execution_20250522` occurrences with `code_execution_20260521`.
- Delete `code-execution-2025-05-22` from every `betas` list. In `04-api/10-skills-in-the-api.md:40` the remaining list is correct as `["skills-2025-10-02", "files-api-2025-04-14"]`.
- Update `04-api/05:31` to "Run Python and bash in a sandbox; create and edit files."
- Add one line noting the response block types, since the track elsewhere is good about telling readers to iterate `content` blocks.

---

## High

### H1 — The prompt-cache prefix order is stated backwards, in three places.

**Where**

| File | Line | Stated order |
|---|---|---|
| `04-api/07-prompt-caching.md` | 48–55 | System prompt → Tool definitions → Reference docs |
| `04-api/07-prompt-caching.md` | 66–70 | system = breakpoint 1, tools = breakpoint 2 |
| `99-reference/api-cheatsheet.md` | 212 | `system → tools → reference docs → breakpoint → history` |
| `05-agents/03-context-engineering.md` | 44–50 | System prompt → Tool definitions → Reference docs |

**Why it's wrong.** From the prompt caching docs:

> Cache prefixes are created in the following order: `tools`, `system`, then `messages`. This order forms a hierarchy where each level builds upon the previous ones.

The mid-conversation system messages page repeats it and draws the consequence: "The `tools` array sits even earlier in the hashed request prefix than the top-level `system` field."

The multi-breakpoint example at `04-api/07:66–70` is not constructible as written — it puts breakpoint 1 on the system prompt and breakpoint 2 on the tool definitions, but tools are hashed first, so that numbering inverts the actual nesting. A reader following it will place breakpoints that don't do what the diagram claims.

This also undercuts the track's own (correct) advice that changing tools invalidates the cache — the reason it does is precisely that tools sit at position 0.

**Proposed fix.** Swap to `tools → system → messages` in all four locations, and renumber the breakpoint example so tools is breakpoint 1. In `05-agents/03-context-engineering.md` the surrounding claim that the two rules "agree with each other" still holds after the swap.

---

### H2 — Mid-conversation system messages are presented as universally available. They are not available on Sonnet 5 — the file's own example model.

**Where:** `04-api/02-messages-api.md:96–100`

> You can change the system prompt or the tool set partway through a conversation. Useful for multi-phase agents — a research phase with search tools, then a writing phase with different instructions.

**Why it's wrong.** From the feature's own page:

> This feature is available on Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, and Claude Opus 5. No beta header is required for mid-conversation system messages. **This feature is not available on Claude Sonnet 5; use the top-level `system` field instead.**

And separately, the tool half is beta and gated:

> Mid-conversation tool changes are in beta and require the `mid-conversation-tool-changes-2026-07-01` beta header. They are available on Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, and Claude Opus 5.

Every code example in that file uses `claude-sonnet-5`, so a reader will naturally try this on the one current model where it returns a 400. The section also conflates two distinct features (GA system messages; beta tool changes) into one sentence.

**Proposed fix.** Split into two sentences with the model list and the beta header stated, and add the placement constraint (a system message must follow a `user` turn and cannot be `messages[0]`), which is the other thing that 400s.

---

### H3 — Bash, text editor, and memory are classified as *server* tools. All three are client-implemented.

**Where**

| File | Line | Content |
|---|---|---|
| `04-api/05-server-tools-and-mcp.md` | 32–35 | "The server tool catalogue" table lists Bash, Text editor, Memory |
| `99-reference/glossary.md` | 86 | "**Memory tool** — a server tool giving Claude persistent memory" |
| `99-reference/glossary.md` | 122 | "**Server tool** — a tool Anthropic executes for you (web search, code execution, computer use, memory, advisor)" |

**Why it's wrong.** The server tools page defines the boundary explicitly:

> A client tool is any tool that your code executes and that produces a `tool_use` block, whether it is user-defined or **an Anthropic-schema client tool such as the Bash tool**.

Bash and text editor are Anthropic-*defined* (fixed schema, declared by `type`) but client-*executed* — you run the command and return a `tool_result`. The memory tool is likewise client-side: Anthropic defines the command set, you implement the storage backend.

This matters more than a taxonomy nit because the table sits directly under the file's framing at lines 14–21: *"Executed by: Anthropic's infrastructure / You implement: Nothing / Loop: Handled for you."* A reader will expect to enable the memory tool and get persistence for free. They will instead get `tool_use` blocks for a backend they haven't written.

**Proposed fix.** Split the catalogue into two tables — server-executed (web search, web fetch, code execution, tool search, advisor) and Anthropic-defined but client-executed (bash, text editor, memory; computer use can be either). Add one line: *bash and file operations also exist as sub-tools **inside** the code execution container — that is the server-side path, and it is different from the standalone client tools.* Correct both glossary entries.

---

### H4 — Web search examples are pinned to the oldest of three tool versions, and the ZDR interaction is unmentioned.

**Where:** `99-reference/api-cheatsheet.md:180`, `04-api/05-server-tools-and-mcp.md:49`, `:147` — all `web_search_20250305`.

**Why it matters.** Not broken — `web_search_20250305` is still valid and still shown in the official basic example. But the docs list three versions and the track mentions only the oldest:

> * `web_search_20250305`: basic web search
> * `web_search_20260209`: adds dynamic filtering
> * `web_search_20260318`: adds response inclusion control for agentic workflows

Dynamic filtering has a direct bearing on two themes the track cares about a lot — token cost and context hygiene: "Claude instead writes and runs code that filters the results first, so only relevant content reaches the context window. This reduces token use on search-heavy requests."

There is also a trap the track is well-positioned to warn about, given it covers ZDR in `06-production/05`: the `_20260209` and later versions are **not** ZDR-eligible by default, because dynamic filtering uses code execution internally. The escape hatch is `"allowed_callers": ["direct"]`.

**Proposed fix.** Move the examples to `web_search_20260318`, add a three-line version table, and add the ZDR caveat to `04-api/05`. Note in the same place that you should *not* separately declare `code_execution` alongside a `_20260209`+ web tool — the API provisions it automatically.

---

## Medium

### M1 — The track contradicts itself on model-routing savings, by a factor of two.

| File | Line | Claim |
|---|---|---|
| `99-reference/model-cheatsheet.md` | 48 | "Typically 60–80% cheaper with equal or better quality" |
| `06-production/03-cost-and-latency.md` | 49 | "Typical result: 60–80% cost reduction with equal or better quality" |
| `01-foundations/03-models-and-modes.md` | 90 | "The realistic win on a pipeline like this is **30–50%, not an order of magnitude**" |

All three are unsourced. `01-foundations/03` is the honest one — it shows the arithmetic (Haiku is 3× cheaper than Sonnet, so that bounds the classification step; routing hard cases *up* to Opus spends some back) and explicitly warns against the rule of thumb the other two files state.

**Proposed fix.** Adopt the 30–50% figure and the reasoning from `01-foundations/03` in all three places, or drop the number entirely and keep the method. A reader who reads the foundations file and then the cheat sheet will not know which to believe.

### M2 — Cache minimums are never stated, and the one number given is wrong for half the models taught.

`04-api/07-prompt-caching.md:117` says caching suits "Anything with a prefix over ~2,000 tokens." Line 121 lists "Prefix under the minimum cacheable size" as a poor fit without ever defining it.

Official minimums are per-model and **not monotonic across generations**:

| Model | Minimum |
|---|---|
| Opus 5, Fable 5, Mythos 5 | 512 |
| Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 | 1,024 |
| Opus 4.7 | 2,048 |
| Opus 4.6, Opus 4.5, **Haiku 4.5** | 4,096 |

So "~2,000" is too conservative for Opus 5 and Sonnet 5 (discourages caching that would work) and less than half the real threshold for Haiku 4.5 — where a marked prefix silently isn't cached and returns no error. Given the file's Exercise 2 is "break it deliberately and watch the number drop to zero," the silent-failure threshold belongs here.

**Proposed fix.** Add the table, flag the non-monotonicity, and note that a sub-minimum prefix produces `cache_creation_input_tokens: 0` with no error.

### M3 — Cache write cost is described only as "slightly more".

`04-api/07-prompt-caching.md:93`: "writing costs slightly *more* than normal input."

Actual: **1.25×** for the 5-minute TTL and **2×** for the 1-hour TTL, against 0.1× for reads. That sets break-even at two requests on the 5-minute TTL and three on the 1-hour. In a file whose entire subject is cost, the actual multipliers are more useful than "slightly," and they're what tells a reader whether the 1-hour TTL (line 78, currently just "Longer TTL options exist at different pricing") is worth it.

### M4 — Stop-reason coverage is incomplete, while the checkpoint demands completeness.

`99-reference/api-cheatsheet.md:82–88` lists `end_turn`, `max_tokens`, `tool_use`, `stop_sequence`, `refusal`. Missing:

- **`pause_turn`** — returned by the server-side loop for web search, web fetch, and code execution, all of which the track teaches in `04-api/05`. Handling is non-obvious: re-send the assistant content unchanged, and keep the same `tools` array or the continuation 400s.
- **`model_context_window_exceeded`** — Claude 4.5 and newer, distinct from `max_tokens`.

Meanwhile `04-api/02-messages-api.md:232` sets the checkpoint "You handle every `stop_reason` value" — which the track never enumerates. `04-api/02` does handle `refusal` and fallback well.

**Proposed fix.** Add both rows to the cheat sheet table and a short `pause_turn` paragraph to `04-api/05`, where server tools are introduced.

### M5 — Code execution pricing omits the free tier.

`04-api/05-server-tools-and-mcp.md:175` gives "Code execution: per container-hour." The docs add two things that change the calculus: it is **free when used with web search or web fetch** (`web_search_20260209` / `web_fetch_20260209` or later), and standard pricing is $0.05/hour after 1,550 free hours per month per organisation. For most readers of this track, code execution is effectively free; the current line implies otherwise.

### M6 — `output-300k-2026-03-24` support is vague in one place, precise in another.

`99-reference/api-cheatsheet.md:283` says "on supported models." `99-reference/model-cheatsheet.md:33` correctly names them (Opus 5, Opus 4.8/4.7/4.6, Sonnet 5, Sonnet 4.6) and matches the docs exactly. Cross-reference rather than leaving the vaguer statement to stand alone.

---

## Low / consistency

### L1 — Cutoff terminology varies across files.

The values are correct everywhere (verified against the models overview). But the label differs: `99-reference/model-cheatsheet.md:24` "Reliable cutoff", `01-foundations/03-models-and-modes.md:40` "Knowledge cutoff", `00-start-here/01-what-claude-is.md:96` "Reliable knowledge cutoff".

Anthropic distinguishes two dates and the difference is material for Haiku 4.5: **reliable knowledge cutoff Feb 2025, training data cutoff Jul 2025**. Use the official term "reliable knowledge cutoff" consistently, and consider a one-line footnote on the distinction — the track already teaches readers to distrust post-cutoff facts, so the nuance lands.

### L2 — `04-api/05:31` "Also what powers Agent Skills."

Correct, but worth tightening to match `04-api/10`'s framing that the code execution tool is a *prerequisite* you must declare, not just an implementation detail.

### L3 — `05-agents/03-context-engineering.md:123`

"a capable agent will politely give up with 30% of its budget left" — presented as fact, unsourced, and a suspiciously precise number. The underlying behaviour is real and well-documented (context awareness causes premature wrap-up; the docs and `04-api/02:151–164` both cover the mitigation prompt). Recommend dropping the figure and keeping the behaviour.

---

## Verified correct

Worth recording, both to avoid re-litigating and because several of these are places where third-party material usually goes wrong:

- **All 262 documentation deep links resolve.** No dead links, no redirects to generic pages. (Non-Anthropic and `support.claude.com` links could not be checked from this environment — outbound proxy blocks those hosts — so they are unverified rather than broken.)
- **Model tables are exact.** IDs, aliases, pricing, context windows, max output, latency ranking, adaptive vs extended thinking columns, Sonnet 5 introductory pricing and its 31 Aug 2026 end date, and the `output-300k-2026-03-24` batch beta all match the models overview.
- **Reliable knowledge cutoffs** — Fable 5 Jan 2026, Opus 5 May 2026, Sonnet 5 Jan 2026, Haiku 4.5 Feb 2025. All four correct.
- **Effort defaults**, including the subtle surface distinction: `high` on the Claude API and Claude Code for Opus 5 / Sonnet 5, versus `high` everywhere including claude.ai for Opus 4.8. This matches the docs almost verbatim and is a detail most secondary sources miss.
- **Thinking defaults per model**, `budget_tokens` returning 400 on 4.7+, prefill removal from 4.6 onward, and the Opus 5 rule that thinking can be disabled only at effort `high` or lower — all correct.
- **Context awareness model list** (`04-api/02:151`) — Sonnet 5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5. Exact match, including the correct omission of Opus models.
- **Mythos 5 / Project Glasswing** framing — invitation-only, defensive cybersecurity, no self-serve access, same specs and pricing as Fable 5. Matches the docs' callout.
- **The "up to 30%" claim** (6 occurrences) is real and fairly attributed: *"Queries at the end can improve response quality by up to 30 percent in tests, especially with complex, multidocument inputs."*
- **Model IDs are pinned snapshots from the 4.6 generation onward** — correct, and correctly distinguished from the older dated-ID-plus-alias scheme.
- **Claude Code CLI surface** — spot-checked `--effort low|medium|high|xhigh|max|ultracode`, `--advisor`, `--teleport`, `--fallback-model`, `--max-budget-usd`, `--bare`, `--safe-mode`, `--teammate-mode`, and `claude ultrareview`. All exist as documented. `ultracode` is correctly scoped to the CLI rather than presented as an API `effort` value.
- **Cache breakpoint maximum of four** — correct in all three places it appears.
- **No fabricated model IDs, endpoints, or SDK methods** anywhere in the repo.

---

## Recommendation on process

Every Critical and High finding is the same failure mode: a tool version or parameter that was correct when written and has since moved. The model and Claude Code content has clearly been refreshed; the API tool surface has not.

Two cheap guards:

1. **A CI grep for stale identifiers.** Fail the build on any `*_2025*` tool `type` string, any `betas=[...]` entry that has since gone GA, and any `temperature`/`top_p`/`top_k` in a code block whose `model=` is a current model. All of this review's Critical findings would have been caught by roughly twenty lines of regex.
2. **A link-checker that inspects `<title>`, not status code.** The docs sites return 200 for missing pages; a naive checker reports a clean bill of health regardless. The check used here — compare against the generic fallback title `Documentation | Claude Platform` — is reliable and fast.

The `*Verify against …*` disclaimers already present in the cheat sheets are good practice and should stay, but they are not a substitute for either guard: a reader who copies `code_execution_20250522` will hit the error long before they check the source.
