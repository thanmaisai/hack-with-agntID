---
title: TypeScript SDK
last_verified: 2026-09-04
owner: sdk-team
---

<div class="page-intro" markdown>

# TypeScript SDK

A public TypeScript SDK is planned but is not available yet. Use the Python SDK for application integration or connect a TypeScript MCP client directly to the runtime.

</div>

## Available today

| Need | Use |
| --- | --- |
| Add AgntID task and tool correlation to application code | [Python SDK](python.md) |
| Connect an MCP-compatible TypeScript client | Runtime MCP address, usually `http://localhost:8082/mcp` |
| Connect Cursor, Claude, or Codex | [MCP client guide](../mcp/connect-clients.md) |

A direct MCP client receives the same profile-filtered tool list and runtime policy checks. It does not receive the Python SDK's task helpers, result types, or framework adapters.

## Planned scope

The TypeScript SDK is expected to provide the same core workflow as Python:

- connect and discover available tools
- open and close one task for each user request
- correlate tool calls to that task
- return clean results and structured denials

No package name, installation command, or release date is published yet.
