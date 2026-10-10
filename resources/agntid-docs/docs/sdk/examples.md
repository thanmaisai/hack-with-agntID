---
title: Python SDK Examples
last_verified: 2026-10-08
owner: sdk-team
---

<div class="page-intro" markdown>

# Python SDK Examples

Start with a test that needs no model key. Then choose the framework that matches your application.

</div>

## Example map

| Example | Model key | Main tool requirement | Run |
| --- | --- | --- | --- |
| Core SDK smoke test | No | `demo_add_numbers` | `python examples/direct/direct_tool_call.py` |
| Intent shortlist smoke test | No | `demo_add_numbers` and task intent enabled | `python examples/direct/intent_shortlist.py` |
| OpenAI function-calling agent | Yes | Prompt-dependent | `python examples/fastmcp/openai_demo.py` |
| LangChain smoke test | No | `demo_add_numbers` | `agntid-poc framework-smoke --framework langchain` |
| Deep Agents smoke test | No | `demo_add_numbers` | `agntid-poc framework-smoke --framework deepagents` |
| Microsoft Semantic Kernel chat | Yes | At least one visible business tool | `python examples/msk/msk_demo.py` |
| Interactive operations Deep Agent | Yes | Five operations demo tools | `agntid-poc ops-chat` |
| AWS AgentCore contract tests | No | In-memory MCP double | `cd examples/agentcore && make test` |
| AWS AgentCore direct smoke | No AWS or model | Local `demo_add_numbers` | [Run the AgentCore guide](agentcore.md) |

All examples connect to the tool list returned by the runtime. A protection profile can hide tools that the example expects.

Coding assistants should read the repository's
[`AGENTS.md`](https://github.com/AGNTID-AI/agntid-python/blob/main/AGENTS.md)
before changing an integration. It records the trusted-identity, task lifecycle,
shortlist, wrapped-call, and OAuth boundaries in a compact form.

For a new checkout, start with the repository's
[shared runtime and framework setup](https://github.com/AGNTID-AI/agntid-python/blob/main/examples/README.md).
It covers runtime 2.0.0 startup, bootstrap registration, profile review, open
or OAuth-protected MCP access, a direct protected call, and model-free readiness
checks for the maintained framework paths.

## 1. Core SDK smoke test

```bash
git clone https://github.com/AGNTID-AI/agntid-python.git
cd agntid-python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
export AGNTID_MCP_URL=http://localhost:8082/mcp
python examples/direct/direct_tool_call.py
```

Expected output:

```text
Connected to runtime
Discovered 23 tools
Tool call successful
```

The tool count depends on the current profile and configuration. Success means the client connected, opened a task, ran a protected business tool, and closed the task.

## 2. Inspect prompt-aware intent without a model

Enable the intended runtime intent mode, then run:

```bash
python examples/direct/intent_shortlist.py
```

The example opens this task:

```text
Add 11 and 22. Do not send any notification.
```

It prints the selected intent engine, eligible-to-relevant tool reduction,
extracted tasks and constraints, and the exact tools an agent model would
receive. It then calls `demo_add_numbers` through the task-correlated protected
client. Intent preparation failures stop the run instead of silently exposing
the broader profile-visible list.

## 3. OpenAI function calling with prompt-aware tools

```bash
python -m pip install -e ".[openai]"
export OPENAI_API_KEY=your-openai-api-key
export AGNTID_MCP_URL=http://localhost:8082/mcp
python examples/fastmcp/openai_demo.py
```

For every prompt, this example opens an AgntID task, converts only the runtime
shortlist into OpenAI function definitions, executes selected tools through the
wrapped client, and prints the task analysis used for binding.

## 4. Microsoft Semantic Kernel

```bash
python -m pip install -e ".[msk]"
export OPENAI_API_KEY=your-openai-api-key
export AGNTID_MCP_URL=http://localhost:8082/mcp
python examples/msk/msk_demo.py --agent-name QuickStartAgent --user-id user-42
```

Try:

```text
Add 11 and 22.
```

The SDK converts the returned MCP tools into a Semantic Kernel plugin and keeps runtime control tools out of the model-visible plugin. Continue with the [Microsoft Semantic Kernel guide](msk.md).

## 5. LangChain and Deep Agents without a model key

The repository includes a separate, locked environment for these examples.

```bash
cd examples/langchain-deepagents
export AGNTID_MCP_URL=http://localhost:8082/mcp

uv run --python 3.11 agntid-poc \
  --agent-id docs-langchain-agent \
  --user-id user-42 \
  framework-smoke --framework langchain --first 11 --second 22
```

Run the same call through Deep Agents:

```bash
uv run --python 3.11 agntid-poc \
  --agent-id docs-deep-agent \
  --user-id user-42 \
  framework-smoke --framework deepagents --first 11 --second 22
```

Both commands use a deterministic local model. They test framework tool selection, trusted identity injection, task correlation, runtime policy, and result parsing without sending a prompt to a model provider.

## 6. Interactive LangChain or Deep Agents

```bash
export OPENAI_API_KEY=your-openai-api-key
export MODEL=openai:gpt-4.1-mini

uv run --python 3.11 agntid-poc langchain "Please add 11 and 22"
uv run --python 3.11 agntid-poc deepagents "Please add 11 and 22"
```

Use a model identifier supported by your installed LangChain provider. The example passes the model explicitly.

## 7. Multi-agent operations example

The larger example adds a supervisor, specialist subagents, a saved conversation thread, an execution plan, child delegation records, and approval pauses.

Before running it, confirm that the profile-visible tool list contains all five tools:

- `demo_add_numbers`
- `demo_get_ticket`
- `demo_send_notification`
- `demo_schedule_job`
- `demo_export_payroll_records`

Then run:

```bash
uv run --python 3.11 agntid-poc \
  --agent-id service-operations-supervisor:v1 \
  --user-id user-42 \
  ops-chat
```

If any required tool is hidden by the protection profile, the example stops and lists the missing tools. This is not a connection failure.

## 8. AWS AgentCore with OAuth

The complete AgentCore CLI project uses LangGraph and the AgntID Python SDK. Run its AWS-free tests from the repository root:

```bash
cd examples/agentcore
make test
make validate
```

The test suite verifies the AgentCore HTTP contract, OAuth bearer and user headers, profile-list and application-allowlist intersection, task lifecycle, correlation injection, and result cleanup without contacting AWS. Continue with the [AWS AgentCore guide](agentcore.md) for the local direct smoke, model path, OAuth handoff, CodeZip packaging, and deployment steps.

## Verify the example suite

From `examples/langchain-deepagents`:

```bash
uv run --python 3.11 --extra dev pytest -q
```

From `examples/agentcore`:

```bash
make test
make validate
```

## What’s next

- [Microsoft Semantic Kernel](msk.md)
- [LangChain and Deep Agents](langchain.md)
- [AWS AgentCore](agentcore.md)
- [Core Python guide](python-guide.md)
