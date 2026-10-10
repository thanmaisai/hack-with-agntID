---
title: Flow Diagrams
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Flow Diagrams

Use these diagrams to explain how the main parts of AgntID work together. Each diagram gives a current overview; follow the linked guide for exact steps and settings.

</div>

## Choose a flow

| If you want to understand… | Start here |
| --- | --- |
| First-time runtime setup | [Quick Start flow](#quick-start-flow) |
| What runs in the portal and in your environment | [Portal and runtime](#portal-and-runtime) |
| How an MCP server reaches a client | [MCP server to client](#mcp-server-to-client) |
| How to add an MCP server | [Add an MCP server](#add-an-mcp-server) |
| Where OAuth applies | [OAuth connections](#oauth-connections) |
| How Simulator runs a request | [Simulator request](#simulator-request) |
| How an SDK request is protected | [SDK request](#sdk-request) |

## Quick Start flow

Register and deploy the runtime, complete Setup, run a protected tool, and confirm its result in Reporting. The optional branch adds input limits and compares an allowed call with a denied call.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/quick-start-flow.svg" alt="Quick Start flow from runtime registration through Reporting, with an optional input-limit exercise" />
  <img class="diagram-dark" src="../assets/diagrams/quick-start-flow-dark.svg" alt="Quick Start flow from runtime registration through Reporting, with an optional input-limit exercise" />
</div>

[Follow the Quick Start](quick-start.md){ .md-button }

## Portal and runtime

The [AgntID portal](https://app.agntid.ai/) is the control plane. It manages protection profiles, detailed policies, and reporting. The customer-hosted runtime receives signed updates, filters the tool list, checks every tool call locally, and connects clients to built-in or customer MCP servers.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/architecture-flow.svg" alt="AgntID portal synchronizing profiles and policies to a customer runtime that filters and protects MCP tools" />
  <img class="diagram-dark" src="../assets/diagrams/architecture-flow-dark.svg" alt="AgntID portal synchronizing profiles and policies to a customer runtime that filters and protects MCP tools" />
</div>

The protection profile sets the largest tool list available from the runtime. Individual settings, OAuth role grants, and policies can reduce access further.

## MCP server to client

Add the MCP server in the portal. The runtime applies the configuration, discovers its tools, and shows a client only the tools allowed by the selected profile and any client role. Reporting records each call's result.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/mcp-journey.svg" alt="MCP journey from adding a server through discovery and profile filtering to a client and Reporting" />
  <img class="diagram-dark" src="../assets/diagrams/mcp-journey-dark.svg" alt="MCP journey from adding a server through discovery and profile filtering to a client and Reporting" />
</div>

[Use MCP with AgntID](mcp/index.md){ .md-button }

## Add an MCP server

The portal stores the server configuration. The customer runtime tests the connection, discovers tools, and applies the saved configuration. You then review tool availability and run a safe test.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/mcp-attach-flow.svg" alt="Flow for adding, testing, applying, reviewing, and using an MCP server" />
  <img class="diagram-dark" src="../assets/diagrams/mcp-attach-flow-dark.svg" alt="Flow for adding, testing, applying, reviewing, and using an MCP server" />
</div>

[Add an MCP server](mcp/attach-server.md){ .md-button }

## OAuth connections

OAuth can protect incoming client access to the AgntID runtime. The runtime may use a separate credential when it connects to an external MCP server. Keeping these two connections separate helps you configure and troubleshoot them correctly.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/mcp-oauth-flow.svg" alt="OAuth-protected connection from an MCP client to the AgntID runtime and a separate authenticated connection to an external MCP server" />
  <img class="diagram-dark" src="../assets/diagrams/mcp-oauth-flow-dark.svg" alt="OAuth-protected connection from an MCP client to the AgntID runtime and a separate authenticated connection to an external MCP server" />
</div>

[Protect MCP access with OAuth](mcp/oauth.md){ .md-button }

## Simulator request

Simulator sends a plain-English request to the selected AI model. The model chooses from profile-visible tools, and the runtime checks the chosen call before any tool runs. Simulator then shows the result, call flow, audit details, and timing.

Use [Configure the intent engine](runtime/intent-engine.md) to choose Standard or LLM-based intent. Use [Read intent checks in Simulator](simulator/intent.md) to understand the stages shown in Call Flow.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/simulator-runtime-flow.svg" alt="Simulator request moving from the portal and AI model through the customer runtime policy check to an MCP tool" />
  <img class="diagram-dark" src="../assets/diagrams/simulator-runtime-flow-dark.svg" alt="Simulator request moving from the portal and AI model through the customer runtime policy check to an MCP tool" />
</div>

[Run a Simulator test](simulator/index.md){ .md-button }

## SDK request

The SDK keeps identity and task context with a request. The runtime lists eligible tools, checks the selected tool and inputs, and returns either the tool result or a denial. Reporting keeps the outcome for review.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/sdk-request-flow.svg" alt="SDK request from user input through task context, profile-filtered tool choice, runtime protection, tool execution, and task completion" />
  <img class="diagram-dark" src="../assets/diagrams/sdk-request-flow-dark.svg" alt="SDK request from user input through task context, profile-filtered tool choice, runtime protection, tool execution, and task completion" />
</div>

[Read the Python SDK guide](sdk/python-guide.md){ .md-button }

## How access decisions fit together

| Layer | Purpose |
| --- | --- |
| Protection profile | Sets the largest group of tool actions the runtime can show |
| Tool review and state | Confirms the action classification and whether the tool is enabled |
| OAuth role grants | Reduce the visible actions for a verified client role |
| Policy | Checks a visible tool call and its input values |
| Runtime | Enforces the current decision before the MCP tool runs |
| Reporting | Records the allowed or denied result |

A detailed policy for one tool does not block all other tools. Each tool continues to follow its own profile, state, role grants, and policy decision.

## Related guides

- [Troubleshooting](troubleshooting.md)
- [Connect Cursor, Claude, or Codex](mcp/connect-clients.md)
- [SDK examples](sdk/examples.md)
- [Release Notes](release-notes.md)
