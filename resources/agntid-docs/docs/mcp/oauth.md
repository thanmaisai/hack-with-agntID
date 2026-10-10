---
title: Protect MCP Access with OAuth
last_verified: 2026-09-04
owner: docs-team
---

<div class="page-intro" markdown>

# Protect MCP Access with OAuth

Require people and agents to sign in before they connect an MCP client to the AgntID runtime. The runtime verifies the OAuth token and can use the verified identity and roles when deciding which tools to show.

</div>

!!! warning "Direct-client validation is still pending"
    The portal and runtime steps on this page match the current product. End-to-end OAuth tests for Cursor, Claude, and Codex are still pending. Treat each client as unverified until its complete sign-in, tool-list, tool-call, and reporting flow passes.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/mcp-oauth-flow.svg" alt="OAuth flow from an MCP client and identity provider to the AgntID runtime, followed by a separately authenticated connection to an external MCP server" />
  <img class="diagram-dark" src="../../assets/diagrams/mcp-oauth-flow-dark.svg" alt="OAuth flow from an MCP client and identity provider to the AgntID runtime, followed by a separately authenticated connection to an external MCP server" />
</div>

## Before you begin

You need:

- a working identity provider, such as Keycloak or Auth0
- an OAuth client created for MCP access
- the provider URL, realm or tenant, client ID, and client secret
- the base address where MCP clients reach the runtime
- the callback addresses required by the MCP clients you plan to use

Provider setup differs between products. Confirm the required redirect addresses and scopes with your identity provider administrator.

!!! important "Simulator cannot be used while OAuth is required"
    The runtime currently turns off Simulation when OAuth client access is enabled. Use Cursor, Claude, or Codex to test OAuth. Inspector is useful for direct tool testing, but an Inspector result is not proof that an external client's OAuth login works.

## 1. Create the OAuth credential

1. Open **Access Control → Credentials**.
2. Select **Add Credential** and choose **OAuth Client**.
3. Enter a clear name and the identity provider details.
4. Enter the **MCP Server Address** as the base address only.

    For example, if clients connect to `https://runtime.example.com/mcp`, enter:

    ```text
    https://runtime.example.com
    ```

5. Add the required scopes. Keep `mcp:tools` and any identity or role scopes required by your provider.
6. Save the credential.
7. Open it and select **Test Connection**.
8. Continue only when the OAuth validation status is **VALID**.

The MCP Server Address is important when the identity provider and runtime use different hosts. Leaving it blank makes AgntID assume that both use the provider host.

## 2. Require OAuth on the runtime

1. Open **Runtimes** and select the runtime.
2. Open **Operations → Security**.
3. Under **Client Access**, select the validated OAuth credential.
4. Select **Require OAuth** and confirm.
5. Wait for the runtime proxy to restart and show **Authenticated**.

The example below shows Client Access before a validated credential is selected. After you select one, **Require OAuth** becomes available.

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/06-require-oauth.png" alt="Runtime Security page before a validated credential is selected, with Client Access unauthenticated and Require OAuth unavailable" />
</div>

This setting protects incoming MCP client connections. It does not configure credentials used by the runtime to reach an external MCP server.

## 3. Connect and sign in

1. Open **Operations → MCP → Clients**.
2. Generate the configuration for the client you want to test.
3. Add the configuration to Cursor, Claude, or Codex.
4. Start the client's sign-in flow.
5. Complete sign-in with a test user that has the expected roles.
6. List tools and run one safe tool.

For Codex, start sign-in with:

```bash
codex mcp login agntid
```

Test each client separately. A successful login in one client does not confirm support in another.

## 4. Verify the identity and access

Open **Runtimes → Runtime → Operations → MCP → Access Dashboard**.

The example below shows the dashboard before OAuth is enabled. **Open auth** means that role filtering is bypassed. After you enable OAuth, this must change to the configured authentication mode.

<div class="quick-start-screenshot">
  <img src="../../assets/mcp-2/07-access-dashboard.png" alt="MCP Access Dashboard before OAuth is enabled, showing Open auth and the areas used to review scope, actors, role grants, and access events" />
</div>

After the direct client test, confirm:

- **Auth Mode** shows OAuth authentication.
- The recent actor is marked as a verified OAuth client.
- The expected roles are present.
- The current visible-tool count matches the profile and role grants.
- The tool call appears with the expected result.

Events marked **Reported MCP client** contain a name supplied by the client. Events marked **Verified OAuth client** contain an identity verified from the OAuth token.

## Role-based tool access

The protection profile creates the maximum tool set for the runtime. OAuth role grants can reduce that set for a signed-in user; they cannot make a tool available when the protection profile has already excluded it.

Use **MCP → Access Dashboard → Role Operation Grants** to review or change which operation types each role can use. Test with a non-production user before applying role changes broadly.

## External server authentication

OAuth client access ends at the AgntID runtime. The runtime may use a different method when it calls the external MCP server:

- no authentication
- a bearer token
- a static key in a header
- OAuth token passthrough

Configure that method on the MCP server entry. See [Server credentials](attach-server.md#server-credentials).

## Troubleshooting

| Problem | What to check |
| --- | --- |
| OAuth credential is not listed in Runtime Security | Open the credential and confirm its validation status is VALID |
| Login succeeds but the MCP connection fails | Confirm the MCP Server Address is the runtime base address, without `/mcp` |
| Client reports an issuer error | Compare the issuer returned by provider metadata with the issuer expected by the client |
| User signs in but sees no tools | Check the protection profile, action review, verified roles, and role grants |
| Simulator is unavailable | This is expected while OAuth client access is enabled |
| Inspector works but a client fails | Test the client's OAuth discovery, callback, scopes, and logs; Inspector uses a different connection path |

## Disable OAuth only for planned testing

If you select **Allow Unauthenticated Access**, the runtime proxy restarts and accepts MCP clients without tokens. Use this only in an approved test environment. Re-enable OAuth before normal use.

## What’s next

- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Review profile-based tool visibility](index.md#how-tool-visibility-works)
- [Troubleshooting](../troubleshooting.md)
