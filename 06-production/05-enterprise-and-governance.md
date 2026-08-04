---
title: "Enterprise and governance"
order: 5
---

# Enterprise and governance

**What you'll learn:** what exists for deploying Claude across an organisation — so you know what to ask for rather than building it yourself.

---

## Identity and access

### Workspaces

Separate API keys, budgets, and rate limits per project or team. The first thing to set up in any organisation — it makes cost attribution and blast-radius containment possible.

See [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces).

### Admin API

Programmatic management of organisations, users, roles, groups, service accounts, and settings.

See [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api) and [Create an Admin API key](https://platform.claude.com/docs/en/manage-claude/admin-api-keys).

### Workload Identity Federation

API access **without long-lived keys**. Your workloads authenticate with their existing identity.

Supported providers: AWS, Google Cloud, Microsoft Entra ID, Okta, Kubernetes, SPIFFE, GitHub Actions.

This is the correct answer to "how do we give CI an API key" — you don't.

- [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation)
- [WIF reference](https://platform.claude.com/docs/en/manage-claude/wif-reference)
- [Manage WIF with the Admin API](https://platform.claude.com/docs/en/manage-claude/wif-admin-api)

---

## Spend and usage

| API | What |
|---|---|
| [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api) | Per-developer and per-group caps, with an approval flow for increases |
| [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api) | Pull consumption into your own systems |
| [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api) | Adoption and usage patterns |
| [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api) | Claude Code usage, adoption, engineering velocity |
| [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api) | Current limits, programmatically |

---

## Data governance

### Retention and residency

- [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) — what's retained, for how long, per feature
- [Data residency](https://platform.claude.com/docs/en/manage-claude/data-residency) — where data is processed
- [Zero data retention](https://code.claude.com/docs/en/zero-data-retention) — available to qualified Claude for Enterprise accounts, with documented feature trade-offs

> **Note:** Agent Skills are **not** covered by ZDR arrangements. Skill definitions and execution data follow standard retention. Check per-feature ZDR eligibility before assuming coverage.

### Customer-managed encryption keys

Bring your own key, via AWS KMS, Azure Key Vault, or Google Cloud KMS.

See [Customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek).

### Compliance API

Retrieve and delete chats, files, projects, artifacts and code sessions; query an activity feed; list org data. This is what your compliance team needs for e-discovery, audits and deletion requests.

- [Compliance API overview](https://platform.claude.com/docs/en/manage-claude/compliance-api)
- [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access)
- [Design your compliance integration](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns)
- [Retrieve and delete chats, files, and projects](https://platform.claude.com/docs/en/manage-claude/compliance-content-data)
- [Query the Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed)

Note: Cowork sessions on web and mobile are captured in the Compliance API.

### Access Transparency

Visibility into access to your data. See [Access Transparency](https://platform.claude.com/docs/en/manage-claude/access-transparency).

---

## Deploying Claude Code across an organisation

The decision map is [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup). The pieces:

### Managed settings

Client-enforced, regardless of what a user configures:

| Control | Setting |
|---|---|
| Block tools, commands, file paths | `permissions.deny` |
| Enforce sandbox isolation | `sandbox.enabled` |
| Disable bypass mode | `permissions.disableBypassPermissionsMode` |
| Environment variables and provider routing | `env` |
| Auth method and org lock | `forceLoginMethod`, `forceLoginOrgUUID` |
| Behavioural guidance | `claudeMd`, or a managed CLAUDE.md file |
| Approved version range | Managed settings |

Deploy via MDM, Group Policy, Ansible — or via [server-managed settings](https://code.claude.com/docs/en/server-managed-settings), which needs no device management infrastructure.

### MCP governance

Allowlists and denylists of which MCP servers users may add or connect to, plus org-wide `ask` settings on connector tools.

See [Control MCP server access for your organization](https://code.claude.com/docs/en/managed-mcp).

### Gateways

Route Claude Code through a self-hosted gateway for centralised credentials, usage tracking, and cost controls.

- [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway) — Anthropic's, with SSO sign-in, per-group model access, OTLP telemetry, and [live-enforced spend limits](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)
- [Other LLM gateways](https://code.claude.com/docs/en/llm-gateway) — if you already run one
- [Gateway protocol reference](https://code.claude.com/docs/en/llm-gateway-protocol) — what must be forwarded, and what degrades if it isn't

### Network

Proxies, custom CAs, and mutual TLS. See [Enterprise network configuration](https://code.claude.com/docs/en/network-config).

### Cloud providers

Amazon Bedrock, Claude Platform on AWS, Google Vertex AI, Microsoft Foundry. Feature availability differs — check [Feature availability](https://code.claude.com/docs/en/feature-availability) before committing.

---

## Consumer-side org controls

For claude.ai, Cowork and Chat:

- **Capabilities** — network access and web search, in Admin settings → Capabilities
- **Claude in Chrome** — Organization settings → browser extension
- **Cowork on Team/Enterprise** — may require per-task approval for write-capable connector tools, overriding individual "always allow" preferences. See [Use Claude Cowork on Team and Enterprise plans](https://support.claude.com/en/articles/13455879-use-claude-cowork-on-team-and-enterprise-plans)
- **Skill provisioning** — Team and Enterprise Owners can provision skills for all users; they appear automatically in every member's list and can default to enabled or disabled. See [Provision and manage skills for your organization](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization)
- **Software Directory policy** — governs what appears in the skills, connectors and plugins directory. See [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)

---

## Rollout

Anthropic publishes material for the human side, which is usually the harder part:

- [Champion kit](https://code.claude.com/docs/en/champion-kit) — a playbook for engineers advocating internally
- [Communications kit](https://code.claude.com/docs/en/communications-kit) — launch announcements, drip campaigns, FAQ responses
- [Analytics](https://code.claude.com/docs/en/analytics) — measure adoption and velocity

A rollout order that works:

1. **Pilot** with a small, willing team
2. **Managed settings** with sane deny rules and sandboxing on
3. **Workspaces and spend limits** before wide access
4. **Shared configuration** — committed CLAUDE.md, `.mcp.json`, project skills
5. **A plugin or marketplace** once patterns stabilise
6. **Measure** adoption and cost; iterate

Deploying without steps 2 and 3 is how organisations end up with a surprise bill and an incident.

---

## Legal and compliance

- [Legal and compliance (Claude Code)](https://code.claude.com/docs/en/legal-and-compliance)
- [Security and compliance / Trust Center](https://trust.anthropic.com)
- [Usage policy](https://www.anthropic.com/legal/aup)
- [Commercial terms](https://www.anthropic.com/legal/commercial-terms)

---

## Try it

**Exercise 1 — Workspaces.**
Set up a workspace with a budget for each project you run. Move your keys.

**Exercise 2 — Managed settings draft.**
Write the managed settings you'd deploy: deny rules, sandbox, auth lock. Even if you can't deploy them yet, having the draft makes the conversation with IT concrete.

**Exercise 3 — Spend limits.**
Set a per-developer spend limit via the API. Trigger it deliberately.

**Exercise 4 — WIF.**
Set up Workload Identity Federation for one CI pipeline. Delete the long-lived key.

**Exercise 5 — Compliance dry run.**
Use the Compliance API to retrieve and then delete a test conversation. Now you know the process before someone asks for it urgently.

**Exercise 6 — Rollout plan.**
Write the six-step rollout for your organisation, with names against each step.

---

## Checkpoint

- Workspaces with budgets exist for every project
- You have a draft of managed settings
- You know which of your workflows are ZDR-eligible and which aren't
- You've done a Compliance API dry run before you needed to

---

## Going deeper

- [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup)
- [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api)
- [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation)
- [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api)
- [Zero data retention](https://code.claude.com/docs/en/zero-data-retention)
- [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway)
- [Feature availability](https://code.claude.com/docs/en/feature-availability)
- [Trust Center](https://trust.anthropic.com)
