---
title: Python SDK API Reference
last_verified: 2026-10-08
owner: sdk-team
---

<div class="page-intro" markdown>

# Python SDK API Reference

Current public classes, functions, result types, and constants in Python source version 0.2.0.

</div>

For complete programs, use the [Python Quick Start](python.md), [Microsoft Semantic Kernel](msk.md), [LangChain and Deep Agents](langchain.md), or [AWS AgentCore](agentcore.md) guide.

## Connection and discovery

| API | Purpose |
| --- | --- |
| `AgntidMCPClient(url, *, access_token=None)` | Async MCP client for open or OAuth-protected AgntID runtime access. Pass the raw token without `Bearer`. |
| `get_tools_list(client)` | Return tools from `list_tools` or `get_tools`, including async clients. |
| `require_env(*names, hint=None)` | Read required environment variables or exit with a clear message. |

```python
import os

async with agntid.AgntidMCPClient(
    mcp_url,
    access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None,
) as client:
    tools = await agntid.get_tools_list(client)
```

## Task lifecycle

| API | Purpose |
| --- | --- |
| `create_task(agent_id, user_id, prompt, *, sender=None, use_tool_call=True, execution_context=None)` | Validate values and create a new task ID. With no sender, this does not contact the runtime. |
| `send_task_open(client, task_id, agent_id, user_id, prompt, *, execution_context=None)` | Send the task-open tool call and return the raw result. |
| `send_task_open_checked(...)` | Open the task and return `(ok, message)`. |
| `send_task_open_details(...)` | Open the task and return `TaskOpenResult`, including intent preparation and the runtime snapshot. |
| `task_context(client, task_id)` | Async context manager that sends task close when the block exits. |
| `send_task_close(client, task_id)` | Send task close and return the raw result. |
| `close_task(task_id, *, sender=None, use_tool_call=True)` | Low-level synchronous message-builder path. |
| `task_open_arguments(...)` | Build the public task-open argument dictionary. |

Use `create_task`, `send_task_open_checked`, and `task_context` for normal async applications.

## Task intent and tool shortlisting

| API | Purpose |
| --- | --- |
| `TaskOpenResult` | Typed task-open outcome with preparation status, counts, reason, and optional snapshot. |
| `TaskIntentSnapshot` | Engine, extracted tasks, constraints, assessments, canonical `relevant_tool_ids`, and exact public `relevant_tool_names` for one task. |
| `parse_task_open_details(result)` | Parse a raw MCP task-open result without discarding its intent payload. |
| `filter_tools_for_task(tools, task_open)` | Intersect profile-visible tools with the task shortlist. A missing snapshot raises `IntentPreparationError`. |
| `IntentPreparationError` | Fail-closed signal that an application must handle before giving tools to a model. |

```python
task_open = await agntid.send_task_open_details(
    client, task_id, agent_id, user_id, prompt
)
task_tools = agntid.filter_tools_for_task(visible_tools, task_open)
```

An empty `task_tools` list can be a valid result for an informational, catalog,
or unsupported request. Do not substitute the original tool list. Filtering is
not authorization; the runtime still evaluates every business call.

`filter_tools_for_task` matches the exact `relevant_tool_names` returned by
current runtimes. It falls back to `relevant_tool_ids` for compatibility with
older runtimes whose canonical IDs already matched their public MCP names.

## Protected client

| API | Purpose |
| --- | --- |
| `wrap_client(client, task_id=None, delegation_id=None, *, task_argument="_task_id", delegation_argument="_delegation_id")` | Return a wrapper that adds task and optional delegation correlation, then removes internal result fields. |
| `wrapped.set_task_id(task_id)` | Change the task used by later calls. |
| `wrapped.set_delegation_id(delegation_id)` | Set or clear the child delegation used by later calls. |
| `wrapped.call_tool_async(name, arguments=None, **kwargs)` | Call a tool through an async client. |
| `wrapped.call_tool(name, arguments=None, **kwargs)` | Call a tool through a synchronous client. |

## Result and denial types

| API | Purpose |
| --- | --- |
| `ToolResult` | Dictionary result with Rich display support. |
| `ToolResultScalar` | Wrapper for a string, number, list, or other non-dictionary result; original value is in `.value`. |
| `DenialResult` | Falsy policy-denial result with `.denied`, `.message`, and `.tool_name`. |
| `get_last_denial(clear=True)` | Return the last captured denial and optionally clear it. |
| `format_denial(denial)` | Convert denial data to readable text. |
| `print_result`, `print_denial`, `print_tools` | Rich terminal output helpers. |
| `print_connected`, `print_task_opened`, `print_error` | Rich status output helpers. |
| `format_tools_display(tools, exclude=())` | Return a plain-text tool list. |

## Microsoft Semantic Kernel

These APIs are in `agntid.msk`. Install Semantic Kernel with `.[msk]`.

| API | Purpose |
| --- | --- |
| `create_plugin_from_mcp_tools(wrapped_client, tools, *, plugin_name="MCPTools", exclude_tool_names=...)` | Build a Semantic Kernel plugin from the current MCP tools. Runtime control tools are excluded by default. |
| `mcp_plugin_for_task(client, task_id, agent_id, user_id, prompt, *, plugin_name="MCPTools", exclude_tool_names=...)` | Open a task, wrap the client, read tools, and return `(plugin, tools, open_result)`. |
| `agent_id_from_agent(agent)` | Use the agent name or ID, with `msk-agent` as the fallback. |
| `user_id_from_kernel(kernel)` | Always returns `None`; the application must supply user identity. |
| `sanitize_tool_name_for_msk(name)` | Replace characters that Semantic Kernel does not accept in function names. |

## Framework context

The base SDK provides framework-neutral value objects. They do not import LangChain.

| Class or function | Purpose |
| --- | --- |
| `FrameworkInfo` | Framework name, adapter version, and supported context features. |
| `ConversationContext` | Bounded summary, active constraints, revoked intent IDs, and entity references. |
| `ExecutionContext` | Root task, agent, thread, conversation, plan, and namespaced extensions. |
| `ExecutionPlan` | Declared plan with ordered actions. |
| `PlannedAction` | Expected tool or response action and its lifecycle state. |
| `DelegatedIntent` | Bounded description of child-agent work. |
| `DelegationContext` | Parent, child, delegated intent, child tool list, and approval evidence. |
| `ApprovalEvidence` | Approval decision bound to an exact operation, tool, and argument digest. |
| `extract_explicit_constraints(*prompts)` | Extract bounded unconditional negative constraints for adapter context. |
| `arguments_digest(arguments)` | Create the stable SHA-256 digest used to bind approval to arguments. |

### LangChain and Deep Agents adapter

Import from `agntid.adapters.langchain_deep_agents`:

| API | Purpose |
| --- | --- |
| `DeepAgentsAdapter.execution_context(event, *, task_id=None, agent_id=None)` | Convert trusted application state into an `ExecutionContext`. |
| `DeepAgentsAdapter.delegation_for_task_call(...)` | Record a Deep Agents `task` delegation before a business tool runs. |
| `DeepAgentsAdapter.delegation_for_request(request, context)` | Resolve and validate child-agent identity, intent, and tool access for a request. |
| `DeepAgentsAdapter.approval_for_request(request, context, policy=None)` | Bind trusted approval evidence to the exact tool and arguments. |
| `DelegationProposal` | Adapter result containing the canonical delegation context. |

The maintained adapter reads framework objects structurally, so importing the base SDK does not install or import LangChain.

## Delegation and action lifecycle

| API | Purpose |
| --- | --- |
| `send_delegation_open(client, task_id, delegation_context)` | Open a child delegation under a task. |
| `send_delegation_close(client, task_id, delegation_id, *, status="completed", reason=None)` | Close a child delegation. |
| `delegation_open_arguments(task_id, delegation_context)` | Build delegation-open arguments. |
| `send_action_update(client, task_id, action_id, status, **details)` | Update a declared plan action. |

These are advanced APIs. The complete Deep Agents example shows the expected ordering and trusted identity boundary.

## Decision parsing

| API | Purpose |
| --- | --- |
| `parse_decision(value)` | Parse a runtime response into `AgntidDecision`, when present. |
| `parse_decision_from_exception(error)` | Parse decision data from a tool exception. |
| `AgntidDecision` | Parsed allow, deny, or review-required decision. |
| `DecisionOutcome` | Decision outcome enumeration. |
| `ReviewDecision`, `ReviewStatus` | Structured human-review state. |

## Constants

| Constant | Value |
| --- | --- |
| `TASK_OPEN_TOOL` | `agntid_task_open` |
| `TASK_CLOSE_TOOL` | `agntid_task_close` |
| `DELEGATION_OPEN_TOOL` | `agntid_delegation_open` |
| `DELEGATION_CLOSE_TOOL` | `agntid_delegation_close` |
| `ACTION_UPDATE_TOOL` | `agntid_action_update` |
| `__version__` | Installed SDK version string |

## Version notes

- Python 3.10 or later is required by the core SDK.
- The LangChain/Deep Agents example uses Python 3.11 and a checked-in lock file.
- Semantic Kernel is an optional dependency: `semantic-kernel>=1.39,<2`.
- OpenAI is an optional dependency: `openai>=2.20,<3`.
