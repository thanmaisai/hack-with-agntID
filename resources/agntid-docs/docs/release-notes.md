---
title: Release Notes
last_verified: 2026-09-09
owner: release-team
---

<div class="page-intro" markdown>

# Release Notes

See the latest customer-facing changes to the AgntID runtime, portal guidance, MCP workflows, Simulator, and SDK documentation.

</div>

## 2026-09-07

### AWS AgentCore example

- The public Python SDK repository now includes a complete Amazon Bedrock AgentCore Runtime and LangGraph project.
- OAuth access and stable user identity use dedicated AgentCore custom headers and remain outside model context.
- The application intersects profile-visible tools with an operator allowlist, opens and closes one AgntID task per invocation, and hides internal correlation arguments from the model.
- Fourteen automated tests run without AWS credentials, an AWS account, an AgntID runtime, or a model provider.
- A disabled-by-default direct smoke can exercise a local AgntID runtime without calling an LLM.
- AgentCore CLI `0.28.1` validates the project and produces a deployable CodeZip containing the source SDK checkout.
- The Python repository now provides one shared runtime/bootstrap guide and
  model-free readiness checks for MSK, LangChain/Deep Agents, and AgentCore.
- The core SDK and framework examples accept an optional OAuth access token at
  the MCP transport boundary without adding it to model context.

See [AWS AgentCore](sdk/agentcore.md).

## 2026-09-04

### Runtime 2.0.0 and protection profiles

- The customer runtime Compose file now uses `achr-runtime:2.0.0` and `achr-intent-parser:2.0.0` by default.
- Runtime setup now guides users through five checks: registration, health, MCP support, optional CLI enforcement, and protection profile review.
- Protection profiles control which reviewed tools are available. Medium includes normal read and write actions, while destructive and high-impact actions remain excluded.
- A baseline allow policy permits eligible reviewed tools. More detailed policies can limit inputs or block individual calls.
- Runtime Operations provides connection state, activity, metrics, configuration, security, and audit information after setup.

See the updated [Quick Start](quick-start.md).

### MCP servers and clients

- MCP servers are now added and configured in the AgntID portal instead of the local runtime UI.
- The MCP guides cover local processes, remote HTTP servers, Streamable HTTP, Server-Sent Events (SSE), headers, environment variables, and supported credential modes.
- New client guidance shows where to copy the current configuration for Cursor, Claude, and Codex.
- New OAuth guidance separates client-to-runtime authentication from runtime-to-server credentials.
- Tool lists are filtered by the runtime protection profile, tool review state, individual settings, and any verified role grants.

Start with [Use MCP with AgntID](mcp/index.md).

!!! note "OAuth client validation"

    The current portal and runtime setup is documented. Complete OAuth sign-in, tool-list, tool-call, and reporting tests for Cursor, Claude, and Codex are still pending. Each client remains marked unverified until its full flow passes.

### Simulator

- The Simulator guide now follows the current portal flow for enabling simulation, selecting an AI credential, connecting a runtime, and running plain-English requests.
- It includes repeatable allowed and denied `demo.add_numbers` examples.
- Results, logs, call flow, audit evidence, metrics, and saved simulation history are explained with current screenshots.

See [Simulator](simulator/index.md).

### Python SDK and framework examples

- The Python guides now match source version `0.2.0`, including task lifecycle, clean results, denials, trusted identity, execution context, delegation, actions, and approvals.
- Microsoft Semantic Kernel documentation now uses the current plugin and `ChatCompletionAgent` pattern.
- New LangChain and Deep Agents documentation includes deterministic tests that do not need a model-provider key, plus interactive and multi-agent examples.
- Runtime control tools are excluded from the Semantic Kernel plugin by default.
- The direct smoke example now uses `demo_add_numbers` with `first_number` and `second_number`.
- An AWS AgentCore architecture preview was added; it was replaced by the runnable example and guide on 2026-09-07.

See [Use the AgntID SDK](sdk/index.md).

!!! important "SDK package availability"

    Version `0.2.0` is available from the source repository but is not yet the published GitHub wheel. The latest published wheel remains `0.1.1`. Follow the source-install steps when using the new adapters.

### Documentation experience

- The Home page now gives a shorter product overview and clearer routes into the main guides.
- Quick Start, Simulator, MCP, and SDK pages now use simpler English, current screenshots, and responsive light/dark diagrams.
- Product terms now distinguish the **AgntID portal**, **local runtime UI**, and **AgntID runtime**.

## 2026-03-05

- The first end-to-end Quick Start was published for the original runtime and policy flow. It has since been replaced by the [runtime 2.0.0 Quick Start](quick-start.md).

## 2026-02-20

- The AgntID user documentation site was initialized.
