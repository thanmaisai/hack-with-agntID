---
title: Python SDK Quick Start
last_verified: 2026-09-09
owner: sdk-team
---

<div class="page-intro" markdown>

# Python SDK Quick Start

Connect to an AgntID runtime and run the protected `demo_add_numbers` tool. This first test uses no AI model and needs no model API key.

</div>

## Before you begin

You need:

- Python 3.10 or later
- a healthy, connected AgntID runtime
- its MCP address, usually `http://localhost:8082/mcp`
- `demo_add_numbers` visible under the runtime's protection profile

If the tool is missing, review [how tool visibility works](../mcp/index.md#how-tool-visibility-works).

## 1. Get the current SDK

The new framework APIs are in source version 0.2.0. Use the current checkout until the 0.2.0 wheel is published.

```bash
git clone https://github.com/AGNTID-AI/agntid-python.git
cd agntid-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## 2. Set the runtime address

=== "macOS or Linux"

    ```bash
    export AGNTID_MCP_URL=http://localhost:8082/mcp
    ```

=== "Windows PowerShell"

    ```powershell
    $env:AGNTID_MCP_URL = "http://localhost:8082/mcp"
    ```

Use an address reachable from the machine that runs this script.

If Runtime Security requires OAuth client access, also export the current raw
access token without the `Bearer` prefix:

```bash
export AGNTID_ACCESS_TOKEN='<current OAuth access token>'
```

## 3. Save this program

Create `quickstart.py` in the repository root:

```python title="quickstart.py"
import asyncio
import os

import agntid


async def main() -> None:
    mcp_url = os.environ["AGNTID_MCP_URL"]
    agent_id = "quick-start-agent"
    user_id = "quick-start-user"
    prompt = "Add 11 and 22"

    async with agntid.AgntidMCPClient(
        mcp_url,
        access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None,
    ) as client:
        tools = await agntid.get_tools_list(client)
        tool_names = {tool.name for tool in tools}
        if "demo_add_numbers" not in tool_names:
            raise RuntimeError(
                "demo_add_numbers is not available. Review the runtime profile."
            )

        task_id = agntid.create_task(agent_id, user_id, prompt)
        wrapped = agntid.wrap_client(client, task_id)

        async with agntid.task_context(client, task_id):
            ok, message = await agntid.send_task_open_checked(
                client, task_id, agent_id, user_id, prompt
            )
            if not ok:
                raise RuntimeError(f"Task was not accepted: {message}")

            result = await wrapped.call_tool_async(
                "demo_add_numbers",
                {"first_number": 11, "second_number": 22},
            )

            if getattr(result, "denied", False):
                print(result)
                raise SystemExit(1)

            print(f"Result: {result['result']}")


if __name__ == "__main__":
    asyncio.run(main())
```

## 4. Run it

```bash
python quickstart.py
```

Expected result:

```text
Result: 33.0
```

You should also see an allowed event in **Reporting**. The exact task and correlation IDs are different for every run.

## What the code did

1. `AgntidMCPClient` connected to the runtime.
2. `get_tools_list` confirmed that the profile allows the tool to be shown.
3. `create_task` created an ID for this user request.
4. `send_task_open_checked` sent the agent, user, and request to the runtime.
5. `wrap_client` linked the tool call to the task and removed internal result fields.
6. `task_context` closed the task, including when an error occurred.

## Common problems

| Problem | Check |
| --- | --- |
| Connection refused | Confirm the runtime is healthy and the MCP address is reachable. |
| `demo_add_numbers` is missing | Review the runtime profile, tool classification, individual tool state, and role access. |
| Task was not accepted | Confirm the runtime and SDK are compatible, then review runtime logs. |
| The call is denied | Read the policy reason in the output and in Reporting. Do not retry with changed values unless the user asked for them. |

## What’s next

- [Understand the core integration pattern](python-guide.md)
- [Use Microsoft Semantic Kernel](msk.md)
- [Use LangChain or Deep Agents](langchain.md)
- [Choose another runnable example](examples.md)
