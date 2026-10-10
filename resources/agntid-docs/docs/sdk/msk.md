---
title: Microsoft Semantic Kernel
last_verified: 2026-09-09
owner: sdk-team
---

<div class="page-intro" markdown>

# Microsoft Semantic Kernel

Turn the profile-visible MCP tools from an AgntID runtime into a Semantic Kernel plugin, then let a `ChatCompletionAgent` select and call them.

</div>

This guide uses the Python source version 0.2.0 with Semantic Kernel 1.44.1. The SDK supports Semantic Kernel 1.39 or later within the 1.x line.

## Before you begin

You need:

- Python 3.10 or later
- a healthy AgntID runtime and its MCP address
- at least one business tool visible under the runtime's protection profile
- a model provider key; this example uses OpenAI

If you have not prepared the runtime yet, complete the [Quick Start](../quick-start.md)
through the protected `demo_add_numbers` call before continuing.

Semantic Kernel's current Python agent pattern uses `ChatCompletionAgent`, `KernelArguments`, and automatic function choice. See the [Microsoft agent example](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/examples/example-chat-agent) for the framework's own reference.

## 1. Install the integration

From the `agntid-python` repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[msk]"
```

The `[msk]` extra installs Semantic Kernel. It is not part of the base SDK dependency set.

## 2. Set the environment

=== "macOS or Linux"

    ```bash
    export AGNTID_MCP_URL=http://localhost:8082/mcp
    export OPENAI_API_KEY=your-openai-api-key
    export OPENAI_CHAT_MODEL_ID=gpt-4o
    # Only when Runtime Security requires OAuth client access:
    export AGNTID_ACCESS_TOKEN='<current raw OAuth access token>'
    ```

=== "Windows PowerShell"

    ```powershell
    $env:AGNTID_MCP_URL = "http://localhost:8082/mcp"
    $env:OPENAI_API_KEY = "your-openai-api-key"
    $env:OPENAI_CHAT_MODEL_ID = "gpt-4o"
    # Only when Runtime Security requires OAuth client access:
    $env:AGNTID_ACCESS_TOKEN = "<current raw OAuth access token>"
    ```

Use a model available to your account.

Leave `AGNTID_ACCESS_TOKEN` unset for an approved runtime that allows
unauthenticated access. Do not include the `Bearer` prefix; the SDK adds it at
the MCP transport boundary.

## 3. Copy this complete example

Save as `semantic_kernel_example.py`:

```python title="semantic_kernel_example.py"
import asyncio
import os

import agntid
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import KernelArguments


async def main() -> None:
    mcp_url = os.environ["AGNTID_MCP_URL"]
    model = os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")
    user_id = "user-42"  # Replace with your authenticated user ID.
    prompt = "Add 11 and 22."

    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(ai_model_id=model, service_id="chat")
    )
    settings = kernel.get_prompt_execution_settings_from_service_id("chat")
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="ArithmeticAssistant",
        instructions=(
            "Use an available tool for arithmetic. "
            "If a call is denied, explain the denial and do not bypass it."
        ),
        arguments=KernelArguments(settings=settings),
    )

    async with agntid.AgntidMCPClient(
        mcp_url,
        access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None,
    ) as client:
        tools = await agntid.get_tools_list(client)
        wrapped = agntid.wrap_client(client)

        plugin = agntid.msk.create_plugin_from_mcp_tools(wrapped, tools)
        kernel.add_plugin(plugin, plugin_name="MCPTools")

        agent_id = agntid.msk.agent_id_from_agent(agent)
        task_id = agntid.create_task(agent_id, user_id, prompt)

        async with agntid.task_context(client, task_id):
            ok, message = await agntid.send_task_open_checked(
                client, task_id, agent_id, user_id, prompt
            )
            if not ok:
                raise RuntimeError(f"Task was not accepted: {message}")

            wrapped.set_task_id(task_id)
            async for response in agent.invoke(
                messages=prompt,
                arguments=KernelArguments(settings=settings),
            ):
                print(response.content)

        denial = agntid.get_last_denial(clear=True)
        if denial:
            print(f"Policy: {agntid.format_denial(denial)}")


if __name__ == "__main__":
    asyncio.run(main())
```

## 4. Run it

```bash
python semantic_kernel_example.py
```

The exact response depends on the model. For the default demo policy, the agent should call `demo_add_numbers` and report 33. Confirm the allowed tool call in Reporting.

## How the plugin is built

```python
tools = await agntid.get_tools_list(client)
plugin = agntid.msk.create_plugin_from_mcp_tools(wrapped, tools)
kernel.add_plugin(plugin, plugin_name="MCPTools")
```

The SDK:

1. uses only the tool list returned by the runtime
2. excludes AgntID task, action, and delegation control tools
3. converts MCP input schemas into Semantic Kernel function parameters
4. changes unsupported characters in function names, such as `demo.add_numbers` to `demo_add_numbers`
5. maps the model's function call back to the original MCP tool name

The runtime protection profile therefore affects which tools Semantic Kernel can see. Runtime policies still check the inputs when the agent calls a visible tool.

## Add AgntID to an existing agent

Keep your current Kernel and model setup. Add these four points:

1. Connect through `AgntidMCPClient`.
2. Build and add the plugin from `get_tools_list`.
3. Open one AgntID task for each user prompt.
4. Set the wrapper's task ID before invoking the agent.

If you keep a Semantic Kernel conversation thread, create a new AgntID task for every new user message. The conversation thread may continue, but the task must represent the current request.

## Identity rules

`agent_id_from_agent(agent)` uses the agent name or ID. Semantic Kernel does not provide a trusted end-user identity:

```python
assert agntid.msk.user_id_from_kernel(kernel) is None
```

Set `user_id` from your application's authentication session. Never ask the model to create it.

## Use the repository example

The repository includes an interactive prompt loop:

```bash
python examples/msk/msk_demo.py --check-runtime
python examples/msk/msk_demo.py \
  --agent-name ArithmeticAssistant \
  --user-id user-42
```

It keeps one Semantic Kernel thread but opens a separate AgntID task for each prompt.
The first command proves live tool discovery and MSK plugin construction without
calling a model.

## Common problems

| Problem | Check |
| --- | --- |
| `No module named semantic_kernel` | Install the SDK with `.[msk]`. |
| The agent sees no business tools | Check the protection profile, tool review, individual state, and role access. |
| A dotted MCP name looks different | Semantic Kernel receives a safe name; the SDK maps it back automatically. |
| Model authentication fails | Confirm the provider key and selected model. |
| Runtime authentication returns 401 | Export a current raw `AGNTID_ACCESS_TOKEN` without the `Bearer` prefix. |
| A call is denied | Read the AgntID reason and stop that action; the plugin remains connected. |

## What’s next

- [Run the repository examples](examples.md)
- [Prepare all repository examples](https://github.com/AGNTID-AI/agntid-python/blob/main/examples/README.md)
- [Use LangChain or Deep Agents](langchain.md)
- [Review the MSK API](api-reference.md#microsoft-semantic-kernel)
