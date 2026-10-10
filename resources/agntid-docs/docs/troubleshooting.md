---
title: Troubleshooting
last_verified: 2026-09-04
owner: support-team
---

<div class="page-intro" markdown>

# Troubleshooting

Find the first part of the AgntID path that is not working, complete its checks, and then test again. Start with runtime health because Setup, tool access, Inspector, and Simulator all depend on a connected runtime.

</div>

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/troubleshooting-path.svg" alt="Troubleshooting path from Docker services and runtime connection through Setup, MCP access, testing, and Reporting" />
  <img class="diagram-dark" src="../assets/diagrams/troubleshooting-path-dark.svg" alt="Troubleshooting path from Docker services and runtime connection through Setup, MCP access, testing, and Reporting" />
</div>

## Start with these checks

Run these commands from the directory that contains `docker-compose.yml`:

```bash
docker compose ps
docker compose logs --tail=100
docker compose config --images
```

Confirm that:

- `achr-runtime` and `achr-intent-parser` are running and healthy
- the local runtime UI opens at [http://localhost:8080](http://localhost:8080)
- the local runtime UI shows **Operational** and **Connected**
- the images shown by the last command use the expected release

The intent parser downloads an approximately 900 MB model on first start. It may remain in its startup period for several minutes. Check its logs before restarting it.

## A service does not start

| What you see | What to do |
| --- | --- |
| Image pull is denied | Confirm that Docker can reach `ghcr.io` over HTTPS and that the Compose file uses the published AgntID image references. The public runtime images do not require a registry login. |
| Registry certificate error | If your network performs TLS inspection, install its trusted CA certificate for Docker and retry. Do not disable TLS verification as a permanent fix. |
| `achr-intent-parser` is starting | Allow the first model download to finish. Check network access, available memory, and free disk space. |
| A service is unhealthy | Run `docker compose logs --tail=200 achr-runtime achr-intent-parser` and start with the first reported error. |
| Port 8080 or 8082 is already used | Stop the conflicting service, or start AgntID with different host ports as shown below. |
| The host is low on resources | Make approximately 4 GB RAM and 5 GB free disk space available, then restart the stack. |

To use different host ports:

```bash
RUNTIME_PORT=18081 MCP_PORT=18082 docker compose -p agntid-runtime-2 up -d
```

Open `http://localhost:18081` for this example. Use port `18082` in MCP client configuration generated for this runtime.

## The runtime does not connect

| What you see | What to check |
| --- | --- |
| The local runtime UI does not open | Confirm that `achr-runtime` is healthy and that its host port is correct in `docker compose ps`. |
| The bootstrap token is rejected | In the [AgntID portal](https://app.agntid.ai/), open **Runtimes → Add Runtime** and create a fresh token. Copy it exactly and use it only in the local runtime UI. |
| Connection times out | Confirm outbound HTTPS, DNS, proxy settings, and the host's date and time. Then review the runtime logs. |
| The local UI is Operational but the portal shows Offline | Refresh the runtime page. If it remains Offline, confirm outbound access and look for connection errors in the runtime logs. |

Do not share a bootstrap token in a screenshot, ticket, chat, or log bundle.

## Setup does not reach 5 of 5

Open the runtime's **Setup** tab and work on the first incomplete row.

| Setup row | What to check |
| --- | --- |
| Runtime Registered | Reconnect with a fresh bootstrap token. |
| Runtime Healthy | Confirm both Compose services are healthy and the portal shows the runtime online. |
| MCP Support | Enable MCP Support and save the runtime configuration. |
| CLI Enforcement | This is optional and can remain off. It does not block Quick Start completion. |
| Protection Profile | Review the selected profile, mark it reviewed, and wait for **Runtime sync: Applied**. |

If synchronization remains **Pending** or **Failed**, confirm that the runtime is connected, review its logs, and wait for the next synchronization. Test tools only after the latest change shows **Applied**.

## A tool is missing

The protection profile sets the largest tool list available from the runtime. Check the tool in **Access Control → Tools**:

1. Confirm that discovery completed and the action was reviewed.
2. Confirm that its action type is included in the selected protection profile.
3. Confirm that the tool and its MCP server are enabled.
4. If OAuth is required, confirm that the signed-in user's role grants include the action.
5. Wait for runtime synchronization to show **Applied**.
6. Reconnect the MCP client and list tools again.

A policy can place limits on a visible tool call. It cannot make a tool visible when the protection profile has excluded it.

## A tool call is denied

Open **Reporting** or **Operations → MCP → Access Dashboard** and find the event for the call. Check the tool name, input values, protection profile, policy result, verified identity, and role grants.

Common causes are:

- an input value is outside the policy's allowed range
- the effective policy blocks the action
- the protection profile changed after the client received its tool list
- an OAuth role does not have the required operation grant
- the client sent different input names or values than expected

Use the event's correlation ID when comparing the client result with runtime logs. Do not bypass a denial by turning off protection; correct the profile, policy, role, or request that caused it.

## An MCP server cannot be added

| What you see | What to check |
| --- | --- |
| **Add MCP** is unavailable | Enable **MCP Support** in the runtime's **Setup** tab. |
| A remote HTTP test fails | Confirm the URL and transport. The address must be reachable from the runtime container, not only from the host browser. |
| A local command fails | Check the command, put each argument on its own line, and confirm required environment variables are available to the runtime. |
| A Docker server fails | Confirm Docker socket sharing and permissions. Enable this only for a trusted deployment. |
| No tools are discovered | Check the server logs, transport, start command, and server response. |
| Apply remains pending | Confirm the runtime is connected and wait for synchronization. Then check runtime logs. |

Inside a container, `localhost` means that container. Use a network address the runtime container can reach when the MCP server runs elsewhere.

See [Add an MCP server](mcp/attach-server.md) for supported connection styles and credential choices.

## OAuth client access does not work

First identify which connection is failing:

- **Client access** is the connection from Cursor, Claude, Codex, or another MCP client to the AgntID runtime.
- **Server authentication** is the separate connection from the runtime to an external MCP server.

For client access, confirm that the OAuth credential is **VALID**, the MCP Server Address is the runtime's base address, and the provider allows the client's callback address and requested scopes. If sign-in succeeds but no tools appear, check the protection profile, verified roles, and role grants.

Simulator is unavailable while OAuth client access is required. Inspector can test a tool directly, but it does not prove that an external client's OAuth flow works. Test OAuth with the client people will use. See [Protect MCP access with OAuth](mcp/oauth.md).

## Simulator does not run

| What you see | What to check |
| --- | --- |
| No runtime is listed | Enable **Simulation System**, save the runtime configuration, and confirm the runtime is Active and Healthy. |
| No AI model credential is listed | Add one under **Access Control → Credentials** and confirm that it is Healthy. |
| Connection fails | Check the runtime, selected credential, and whether OAuth client access is required. Then reconnect. |
| A different tool runs | Name the tool in the request when you need a repeatable test. |
| The expected denial does not occur | Confirm the policy inputs and wait for runtime synchronization to show **Applied**. |
| The session expired | Select **Connect** to create a new session. |

Remember that an allowed Simulator request runs the real tool. Use test tools and test data. See [Simulator](simulator/index.md).

## Sign-in problems

| What you see | What to do |
| --- | --- |
| The sign-in page does not open | Open the [AgntID portal](https://app.agntid.ai/). For a custom instance, confirm its portal address with your administrator. |
| Sign-in redirects repeatedly | Close other AgntID sign-in tabs, clear site cookies, and try again. |
| Authentication succeeds but access is missing | Ask an administrator to check your organization membership and assigned plan or role, then sign in again. |
| MFA fails | Check the device time and authenticator setup, or ask an administrator to reset MFA. |

## Collect information for support

Include:

- the time of the problem and your time zone
- the runtime name and product release
- the step that failed and the exact error message
- output from `docker compose ps`
- the relevant service logs around the failure
- the Reporting correlation ID for a failed tool call
- Docker and Docker Compose versions

Review all output before sharing it. Remove bootstrap tokens, OAuth tokens, client secrets, API keys, personal data, and unrelated events.

```bash
docker version
docker compose version
docker compose ps
docker compose logs --tail=200 achr-runtime achr-intent-parser
docker compose config --images
```

## Related guides

- [Quick Start](quick-start.md)
- [Add an MCP server](mcp/attach-server.md)
- [Connect Cursor, Claude, or Codex](mcp/connect-clients.md)
- [Protect MCP access with OAuth](mcp/oauth.md)
- [Simulator](simulator/index.md)
