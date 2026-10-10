---
title: Add an MCP Server
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Add an MCP Server

Add and test an MCP server from the [AgntID portal](https://app.agntid.ai/). The portal sends the saved configuration to your customer-hosted runtime; you do not need to edit a runtime configuration file or restart the runtime.

</div>

## Before you begin

You need:

- a runtime that is **Healthy** and **Connected**
- **MCP Support** enabled in the runtime's **Setup** tab
- the address or start command for the MCP server
- any required values available as environment variables on the runtime host

The built-in `demo` server is for learning and testing. Add a customer MCP server before using the runtime for real tool access.

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/01-mcp-servers.png" alt="Runtime MCP Servers page showing the built-in demo server and the Add MCP button" />
</div>

## 1. Open MCP Servers

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select your runtime.
2. Open **Operations → MCP → Servers**.
3. Select **Add MCP**.

## 2. Choose how the runtime reaches the server

Use **Form** for normal setup. Use **JSON** only when you need fields that are not shown in the form.

| Connection style | Use it when |
| --- | --- |
| **Remote HTTP** | The MCP server is already running at a URL that the runtime can reach |
| **Local npx** | The runtime should start a Node.js MCP package |
| **Local uvx** | The runtime should start a Python MCP package |
| **Local Docker** | The runtime should start an MCP container |
| **Other local command** | The runtime should start another local program |
| **Service connector** | You are using an AgntID connector, such as AWS S3 |

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/02-add-server.png" alt="Add MCP Server dialog with the server template, connection style, server ID, prefix, and URL fields" />
</div>

For a remote server, enter its MCP URL. For a local server, enter the command and put each command argument on a separate line.

!!! note "Docker-based servers"
    Docker must be available to the runtime. If the runtime is in a container, Docker socket sharing must also be enabled before the connection test can pass.

## 3. Name the server and its tools

- **Server ID** is a short name for the connection, such as `github` or `files`.
- **Prefix** is added to tool names so users can see which server provides them.

Choose a short, stable prefix. For example, the `github` prefix can produce tool names such as `github.create_issue`.

## 4. Add variables and settings

The form separates values into three groups:

- **Environment** contains values read by a local MCP process.
- **Configuration** contains normal settings, such as a region or project name.
- **Credentials** controls how the runtime authenticates to a remote MCP server.

### Server credentials

Do not paste a secret into the portal form. Store the secret as an environment variable on the runtime host and refer to it by name, for example `${GITHUB_TOKEN}`.

The advanced JSON form supports these authentication choices for the connection from the runtime to the external server:

| Choice | What the runtime sends |
| --- | --- |
| `none` | No authentication |
| `bearer_token` | A bearer token read from a runtime environment variable |
| `static_key` | A value from a runtime environment variable in a chosen header |
| `oauth_passthrough` | The signed-in MCP client's OAuth token |

OAuth passthrough is different from protecting access to the runtime. See [Protect MCP access with OAuth](oauth.md) for the client-to-runtime connection.

## 5. Test and save

1. Select **Test Connection**.
2. Confirm **Test passed** and review the discovered-tool count.
3. Select **Save MCP**.
4. Wait for the server row to show **Apply: APPLIED**.

The test runs on the customer-hosted runtime before the portal saves the configuration. A test can confirm that tools were discovered even when a credential can only be checked during the first tool call.

## 6. Review the discovered tools

1. Open **Access Control → Tools**.
2. Filter by your runtime or server.
3. Review any action marked **Needs Review**.
4. Confirm which actions are **Ready** under the runtime's protection profile.

For classification evidence, catalog changes, or corrections, see [Review Advanced access controls](advanced.md).

The profile controls the starting tool list:

- **Low** includes reviewed actions unless another setting blocks them.
- **Medium** includes reviewed read and normal-write actions.
- **High** includes reviewed read and list actions that do not change data.

Changing the profile or an individual tool setting causes a new runtime synchronization. Wait for the update to show **Applied** before testing again.

## 7. Run one tool

Use [Inspector](../quick-start.md#optional-debug-raw-mcp-behavior-with-mcp-inspector) for a direct call, or use the [Simulator](../simulator/index.md) for a plain-English request. Confirm the outcome in **Reporting**.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| **Add MCP** is disabled | Enable MCP Support in the runtime's Setup tab |
| Connection test fails | Confirm that the runtime is connected and can reach the URL or start the command |
| Docker test fails | Confirm Docker availability and socket sharing on the runtime host |
| No tools are discovered | Check the server command, URL, runtime logs, and MCP transport |
| A discovered tool is missing from the client | Review its classification, protection profile, individual state, and client role |
| Server remains pending | Wait for synchronization, then check the runtime connection and logs |

## What’s next

- [Understand profile-based tool visibility](index.md#how-tool-visibility-works)
- [Review Advanced access controls](advanced.md)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)
