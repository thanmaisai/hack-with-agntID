---
title: Python SDK Guide
last_verified: 2026-10-08
owner: sdk-team
---

<div class="page-intro" markdown>

# Python SDK Guide

Use one clear pattern for every agent request: connect, open a task, call protected tools, handle the result, and close the task.

</div>

Run the [Python Quick Start](python.md) first if you have not yet completed a protected tool call.

## How a request moves through AgntID

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/sdk-request-flow.svg" alt="SDK request flow from a user request through task open, profile-filtered tool selection, runtime policy check, MCP execution, result or denial, and task close" />
  <img class="diagram-dark" src="../../assets/diagrams/sdk-request-flow-dark.svg" alt="SDK request flow from a user request through task open, profile-filtered tool selection, runtime policy check, MCP execution, result or denial, and task close" />
</div>

## The recommended pattern

```python
task_id = agntid.create_task(agent_id, user_id, prompt)
wrapped = agntid.wrap_client(client, task_id)

async with agntid.task_context(client, task_id):
    ok, message = await agntid.send_task_open_checked(
        client, task_id, agent_id, user_id, prompt
    )
    if not ok:
        raise RuntimeError(message)

    result = await wrapped.call_tool_async(tool_name, arguments)
```

Use this block once for each new user request. If an agent calls several tools for the same request, reuse the same task ID inside the block.

## Bind the prompt-aware shortlist before model planning

When a framework or custom model loop accepts a tool list, retain the detailed
task-open result and narrow the already profile-visible tools before the first
model call:

```python
visible_tools = await agntid.get_tools_list(client)
task_id = agntid.create_task(agent_id, user_id, prompt)
wrapped = agntid.wrap_client(client, task_id)

async with agntid.task_context(client, task_id):
    task_open = await agntid.send_task_open_details(
        client, task_id, agent_id, user_id, prompt
    )
    if not task_open.ok:
        raise RuntimeError(task_open.reason)

    task_tools = agntid.filter_tools_for_task(visible_tools, task_open)
    # Convert only task_tools into your framework's tool definitions.
    answer = await run_agent(prompt=prompt, tools=task_tools, client=wrapped)
```

`filter_tools_for_task` fails closed when the runtime did not prepare an intent
snapshot. A valid empty shortlist remains empty; do not replace it with the
broader profile-visible list. The shortlist reduces what the model can choose,
while runtime policy still authorizes every actual call and its arguments.

The snapshot also exposes `engine_id`, extracted `tasks`, `constraints`, tool
assessments, canonical `relevant_tool_ids`, and exact MCP
`relevant_tool_names`. Use these fields for developer diagnostics; use AgntID
Reporting for authoritative execution and policy evidence.

## Connect and discover tools

```python
import os

async with agntid.AgntidMCPClient(
    mcp_url,
    access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None,
) as client:
    tools = await agntid.get_tools_list(client)
```

Use the raw OAuth access token only when Runtime Security requires client
authentication. The transport adds the bearer scheme; do not place the token in
prompts, tool arguments, model state, or committed configuration.

The returned list is already filtered by the runtime. A tool can be absent because of the protection profile, review state, individual tool setting, or role access. Never assume that every server tool will appear.

Each tool object normally provides:

- `name`
- `description`
- `inputSchema`

Use the exact returned name and the argument names in `inputSchema`.

## Set trusted identity

```python
agent_id = "support-assistant:v1"
user_id = authenticated_user.subject
```

- Set `agent_id` from trusted application or deployment configuration.
- Set `user_id` from the authenticated user or service identity.
- Do not take either value from the user's prompt.
- Use a stable opaque user ID rather than an email address or other personal data.

Microsoft Semantic Kernel has no built-in end-user identity. Your application must still supply `user_id`. The same rule applies to LangChain and Deep Agents.

## Create and open a task

`create_task` validates the identifiers and creates a task ID locally. It does not contact the runtime unless you supply a low-level sender.

```python
task_id = agntid.create_task(agent_id, user_id, prompt)
ok, message = await agntid.send_task_open_checked(
    client, task_id, agent_id, user_id, prompt
)
```

Stop the run if `ok` is `False`. A tool call without an accepted task should not continue.

## Call through the wrapped client

```python
wrapped = agntid.wrap_client(client, task_id)
result = await wrapped.call_tool_async(
    "demo_add_numbers",
    {"first_number": 11, "second_number": 22},
)
```

The wrapper adds the task correlation value, sends the call through the runtime, and removes internal `__agntid_*` fields from a successful response.

For a prompt loop, create the wrapper once and change its task before each run:

```python
wrapped = agntid.wrap_client(client)

# For each user prompt:
wrapped.set_task_id(task_id)
```

## Handle success and denial

```python
result = await wrapped.call_tool_async(tool_name, arguments)

if getattr(result, "denied", False):
    print(result.message)
    denial = agntid.get_last_denial(clear=True)
    if denial:
        print(agntid.format_denial(denial))
else:
    print(result)
```

| Result | Use |
| --- | --- |
| `ToolResult` | Dictionary result; access values with normal keys. |
| `ToolResultScalar` | String, number, or list result; access the original value with `.value`. |
| `DenialResult` | Policy denial; `.denied` is `True`, `.message` explains why, and its Boolean value is false. |

A denial is a valid security outcome. Show the reason to the user and stop that action. Do not silently change the tool or arguments to obtain an allow result.

## Always close the task

```python
async with agntid.task_context(client, task_id):
    # Open the task and run the agent.
    ...
```

`task_context` sends `task_close` when the block exits, including after an exception. This lets the runtime finish its audit record.

## Framework choices

| Integration | Use it when | Installation |
| --- | --- | --- |
| Core SDK | Your code selects and calls tools | `python -m pip install -e .` |
| Microsoft Semantic Kernel | A `ChatCompletionAgent` should select tools | `python -m pip install -e ".[msk]"` |
| LangChain | You use `create_agent` and want a small agent | Use the pinned example environment |
| Deep Agents | You need planning, memory, or specialist subagents | Use the pinned example environment |
| AWS AgentCore | The LangGraph agent runs locally or in AWS and acts with a user's OAuth access | Use the complete `examples/agentcore` project |

See the complete [Microsoft Semantic Kernel](msk.md), [LangChain and Deep Agents](langchain.md), and [AWS AgentCore](agentcore.md) guides.

## Advanced framework context

Source version 0.2.0 adds framework-neutral context objects such as `ExecutionContext`, `ExecutionPlan`, `PlannedAction`, and `DelegationContext`. The LangChain/Deep Agents example uses them to describe bounded conversation context, expected actions, child-agent work, and approval evidence.

Most direct and Semantic Kernel integrations do not need to create these objects. Use them only when your framework adapter has trusted context to send.

## Production checklist

- Keep the runtime address in configuration.
- Take agent and user identity from trusted sources.
- Open one task for every user request.
- Call every MCP tool through the protected client or framework bridge.
- Treat the returned tool list as the current available set.
- Handle denials as normal outcomes.
- Close tasks even when agent execution fails.
- Review allowed and denied calls in Reporting.

## What’s next

- [Copy a complete example](examples.md)
- [Microsoft Semantic Kernel guide](msk.md)
- [LangChain and Deep Agents guide](langchain.md)
- [API Reference](api-reference.md)
