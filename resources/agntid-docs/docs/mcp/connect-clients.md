---
title: Connect Cursor, Claude, or Codex
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Connect Cursor, Claude, or Codex

Connect an MCP client directly to the AgntID runtime. The runtime gives the client a profile-filtered tool list and checks every tool call before execution.

</div>

## Before you begin

Confirm that:

- the runtime is **Healthy** and **Connected**
- **MCP Support** is enabled
- at least one MCP server is **Applied**
- the client can reach the runtime MCP address

If the client runs on the runtime host, the usual address is `http://localhost:8082/mcp`. For another machine, use an address that is reachable from that machine.

## 1. Generate the configuration

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select your runtime.
2. Open **Operations → MCP → Clients**.
3. Select **Cursor**, **Claude**, or **Codex**.
4. Select where the client runs:

    - **Same machine** uses `localhost`.
    - **Same network** uses the runtime host on your network.
    - **Custom host** lets you enter another reachable address.

5. Confirm the **Runtime MCP URL**.
6. Select **Copy Config**.

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/05-client-config.png" alt="Connect MCP Client panel generating Cursor configuration for a runtime on the same machine" />
</div>

Always copy the current configuration from the portal. This keeps the endpoint and OAuth scopes in sync with the runtime.

## 2. Save it in the client

| Client | Configuration file | What to do next |
| --- | --- | --- |
| **Cursor** | `~/.cursor/mcp.json` or project `.cursor/mcp.json` | Merge the generated `mcpServers` entry and reload Cursor |
| **Claude** | Project `.mcp.json` or user `~/.claude.json` | Merge the generated `mcpServers` entry and reload Claude |
| **Codex** | `~/.codex/config.toml` or project `.codex/config.toml` | Merge the generated TOML block |

Do not replace unrelated client settings. Add or merge the generated `agntid` entry.

If OAuth is required, sign in when the client asks. For Codex, run:

```bash
codex mcp login agntid
```

See [Protect MCP access with OAuth](oauth.md) before testing an authenticated connection.

## 3. Confirm the connection

1. Open the client's MCP server or tools view.
2. Confirm that `agntid` is connected.
3. List the available tools.
4. Run a safe test tool.
5. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes → Runtime → Operations → MCP → Access Dashboard**.
6. Confirm the client activity and tool result.

The client sees only tools allowed by all of these controls:

1. The tool was discovered and reviewed.
2. The runtime protection profile includes the action.
3. The tool is not disabled by an individual setting.
4. When OAuth role filtering is active, the signed-in user has a matching role grant.

Policies still check the inputs and context when a visible tool is called.

## Network guidance

- Use `localhost` only when the client and runtime are on the same machine.
- Do not publish port `8082` to the internet without network protection and OAuth.
- Prefer a private network, VPN, or another approved protected route for remote clients.
- The Inspector tunnel is separate from the direct client address generated on this page.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Client cannot connect | Confirm the selected client location, host, port, and firewall rules |
| `localhost` fails | Confirm the client runs on the same machine as the runtime |
| Login opens but tools do not load | Check the OAuth credential, MCP Server Address, required scopes, and client logs |
| Expected tool is missing | Check the protection profile, classification review, individual tool state, and role grants |
| Tool is listed but the call is denied | Review the policy result in Access Dashboard or Reporting |

## What’s next

- [Protect client access with OAuth](oauth.md)
- [Add another MCP server](attach-server.md)
- [Review tool visibility](index.md#how-tool-visibility-works)
