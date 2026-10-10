---
title: LangChain and Deep Agents
last_verified: 2026-09-09
owner: sdk-team
---

<div class="page-intro" markdown>

# LangChain and Deep Agents

Run LangChain agents and Deep Agents with profile-filtered MCP tools, trusted user and agent identity, task correlation, policy checks, and clear execution evidence.

</div>

The repository provides a complete example application because a safe framework integration needs more than a tool wrapper. It must also control identity, task lifecycle, child-agent delegation, and the context sent to AgntID.

## Choose the right example

| Need | Use |
| --- | --- |
| Small agent with tool calling | LangChain `create_agent` |
| Planning, files, memory, and specialist subagents | `create_deep_agent` |
| Check either path without a provider key | `framework-smoke` |
| See task and child-agent correlation | `delegation-smoke` or `ops-chat` |

Deep Agents builds on LangChain's agent runtime and adds a planning and subagent layer. The [official Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview) explains the framework features.

## 1. Get the example

Install [`uv`](https://docs.astral.sh/uv/) first, then run:

```bash
git clone https://github.com/AGNTID-AI/agntid-python.git
cd agntid-python/examples/langchain-deepagents
export AGNTID_MCP_URL=http://localhost:8082/mcp
```

Complete the [Quick Start](../quick-start.md) through the protected
`demo_add_numbers` call first. When Runtime Security requires OAuth client
access, also export the raw access token without a `Bearer` prefix:

```bash
export AGNTID_ACCESS_TOKEN='<current OAuth access token>'
```

The example attaches this token only to the MCP transport. It does not put the
token in prompts, graph state, memory, evidence files, or tool arguments.

`uv run` creates an isolated Python 3.11 environment and installs the versions recorded in `uv.lock`.

## 2. Run LangChain without a model key

```bash
uv run --python 3.11 agntid-poc \
  --agent-id docs-langchain-agent \
  --user-id user-42 \
  framework-smoke --framework langchain --first 11 --second 22
```

This deterministic test still runs the full path:

```text
prompt → LangChain agent → AgntID bridge → runtime policy → demo_add_numbers
```

Expected business result: `33.0` with policy allowed.

## 3. Run Deep Agents without a model key

```bash
uv run --python 3.11 agntid-poc \
  --agent-id docs-deep-agent \
  --user-id user-42 \
  framework-smoke --framework deepagents --first 11 --second 22
```

This uses the same tool and protected runtime path, but constructs the agent with `create_deep_agent`.

## 4. Use a real model

```bash
export OPENAI_API_KEY=your-openai-api-key
export MODEL=openai:gpt-4.1-mini

uv run --python 3.11 agntid-poc \
  --agent-id arithmetic-agent:v1 \
  --user-id user-42 \
  langchain "Please add 11 and 22"
```

Change `langchain` to `deepagents` to run the same request through Deep Agents:

```bash
uv run --python 3.11 agntid-poc \
  --agent-id arithmetic-agent:v1 \
  --user-id user-42 \
  deepagents "Please add 11 and 22"
```

Pass the model explicitly. Use a `provider:model` value supported by your installed LangChain provider.

## What the example protects

The example's `AgntidBridge` performs six important jobs:

1. Loads tools from the AgntID runtime.
2. Removes runtime control tools from the agent-visible list.
3. Hides internal task, delegation, and approval arguments from the model.
4. Overwrites model-supplied identity values with trusted application context.
5. Opens and closes an AgntID task around each user request.
6. Sends the result, policy decision, task ID, and correlation ID to the example's display layer.

The bridge is example application code, not a public `agntid` class. Copy its pattern when adapting another LangChain application.

## Tool visibility and least privilege

The runtime returns only tools available under its protection profile and other access controls. The example narrows that list again:

```python
tools = bridge.agent_tools({"demo_add_numbers"})
```

The runtime profile is the main availability boundary. A framework allowlist is an additional restriction for that agent; it cannot make a hidden tool visible or bypass runtime policy.

## Trusted request context

The example passes an `InvocationContext` as trusted graph context:

```python
context = InvocationContext(
    agent_id="arithmetic-agent:v1",
    user_id="user-42",
    prompt="Please add 11 and 22",
)
```

In a real service:

- load `agent_id` from deployment configuration
- load `user_id` from verified authentication
- use the current user message as `prompt`
- never let model output replace these values

The SDK's `DeepAgentsAdapter` turns this application context into a framework-neutral `ExecutionContext`. Raw model reasoning and memory files are not sent to AgntID.

## Multi-agent delegation

The operations example maps each specialist to one agent identity and a narrow tool list. Before running it, the current profile must expose:

- `demo_add_numbers`
- `demo_get_ticket`
- `demo_send_notification`
- `demo_schedule_job`
- `demo_export_payroll_records`

Run the interactive example:

```bash
uv run --python 3.11 agntid-poc \
  --agent-id service-operations-supervisor:v1 \
  --user-id user-42 \
  ops-chat
```

Try a non-mutating request first:

```text
Get the status and severity of LIVE-TKT-900. Add 11 and 22 for responder capacity. Do not send notifications.
```

The example creates separate delegation records for the ticket and calculation specialists. Sensitive operations can pause for human review before the tool call continues.

If the profile hides any of the five configured tools, startup stops with a list of missing tools. Use the simpler `framework-smoke` when you want a test that needs only `demo_add_numbers`.

## Important source files

| File | Purpose |
| --- | --- |
| `runners.py` | Builds the small LangChain and Deep Agents examples. |
| `bridge.py` | Connects framework tool calls to AgntID tasks and policies. |
| `operations_agent.py` | Defines the supervisor and least-privilege specialists. |
| `identity.py` | Holds trusted application identity and request context. |
| `adapter.py` | Re-exports the SDK's maintained Deep Agents adapter. |

All files are under `examples/langchain-deepagents/src/agntid_deepagents_poc/` in the [agntid-python repository](https://github.com/AGNTID-AI/agntid-python/tree/main/examples/langchain-deepagents).

## Run the tests

```bash
uv run --python 3.11 --extra dev pytest -q
```

The tests cover adapter context, identity overwrite, tool filtering, task and delegation lifecycle, execution plans, approval pauses, result parsing, and the CLI.

## Common problems

| Problem | Check |
| --- | --- |
| Connection attempts fail | Confirm `AGNTID_MCP_URL` is reachable from the process. |
| `demo_add_numbers` is missing | Review the profile, classification, tool state, and roles. |
| Operations example lists missing tools | Its five-tool graph needs more tools than the basic smoke test. |
| Model package or key is missing | Use `framework-smoke`, or configure the selected model provider. |
| Runtime authentication returns 401 | Export a current raw `AGNTID_ACCESS_TOKEN` issued for the AgntID protected resource. |
| A child call has no trusted policy | Add an application-owned delegation policy; do not infer it from the prompt. |
| A tool call is denied | Use the shown policy and correlation evidence; do not retry to bypass it. |

## What’s next

- [Run all Python examples](examples.md)
- [Prepare all repository examples](https://github.com/AGNTID-AI/agntid-python/blob/main/examples/README.md)
- [Review framework context APIs](api-reference.md#framework-context)
- [Review tool visibility](../mcp/index.md#how-tool-visibility-works)
