---
title: Use MCP with AgntID
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Use MCP with AgntID

Use AgntID to place access controls between MCP clients and the tools they use. You add an MCP server in the [AgntID portal](https://app.agntid.ai/), the customer-hosted runtime discovers its tools, and the runtime shows each client only the tools allowed by its protection profile.

</div>

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/mcp-journey.svg" alt="MCP journey from adding a server in the portal through runtime discovery and profile filtering to a connected client and reporting" />
  <img class="diagram-dark" src="../../assets/diagrams/mcp-journey-dark.svg" alt="MCP journey from adding a server in the portal through runtime discovery and profile filtering to a connected client and reporting" />
</div>

## Before you begin

Complete the [Quick Start](../quick-start.md). Your runtime must be **Healthy**, **Connected**, and have **MCP Support** enabled.

Use the guides in this order:

1. [Add an MCP server](attach-server.md).
2. [Review its discovered actions and classifications](advanced.md).
3. [Connect Cursor, Claude, or Codex](connect-clients.md).
4. If required, [protect client access with OAuth](oauth.md).
5. Review activity in **MCP → Access Dashboard** and **Reporting**.

## Servers, tools, and clients

| Term | Meaning |
| --- | --- |
| **MCP server** | Provides tools, such as a remote service or a process started by the runtime |
| **Tool** | One action provided by a server, such as listing files or creating an issue |
| **MCP client** | Uses the tools, such as Cursor, Claude, or Codex |
| **AgntID runtime** | Discovers tools, filters the tool list, checks every call, and records the outcome |

## How tool visibility works

Adding a server does not make every tool available to every client. AgntID reviews each discovered action and applies the runtime's protection profile.

| Profile | Tools that can be shown after review |
| --- | --- |
| **Low** | All reviewed actions, unless an individual setting or policy blocks them |
| **Medium** | Reviewed read and normal-write actions; destructive and high-impact actions remain hidden |
| **High** | Reviewed read and list actions that do not change data |

A tool can also remain hidden while its classification is waiting for review, when it is disabled, or when a client role does not have access. Policies continue to check calls for tools that are visible.

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/04-profile-visible-tools.png" alt="Tools page showing a discovered MCP tool surface, its Medium protection profile, and actions that need review" />
</div>

## Choose the right test

| Goal | Use |
| --- | --- |
| Call a tool directly | [Inspector](../quick-start.md#optional-debug-raw-mcp-behavior-with-mcp-inspector) |
| Send a plain-English request and let an AI model select a tool | [Simulator](../simulator/index.md) |
| Test the experience used by developers | [Cursor, Claude, or Codex](connect-clients.md) |

Inspector uses a secure AgntID tunnel. Simulator uses a portal-controlled runtime session. Neither test proves that an external client's OAuth login works. Test OAuth with the client that people will use.

If you want the model to work from a plain-English request, configure the [intent engine](../runtime/intent-engine.md). Then use [Read intent checks in Simulator](../simulator/intent.md) to understand tool shortlisting, output inspection, and final-answer validation.

## Two different kinds of authentication

- **Client access** protects the connection from Cursor, Claude, Codex, or another MCP client to the AgntID runtime. See [Protect MCP access with OAuth](oauth.md).
- **Server credentials** let the runtime connect to an external MCP server. Configure them while [adding the server](attach-server.md#server-credentials).

Keeping these directions separate makes it clear which connection is being protected.

## What’s next

- [Add an MCP server](attach-server.md)
- [Review Advanced access controls](advanced.md)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)
- [Troubleshooting](../troubleshooting.md)
