---
title: AWS AgentCore
last_verified: 2026-09-09
owner: sdk-team
---

<div class="page-intro" markdown>

# AWS AgentCore

Run a LangGraph agent locally or on Amazon Bedrock AgentCore Runtime while AgntID controls which MCP tools it can see and whether each call is allowed.

</div>

The public `agntid-python` repository now includes a complete AgentCore CLI project. It follows AWS's current `agentcore create`, `agentcore dev`, and `agentcore deploy` workflow, not the retired Python starter toolkit.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/agentcore-oauth-flow.svg" alt="A trusted application refreshes the signed-in user's OAuth token and invokes a local or deployed AWS AgentCore agent. The agent lists and calls profile-visible tools through the AgntID runtime, which records the result." />
  <img class="diagram-dark" src="../../assets/diagrams/agentcore-oauth-flow-dark.svg" alt="A trusted application refreshes the signed-in user's OAuth token and invokes a local or deployed AWS AgentCore agent. The agent lists and calls profile-visible tools through the AgntID runtime, which records the result." />
</div>

## What the example proves

- AgentCore serves the HTTP `/invocations` contract and hosts LangGraph.
- The current user's AgntID OAuth access is forwarded in a dedicated AgentCore custom header.
- A stable user ID comes from the trusted invoking application, not model output.
- One AgntID task opens before agent work and closes after it, including on failure.
- The model sees only the intersection of the runtime-visible tools and the application's allowlist.
- Internal task arguments, access tokens, and AgntID transport metadata do not enter model context.
- Automated tests and a direct local smoke can run without an AWS account.

AgentCore hosts and runs the agent. AgntID remains responsible for tool visibility, task correlation, policy decisions, credential brokerage, and reporting evidence.

## 1. Get the example

Install Python 3.11 or 3.12, [`uv`](https://docs.astral.sh/uv/), Node.js 20 or later, and the [current AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html):

```bash
npm install --global @aws/agentcore
agentcore --version
```

Clone the SDK repository and enter the example:

```bash
git clone https://github.com/AGNTID-AI/agntid-python.git
cd agntid-python/examples/agentcore
make setup
```

For a new runtime, complete the repository's
[shared framework setup](https://github.com/AGNTID-AI/agntid-python/blob/main/examples/README.md)
through its protected direct call before starting the local runtime smoke.

The example was verified with AgentCore CLI `0.28.1` and `bedrock-agentcore==1.22.0`.

`make setup` builds an ignored wheel from the current SDK checkout. This makes
the real `agntid` package available locally and inside the deployment ZIP.

## 2. Run the AWS-free tests

```bash
make test
make validate
```

Expected test result:

```text
14 passed
```

These tests use an in-memory MCP double and deterministic agent runner. They check the AgentCore HTTP contract, custom headers, OAuth bearer parsing, required user identity, tool filtering, task correlation, result cleanup, and task close behavior. They do not contact AWS, Bedrock, AgntID, or a model provider.

`make validate` checks `agentcore/agentcore.json` against the installed AgentCore CLI schema.

## 3. Run AgentCore locally without a model

This smoke starts AgentCore locally and calls `demo_add_numbers` through a local AgntID runtime. It needs the AgntID runtime, but it does not call AWS or an LLM.

Start the AgntID runtime and confirm that `demo_add_numbers` is visible under its current protection profile. Then copy the local settings:

```bash
cp agentcore/.env.local.example agentcore/.env.local
```

For a local MCP address that intentionally has no client authentication, set these values in `agentcore/.env.local`:

```dotenv
AGNTID_MCP_URL=http://localhost:8082/mcp
AGNTID_TOOL_ALLOWLIST=demo_add_numbers
AGNTID_REQUIRE_BEARER=false
AGNTID_ENABLE_DIRECT_SMOKE=true
```

Start AgentCore in terminal 1:

```bash
make dev
```

Invoke it from terminal 2:

```bash
export AGNTID_USER_ID=user-42

curl --fail-with-body --silent --show-error \
  --request POST http://localhost:8080/invocations \
  --header 'Content-Type: application/json' \
  --header 'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: 123e4567-e89b-12d3-a456-426614174000' \
  --header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-User-Id: ${AGNTID_USER_ID}" \
  --data '{
    "prompt": "Add 11 and 22",
    "direct_tool": {
      "name": "demo_add_numbers",
      "arguments": {"first_number": 11, "second_number": 22}
    }
  }'
```

A successful response contains the business result, `mode: "direct-smoke"`, a `task_id`, and the count of visible allowlisted tools. Search Reporting with that task ID.

!!! warning "Direct smoke is for validation"

    `AGNTID_ENABLE_DIRECT_SMOKE` is false by default. Turn it off after the check. Even when enabled, the direct call is limited by the application allowlist, the runtime-visible list, and AgntID's normal task and policy checks.

## 4. Use an OAuth-protected AgntID address

Keep `AGNTID_REQUIRE_BEARER=true`. A trusted backend must obtain the current user's access token through Authorization Code with PKCE, refresh it server-side, and invoke AgentCore with these two headers:

| Header | Value source |
| --- | --- |
| `X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-User-Id` | Stable user ID from the verified application session or token |
| `X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-Authorization` | `Bearer <current AgntID access token>` |

Export the token only for a command-line smoke:

```bash
export AGNTID_ACCESS_TOKEN='<current OAuth access token>'
```

Add this header to the preceding `curl` command:

```text
--header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-Authorization: Bearer ${AGNTID_ACCESS_TOKEN}"
```

The AgntID token is separate from AgentCore invocation authentication and from the AgentCore workload access token. Never put it in the JSON payload, model prompt, committed configuration, or browser storage. See [Protect MCP access with OAuth](../mcp/oauth.md) for the discovery and sign-in flow.

The checked-in runtime configuration includes both names in `requestHeaderAllowlist`; without that AgentCore setting, deployed requests cannot deliver the custom headers to the application.

## 5. Run the LangGraph model path locally

Change the local setting back to:

```dotenv
AGNTID_ENABLE_DIRECT_SMOKE=false
```

Configure AWS credentials with Bedrock model access. Restart `make dev`, then send only the prompt:

```bash
curl --fail-with-body --silent --show-error \
  --request POST http://localhost:8080/invocations \
  --header 'Content-Type: application/json' \
  --header 'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: 123e4567-e89b-12d3-a456-426614174000' \
  --header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-User-Id: ${AGNTID_USER_ID}" \
  --header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-Authorization: Bearer ${AGNTID_ACCESS_TOKEN}" \
  --data '{"prompt":"Add 11 and 22 using the available tool."}'
```

The default model is configured by `AGNTID_MODEL_ID`. The application loads it only on the normal LangGraph path, so the tests and direct smoke remain independent of Bedrock.

## 6. Deploy to AWS AgentCore Runtime

Deployment creates AWS resources. It requires AWS credentials, AgentCore permissions, Bedrock model access, and an AgntID MCP address reachable from the selected AgentCore network mode.

Verify the selected AWS CLI identity before editing the deployment target:

```bash
aws --version
aws sts get-caller-identity
```

The identity needs AgentCore API access and permission to assume the CDK
bootstrap roles used during deployment. Review AWS's current
[AgentCore Runtime permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html)
instead of guessing a production policy.

First replace the `AGNTID_MCP_URL` value in `agentcore/agentcore.json` with the reachable HTTPS address. Do not deploy the checked-in `localhost` value.

Add the deployment account and region to `agentcore/aws-targets.json`:

```json
[
  {
    "name": "dev",
    "description": "AgntID AgentCore development target",
    "account": "123456789012",
    "region": "us-east-1"
  }
]
```

Validate and package the project before deployment:

```bash
make validate
make package
agentcore deploy --dry-run
make deploy
```

The Make targets rebuild the ignored SDK wheel when its source changes. The
CodeZip artifact therefore contains the actual `agntid` package instead of a
checkout-only editable path. Run these commands from a complete clone; do not
copy only the `examples/agentcore` directory.

Invoke the deployed agent:

```bash
agentcore invoke \
  --runtime AgntidAgent \
  --target dev \
  --session-id 123e4567-e89b-12d3-a456-426614174000 \
  --header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-User-Id: ${AGNTID_USER_ID}" \
  --header "X-Amzn-Bedrock-AgentCore-Runtime-Custom-Agntid-Authorization: Bearer ${AGNTID_ACCESS_TOKEN}" \
  'Add 11 and 22 using the available tool.'
```

Use `agentcore logs` and `agentcore traces` for hosting diagnostics. Use AgntID Reporting and the returned `task_id` for authoritative tool, policy, and audit evidence.

## Security boundaries

- The MCP URL, agent identity, model ID, and tool allowlist are operator configuration, not payload fields.
- Missing user identity fails closed; the example does not invent or share a fallback identity.
- The application allowlist can reduce the runtime list but cannot reveal a hidden tool.
- AgntID checks the actual tool arguments again at call time.
- Runtime control tools and internal correlation arguments are not exposed to the model.
- The access token is used only by the MCP transport and is not deliberately logged or returned.
- A trusted backend, not browser JavaScript, owns token refresh and AgentCore invocation.

## Common problems

| Problem | Check |
| --- | --- |
| Missing required header | Use the exact two custom header names; matching is case-insensitive. |
| No allowlisted tools are visible | Compare `AGNTID_TOOL_ALLOWLIST` with the current profile-filtered MCP list. |
| Local MCP connection fails | Confirm the runtime is ready and `AGNTID_MCP_URL` is correct. |
| Deployed MCP connection fails | Use a reachable HTTPS address and review AgentCore public/VPC egress. |
| Bedrock model fails | Check model access, execution-role permissions, region, and `AGNTID_MODEL_ID`. |
| Instructions mention `agentcore configure` or `agentcore launch` | They use the legacy starter toolkit; use the current CLI commands on this page. |

## Source and AWS references

- [AgntID AgentCore example](https://github.com/AGNTID-AI/agntid-python/tree/main/examples/agentcore)
- [AWS AgentCore CLI getting started](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html)
- [AWS AgentCore samples](https://github.com/awslabs/agentcore-samples)
- [AWS AgentCore Python SDK](https://github.com/aws/bedrock-agentcore-sdk-python)

## What’s next

- [Use LangChain or Deep Agents](langchain.md)
- [Use Microsoft Semantic Kernel](msk.md)
- [Understand OAuth for MCP](../mcp/oauth.md)
- [Review tool visibility](../mcp/index.md#how-tool-visibility-works)
