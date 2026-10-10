---
title: AgntID Documentation Context
documentation_version: development
source_commit: unknown
generated_at: 2026-10-09T07:17:04Z
---

# AgntID Documentation Context

This text-only reference is generated from approved AgntID documentation. It is intended for coding assistants, search, offline reading, and other workflows that benefit from one portable Markdown file.

Use the source labels to distinguish pages. Commands and code examples are preserved; screenshots and diagrams are represented by concise descriptions.


---

## Source document: AgntID Documentation

Source: https://docs.agntid.ai/

# Control which tools AI agents can see and use

AgntID places access controls between AI clients and their tools. A customer-hosted runtime filters the available tools, checks every call, and sends the result to the [AgntID portal](https://app.agntid.ai/) for reporting.

[Start the Quick Start](quick-start.md)
[Connect an MCP client](mcp/connect-clients.md)
[Download documentation](downloads.md)

## What do you want to do?

  
    
### Set up AgntID

    
Deploy and connect a runtime, review its protection profile, and run a protected tool.

  
  
    
### Add MCP tools

    
Add an MCP server in the portal and review which discovered tools are available.

  
  
    
### Connect a client

    
Generate the configuration for Cursor, Claude, or Codex and connect it to the runtime.

  
  
    
### Test access

    
Send a plain-English request and compare an allowed tool call with a denied one.

  
  
    
### Build with an SDK

    
Connect an application to AgntID and handle tool results and denials in code.

  

## How AgntID protects tools

  
> Visual reference: MCP clients and applications connect through a customer-hosted runtime to tools, while the AgntID portal synchronizes access settings and receives reporting events

  

1. **Configure access in the [AgntID portal](https://app.agntid.ai/).** Register a runtime, add MCP servers, choose a protection profile, and add tool-specific policies when needed.
2. **Enforce access in your environment.** The protection profile creates the starting tool list. Tool review, individual settings, and user roles can reduce it. The runtime checks policy whenever a visible tool is called.
3. **Run the tool or stop the call.** An allowed call reaches its MCP server. A denied call stops at the runtime. Both outcomes are available in Reporting.

## Learn more

- [Understand MCP tool visibility](mcp/index.md#how-tool-visibility-works)
- [Troubleshoot a connection or tool call](troubleshooting.md)
- [View detailed flow diagrams](flows.md)
- [Read the release notes](release-notes.md)


---

## Source document: Quick Start

Source: https://docs.agntid.ai/quick-start/

# Quick Start

Deploy a customer-hosted AgntID runtime, add input limits to a built-in MCP tool, simulate AI-agent requests, and verify that AgntID allows or denies tool execution before the tool runs. The required path takes about 15 minutes, plus the first model download.

  
> Visual reference: Runtime setup, profile review, demo tool availability, input policy, Simulator allowed and denied calls, and Reporting audit; MCP Inspector is an optional debugging branch

  

!!! info "What you will prove"
    - The runtime connects to the AgntID control plane.
    - The Medium protection profile is reviewed and synchronized.
    - A built-in demo MCP tool is available.
    - A policy restricts allowed inputs for `demo.add_numbers`.
    - Simulator succeeds when inputs are allowed.
    - Simulator is denied when inputs violate policy.
    - Reporting shows the full allow/deny audit trail.

## Before you begin

You need:

- access to the **[AgntID portal](https://app.agntid.ai/)** and its container registry
- Docker with Docker Compose v2
- outbound HTTPS access
- approximately 4 GB RAM and 5 GB free disk space

The intent parser downloads an approximately 900 MB model on first start. Allow several extra minutes, depending on your connection.

You also need at least one healthy AI model credential configured in AgntID to use Simulator. If your organization does not have one yet, complete runtime setup first, then add a model credential under **Access Control → Credentials** before running the Simulator step.

You do not need Cursor, Claude, Codex, or any external MCP client for this Quick Start.

## 1. Prepare and deploy runtime 2.0.0

1. Create a clean working directory.

    === "Linux / macOS"

        ```bash
        mkdir agntid-runtime
        cd agntid-runtime
        ```

    === "Windows PowerShell"

        ```powershell
        New-Item -ItemType Directory agntid-runtime
        Set-Location agntid-runtime
        ```

2. Download the customer compose file.

    === "Linux / macOS"

        ```bash
        curl -L -o docker-compose.yml https://raw.githubusercontent.com/AGNTID-AI/agntid-python/main/docker-compose.yml
        ```

    === "Windows PowerShell"

        ```powershell
        Invoke-WebRequest https://raw.githubusercontent.com/AGNTID-AI/agntid-python/main/docker-compose.yml -OutFile docker-compose.yml
        ```

3. Start both services. The runtime images are public on GitHub Container Registry, so no registry login is required.

    ```bash
    docker compose up -d
    ```

4. Wait for both services to report `healthy`.

    ```bash
    docker compose ps
    ```

If either service remains unhealthy, run `docker compose logs -f` and see [Troubleshooting](troubleshooting.md).

**Checkpoint:** `docker compose ps` shows both services as `healthy`.

## 2. Register a runtime

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select **Add Runtime**.
2. Name it `Quick Start Runtime`, then generate its bootstrap token.
3. Copy the token and use it in the next step to connect your prepared runtime. Treat it like a password; do not paste it into tickets, chat, screenshots, or source control.

The token is shown only for bootstrapping this runtime.

  
> Visual reference: Register Runtime dialog with the Quick Start Runtime name, before the bootstrap token is shown

**Checkpoint:** The portal lists `Quick Start Runtime`, and you have its bootstrap token ready for connection.

## 3. Connect the runtime

1. Open the **local runtime UI** at [http://localhost:8080](http://localhost:8080).

    

      
> Visual reference: Local runtime UI ready for a bootstrap token

    

2. Paste the bootstrap token and select **Connect to Control Plane**.
3. Confirm that the local runtime UI shows **Operational** and **Connected**.

    

      
> Visual reference: Local runtime UI showing Operational and Connected status

    

4. Return to **Runtimes** in the [AgntID portal](https://app.agntid.ai/) and open `Quick Start Runtime`.

The AgntID portal is the control plane. The local runtime UI runs on your machine and shows whether the runtime is connected and ready.

  
> Visual reference: AgntID portal synchronizing profiles and policies to a customer runtime that filters and enforces access to MCP servers

  

**Checkpoint:** The local runtime UI shows **Operational** and **Connected**.

## 4. Complete Setup and review the profile

1. Open the runtime's **Setup** tab. Its five rows are **Runtime Registered**, **Runtime Healthy**, **MCP Support**, **CLI Enforcement**, and **Protection Profile**.

    

      
> Visual reference: Runtime Setup tab showing four of five checks complete and Protection Profile as the next step

    

2. Leave optional CLI enforcement off for this quick start. The built-in `demo` MCP server is already available.
3. Open **Protection Profile**, review **Medium / READ_WRITE**, and mark the profile reviewed.

    | Profile | Actions available after review |
    | --- | --- |
    | Low | All reviewed actions can run unless a policy blocks them |
    | Medium | Reviewed read and normal-write actions can run. Delete, execute, and other high-impact actions cannot run. |
    | High | Only reviewed read and list actions that do not change data can run |

    The protection profile controls the largest set of tool actions the runtime may expose. Tool policies then decide whether a specific visible tool call is allowed based on details such as inputs.

    

      
> Visual reference: Protection Profile Review with Medium selected, the projected enabled and disabled action counts, classification review status, and saved runtime settings applied

    

4. Confirm **5 of 5** setup checks and **Runtime sync: Applied**.

    

      
> Visual reference: Runtime Setup tab showing all five setup checks complete

    

**Checkpoint:** Setup shows **5 of 5** complete and **Runtime sync: Applied**.

## 5. Confirm demo MCP tools are available

1. In the portal, open `Quick Start Runtime`.
2. Open **Operations → MCP → Servers**.
3. Confirm the built-in `demo` MCP server is enabled and connected.
4. Confirm `demo.add_numbers` is available.
5. If you made any changes, wait for **Runtime sync: Applied**.

**Checkpoint:** You have a healthy runtime with the demo MCP server available. Do not test the tool yet; first add a policy so the test demonstrates enforcement.

## 6. Add input limits to demo.add_numbers

Now add a simple policy that makes one call succeed and another call fail. This creates a clear end-to-end enforcement test.

1. Open **Access Control → Access Policies**.
2. Select the `demo` server.
3. Select `demo.add_numbers`.
4. Open the **Baseline Allow Policy**.
5. Add these input constraints:

    | Input | Minimum | Maximum |
    | --- | --- | --- |
    | `first_number` | 10 | 20 |
    | `second_number` | 20 | 30 |

    

      
> Visual reference: Baseline policy for demo.add_numbers with input ranges 10 to 20 and 20 to 30

    

6. Save the policy.
7. Wait for **Runtime sync: Applied**. The runtime signs policy changes automatically during synchronization.

**Checkpoint:** `demo.add_numbers` has input limits for both inputs. The runtime allows it only when `first_number` is between 10 and 20 and `second_number` is between 20 and 30, inclusive.

These limits affect only `demo.add_numbers`. Other tools continue to follow their own protection profile, review state, OAuth role grants, and policy decisions.

## 7. Test policy in Simulator

Simulator is the native AgntID way to test how an AI-agent request will behave. The model receives a plain-English request, chooses from profile-visible tools, and the AgntID runtime checks the selected tool call before execution. An allowed call runs the real demo tool on your runtime.

1. On `Quick Start Runtime`, open **Operations → Configuration**, enable **Simulation System** under **Simulation**, and select **Save Configuration**. Wait for synchronization to show **Applied** so the runtime appears in Simulator.
2. Confirm you have a **Healthy** AI model credential under **Access Control → Credentials**. Add one for your AI provider if needed.
3. Open **Observe & Validate → Simulator**.
4. Select `Quick Start Runtime`.
5. Select the healthy model credential.
6. Select a model, or keep the default model for your provider.
7. Select **Connect**. After connection, a request box and **Run** button appear.

    

      
> Visual reference: Simulator setup with a runtime, healthy model credential, selected model, and Connect button

    

8. Enter this allowed prompt and select **Run**:

    ```text
    Use demo.add_numbers to add 11 and 21.
    ```

9. Confirm **Success** and `Result: 32` in **Results**.

    

      
> Visual reference: Simulator showing Success and result 32 for demo.add_numbers with inputs 11 and 21

    

    **Checkpoint:** Simulator shows **Success** and `Result: 32`. The AI request selected and ran an approved tool call.

10. Enter this denied prompt and select **Run**:

    ```text
    Use demo.add_numbers to add 50 and 21.
    ```

11. Confirm **Execution Denied** and a message like:

    ```text
    AgntID Policy Denied
    Policy denied: first_number must satisfy {'min': 10, 'max': 20}
    ```

    

      
> Visual reference: Simulator showing AgntID Policy Denied because first_number 50 violates the input limits

    

    **Checkpoint:** Simulator shows **AgntID Policy Denied** and mentions `first_number`. The runtime blocked the policy-violating tool call before execution.

## 8. Verify results in Reporting

Reporting is the audit trail. It shows what the agent requested, which tool was selected, whether the runtime allowed or denied execution, which policy applied, and why.

1. Open **Reporting**.
2. Find the latest `demo.add_numbers` event groups from your two Simulator runs.
3. Expand each event group.
4. Confirm these outcomes:

    | Event | Allowed run (`11`, `21`) | Denied run (`50`, `21`) |
    | --- | --- | --- |
    | Intent Check | Success | Success |
    | Intercept | Success | Success |
    | Tool Execution | Success | Denied |

5. For the denied run, confirm the denial reason identifies `first_number` and its minimum of 10 and maximum of 20. The denied Tool Execution event records the blocked attempt; the tool did not run.

**Checkpoint:** Reporting shows both successful and denied tool execution events for `demo.add_numbers`, including the input-policy denial reason.

## Optional: Debug raw MCP behavior with MCP Inspector

MCP Inspector is useful for testing the raw MCP endpoint directly. It is not required for this Quick Start and is less representative of the native AgntID workflow than Simulator.

Use MCP Inspector to verify the runtime's tool list, call `demo_add_numbers` without an AI model, debug MCP client/runtime connectivity, or compare raw MCP calls with Simulator-driven calls.

1. Open **Inspector** in the portal.
2. Select `Quick Start Runtime`.
3. Select **Create Link**, then **Open Inspector**.
4. If **Connection Type** is **Via Proxy**, select **Direct**.
5. Select **Connect**. The connection uses the runtime's secure AgntID tunnel; it does not require a public runtime port.
6. Open **Tools** and select **List Tools**. The list contains only tools allowed by the runtime's protection profile. Inspector exposes `demo.add_numbers` as `demo_add_numbers`.
7. Run `demo_add_numbers` with `first_number: 11` and `second_number: 21`.
8. Confirm result `32`.
9. Run `demo_add_numbers` with `first_number: 50` and `second_number: 21`.
10. Confirm policy denial.

**Checkpoint:** MCP Inspector returns `32` for the allowed inputs and a policy denial for `first_number: 50`.

## What's next

- [Add a customer MCP server](mcp/attach-server.md)
- [Create policies for real tools](mcp/advanced.md)
- [Use Simulator for policy testing](simulator/index.md)
- [Connect external MCP clients such as Cursor, Claude, or Codex](mcp/connect-clients.md)
- [Use MCP Inspector for raw MCP debugging](#optional-debug-raw-mcp-behavior-with-mcp-inspector)
- Review [Runtime Operations](runtime/index.md) for connections, recent activity, metrics, settings, security, and audit records, and use [Troubleshooting](troubleshooting.md) for connection or enforcement issues

For CLI enforcement, tool classifications, catalog changes, and custom Rego rules, see [Advanced access controls](mcp/advanced.md).


---

## Source document: Configure the intent engine

Source: https://docs.agntid.ai/runtime/intent-engine/

# Configure the intent engine

Choose the intent mode that matches the complexity of the user's request, then use the [Simulator](../simulator/index.md) to verify which mode protected the run.

## What the intent engine does

When an agent sends a plain-English request, AgntID compares the request with the tool action the model wants to run.

Intent checks help answer questions such as:

- Did the model choose a tool that matches the user's request?
- Did the model ignore a limit such as "do not send email"?
- Should the tool result be shown back to the model?
- Did the final answer stay within the facts AgntID released?

Intent checks do not replace profiles, guardrails, or policies. They add another check around the model's decision.

## Choose Standard or LLM-based

AgntID supports two intent modes.

| Mode | Use it when | What to expect |
| --- | --- | --- |
| **Standard** | You are setting up the runtime, testing a simple request with a clear tool, or do not want to configure an intent LLM credential yet | AgntID uses its local natural language inference (NLI) and schema pipeline to compare each proposed tool call with the request. It does not shortlist tools, inspect tool output, or validate the final answer. |
| **LLM-based** | Your runtime has many tools, unclear tool names, multi-step or long prompts, explicit limits such as "do not send email," or untrusted tool output | AgntID uses your OpenAI credential to analyze the complete task, shortlist tools, check each tool call, inspect tool output, and validate the final answer. |

LLM-based intent can fall back to Standard if the runtime cannot complete the LLM-based check. The run output shows which engine was used.

!!! important "Choose the mode before a complex test"
    **Standard is the default** for a new or unconfigured runtime. It is a baseline tool-call alignment check, not the full contextual protection path. A long or compound request can contain several actions, dependencies, or negative instructions that do not fit one broad action classification. In that case, Standard may produce an incomplete or low-confidence interpretation.

    Use **LLM-based** intent before demonstrating multi-step task analysis, explicit prohibitions, tool shortlisting, tool-output protection, or final-answer validation. Do not present a Standard result as evidence that those LLM-based stages ran.

## Compare the protection stages

| Protection stage | Standard | LLM-based |
| --- | --- | --- |
| Customer-owned OpenAI credential required | No | Yes |
| Compare a proposed tool call with the request | Yes | Yes |
| Interpret multiple tasks, dependencies, and explicit constraints | Limited to the Standard classification pipeline | Yes |
| Shortlist relevant tools before model planning | No | Yes |
| Inspect tool output before returning facts to the model | No | Yes |
| Validate the final answer against released facts | No | Yes |

Use Standard for a simple baseline. Use LLM-based when the protection claim depends on understanding the request as a complete task or on checking what happens after a tool runs.

## Intent engine vs tool intelligence

These settings are related, but they run at different times.

| Setting | When it runs | Purpose |
| --- | --- | --- |
| **Intent engine** | During a prompt, tool call, tool result, or final answer | Checks whether the model's action still matches the user's request. |
| **Tool intelligence** | When tools are discovered | Adds better tool hints so AgntID can classify and select tools more accurately. |

Use **Standard** tool intelligence for the simplest setup. Use **LLM-based** tool intelligence when a server exposes many tools or tool descriptions are hard to understand.

## Before you configure LLM-based intent

You need:

- a connected and healthy runtime
- one healthy OpenAI credential in the same organization as the runtime
- permission to update runtime configuration

If you only want to use Standard intent, no OpenAI credential is required for the intent engine.

## Configure the intent engine

Use this screen path in the [AgntID portal](https://app.agntid.ai/):

| Screen | What to do | What to confirm |
| --- | --- | --- |
| **Runtimes** | Select the runtime you want to configure | Runtime is **Healthy** and **Connected** |
| **Runtime detail** | Open **Operations → Configuration** | You are editing the correct runtime |
| **Runtime features** | Find **Intent engine** | Current mode is visible before you change it |
| **Intent engine configuration** | Choose **Standard** or **LLM-based** | LLM-based shows credential configuration |
| **Credential selector** | Choose the OpenAI credential | Credential belongs to the same organization |
| **Save configuration** | Select **Save Configuration** | The runtime starts synchronizing the new setting |
| **Audit or activity view** | Review the saved change | The change is shown in plain language, such as **Intent engine: LLM-based** |

Then follow these steps:

1. Open **Runtimes**.
2. Select the runtime you want to configure.
3. Open **Operations → Configuration**.
4. In **Runtime features**, find **Intent engine**.
5. Choose **Standard** or **LLM-based**.
6. If you choose **LLM-based**, select **Configure** and choose an OpenAI credential.
7. Optional: enter a model override. If you leave it empty, the runtime uses its default model.
8. Select **Save Configuration**.
9. Wait for the runtime to synchronize the new settings.

After saving, the runtime audit should show the updated setting in plain language, for example **Intent engine: LLM-based**.

!!! note "Screenshots"
    Add screenshots for the screen path above when capturing the final docs assets. Do not use screenshots that show secret values, API keys, or private runtime identifiers.

## Configure tool intelligence

Tool intelligence is configured in the same place.

1. Open **Runtimes** and select the runtime.
2. Open **Operations → Configuration**.
3. In **Runtime features**, find **Tool intelligence**.
4. Choose **Standard** or **LLM-based**.
5. If you choose **LLM-based**, select the OpenAI credential.
6. Select **Save Configuration**.
7. Wait for runtime synchronization.

After saving, newly discovered tools can use the selected intelligence mode during classification.

## Test the configuration

Use the Simulator after the runtime has synchronized.

First run a simple request:

```text
Use demo.add_numbers to add 11 and 21.
```

Then run a request with a clear limit:

```text
Check my calendar for today. Do not send any email.
```

In the Simulator, open **Call Flow** and check:

- the intent stage identifies **LLM-based** or `contextual` as the engine used
- **Task analysis** found the user request and limits
- **Tool shortlist** showed only relevant tools
- **Tool call** matched the user's request
- **Tool output protection** inspected the tool result before releasing facts
- **Final answer validation** checked the final answer before the user saw it

Check the engine used for every important run. The saved runtime setting is the requested mode; a run can still use Standard if LLM-based intent falls back. If Call Flow shows `standard` or a fallback reason, fix the credential or runtime problem and run the test again before claiming LLM-based protection.

For more detail about reading the Simulator output, see [Read intent checks in Simulator](../simulator/intent.md).

## What changes after LLM-based intent is enabled

| Area | What you should see |
| --- | --- |
| **Call Flow** | Extra intent stages such as Task analysis, Tool shortlist, Tool output protection, and Final answer validation |
| **Audit** | Entries showing what AgntID allowed, denied, withheld, or released |
| **Logs** | Human-readable stage names for intent decisions |
| **Metrics** | Intent check counts and timing for the stages that ran |

If a tool result cannot be safely inspected, AgntID withholds it from the model. The Simulator should show a short user-safe message instead of internal runtime details.

## How this fits with other controls

| Control | What it controls |
| --- | --- |
| Protection profile | Which tool actions can be visible at all |
| Tool review and state | Whether a discovered action is approved and enabled |
| OAuth role grants | Which tools a connected client role can see |
| Guardrails | Extra limits on a credential, such as day, time, or rate rules |
| Policies | Whether a specific tool call and its inputs are allowed |
| Intent checks | Whether the tool call and final answer still match the user's prompt |

For the full request path, see [Flow Diagrams](../flows.md#simulator-request).


---

## Source document: Simulator

Source: https://docs.agntid.ai/simulator/

# Simulator

Use the Simulator to send a plain-English request to an AI model and see how AgntID protects each tool call. This guide connects a runtime, runs one allowed request and one denied request, and reviews the result. It takes about 10 minutes after the [Quick Start](../quick-start.md) is complete.

  
> Visual reference: Simulator journey from preparation and connection to an allowed or denied request and review

  

!!! important "This is a live test"
    The Simulator is not a preview or a mock. An allowed request runs the selected tool on your runtime. Use test tools and test data.

## Before you begin

You need:

- an **Active** and **Healthy** runtime with [Setup complete](../quick-start.md#4-complete-setup-and-review-the-profile)
- **Simulation System** enabled on that runtime
- one healthy AI model credential
- an enabled policy for the tool you want to test

Standard is the default intent mode. It is suitable for the simple allow-and-deny examples on this page. Before testing a larger prompt, multiple dependent actions, an explicit prohibition, or protection after a tool returns data, configure [LLM-based intent](../runtime/intent-engine.md#choose-standard-or-llm-based). In **Call Flow**, confirm that the engine used is LLM-based and that no fallback occurred.

The Medium protection profile creates baseline allow policies when you complete runtime Setup. No manual policy signing is needed; the runtime signs synchronized policy changes automatically.

To follow the allow-and-deny example below, first complete [Add input limits to demo.add_numbers](../quick-start.md#6-add-input-limits-to-demoadd_numbers). It limits `demo.add_numbers` as follows:

| Input | Allowed values |
| --- | --- |
| `first_number` | 10 to 20 |
| `second_number` | 20 to 30 |

## 1. Prepare the runtime

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select your runtime.
2. Open **Operations → Configuration**.
3. Under **Simulation**, turn on **Simulation System**.
4. Select **Save Configuration**.
5. Wait for the next policy synchronization. The runtime then appears in the Simulator runtime list.

  
> Visual reference: Runtime Configuration with Simulation System enabled and Save Configuration available

Next, open **Access Control → Credentials**. Add a credential for your AI provider if you do not already have one. Save it and confirm that its status is **Healthy**. Never include the secret value in screenshots, tickets, or source control.

  
> Visual reference: Credentials page with a healthy Simulator Demo AI model credential

AgntID securely provides the selected credential to the customer-hosted runtime for the simulation session.

## 2. Connect the Simulator

1. Open **Observe & Validate → Simulator**.
2. Select the runtime you prepared.
3. Select the AI model credential.
4. Keep the default model, or choose another available model.
5. Select **Connect**.

The model list depends on your provider and can change. The portal selects a default model automatically.

  
> Visual reference: Simulator session setup with a runtime, AI model credential, default model, and Connect button

After the connection succeeds, a request box and **Run** button appear.

  
> Visual reference: Connected Simulator with a plain-English request box and Run button

  
> Visual reference: A Simulator request moving from the AgntID portal through the customer runtime policy check to an MCP tool

  

## 3. Run an allowed request

Enter this request and select **Run**:

```text
Use demo.add_numbers to add 11 and 21
```

Both values are within the policy limits, so the runtime allows the tool call. The **Results** tab shows **Query Results**, a green **Success** badge, and the result `32`.

  
> Visual reference: Simulator Results tab showing a successful demo.add_numbers request and result 32

The tool name is included because this runtime has more than one addition tool. Naming the tool makes the example repeatable. For normal testing, you can use a request without a tool name and see which profile-visible tool the model selects.

## 4. Run a denied request

Enter this request and select **Run**:

```text
Use demo.add_numbers to add 50 and 21
```

`first_number` is outside the allowed range of 10 to 20. The runtime blocks the tool before it runs. The **Results** tab shows **Execution Denied**, **AgntID Policy Denied**, and the failed input rule.

  
> Visual reference: Simulator Results tab showing demo.add_numbers denied because first_number is outside its allowed range

This policy limits only `demo.add_numbers`. Other tools remain controlled by their protection profiles and their own policy decisions.

## 5. Review what happened

Use the tabs below the request to understand the result:

| Tab | What it shows |
| --- | --- |
| **Results** | The answer, tool-call count, and final outcome |
| **Logs** | A time-ordered record of the request |
| **Call Flow** | Each step from the request to the final response |
| **Audit** | Guardrail, intent, and policy decisions for each tool call |
| **Metrics** | Time spent on the model, policy checks, and tools |

For a short explanation of the Call Flow stages, see [Read intent checks](intent.md). To change Standard or LLM-based intent, see [Configure the intent engine](../runtime/intent-engine.md).

The denied call flow shows where processing stopped. Expand a row when you need more detail.

  
> Visual reference: Simulator Call Flow tab showing passed steps followed by a denied policy step

The Audit tab shows the policy decision and the tool involved. It provides evidence that the denial happened before tool execution.

  
> Visual reference: Simulator Audit Trail with passed guardrail and intent checks and a denied policy evaluation

Use **Simulation history** to reopen recent saved runs. A session expires after 30 minutes without activity; reconnect to continue.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No runtime is listed | Confirm that Simulation System is saved, and the runtime is Active and Healthy. Wait for the next synchronization. |
| No credential is listed | Add an AI model credential under Access Control → Credentials and confirm that it is Healthy. |
| Connection fails | Check the runtime connection and the selected credential. Then reconnect. |
| A different tool runs | Name the required tool in the request, as shown in this guide. |
| The expected denial does not occur | Confirm the input limits, policy status, and latest runtime synchronization. |
| Session expired | Select Connect to create a new session. |

For more checks, see [Troubleshooting](../troubleshooting.md).

## What's next

- [Add an MCP server](../mcp/attach-server.md) and test one of its tools
- [Configure the intent engine](../runtime/intent-engine.md)
- [Understand intent checks in Simulator](intent.md)
- Learn about [Runtime operations](../runtime/index.md)
- Use the [Inspector](../quick-start.md#optional-debug-raw-mcp-behavior-with-mcp-inspector) for direct tool tests
- Review allowed and denied events in [Reporting](../quick-start.md#8-verify-results-in-reporting)


---

## Source document: Read intent checks in Simulator

Source: https://docs.agntid.ai/simulator/intent/

# Read intent checks in Simulator

Use this page to understand the intent stages shown during a Simulator run. To configure Standard or LLM-based intent on a runtime, see [Configure the intent engine](../runtime/intent-engine.md).

## What the Simulator shows

!!! important "Confirm the engine used"
    Standard is the default intent mode. Use it for simple, clear tool-call checks. Select **LLM-based** intent before testing a long or multi-step prompt, an explicit limit such as "do not send email," tool-output protection, or final-answer validation.

    In **Call Flow**, expand the intent stage and confirm the engine used. A saved LLM-based setting can fall back to `standard` when the LLM check cannot complete. Treat that run as a Standard result, not as evidence of LLM-based protection.

In a Simulator run, AgntID can show these stages around the model and the runtime:

| Stage | What it means |
| --- | --- |
| Prompt correlation | AgntID binds the run to one user prompt. Later checks use that prompt as the source of authority. |
| Task analysis | AgntID reads what the user asked for, including limits such as "do not send email". |
| Tool shortlist | AgntID decides which profile-visible tools are relevant to the prompt. |
| Tool call | The model chooses a tool and arguments. |
| Guardrail validation | Credential guardrails are checked. If none are configured, the Simulator shows **No guardrails set**. |
| Policy evaluation | Tool policies check whether the selected tool and input values are allowed. |
| Tool output protection | AgntID inspects the tool result before releasing facts back to the model. |
| Final answer validation | AgntID checks the final answer before it is shown to the user. |

Not every run shows every stage. For example, a request that does not call a tool has no tool output to inspect. Standard runs do not show LLM-based task analysis, tool shortlisting, tool-output protection, or final-answer validation as completed protection stages.

## What to test first

Use a small Simulator request first:

```text
Use demo.add_numbers to add 11 and 21.
```

Then test a request with a clear limit:

```text
Check my calendar for today. Do not send any email.
```

In **Call Flow**, check:

- which tools were shown to the model
- whether the chosen tool matched the prompt
- whether policy allowed or denied the tool call
- whether tool output was inspected before the final answer
- whether the final answer stayed within released facts

## How to read each tab

| Tab | What to look for |
| --- | --- |
| **Call Flow** | The order of model, intent, guardrail, policy, tool, and final-answer stages |
| **Audit** | The decision AgntID made at each security stage |
| **Logs** | A time-ordered record of the run, with readable stage names |
| **Metrics** | Time spent and count of model, tool, policy, and intent checks |
| **Results** | The final answer or the reason the request was blocked |

## Common outcomes

| Outcome | What it means |
| --- | --- |
| **Allowed** | The tool call matched the prompt and passed the configured controls. |
| **Denied** | AgntID blocked the tool call before execution. Check Audit and Call Flow for the failed stage. |
| **Tool output withheld** | The tool ran, but AgntID did not release the result to the model because output inspection failed or found unsafe content. |
| **Fallback to Standard** | LLM-based intent could not complete, so AgntID used the Standard engine. Check runtime health and the configured OpenAI credential. |

For a hackathon or recorded demonstration, keep the expanded intent stage visible in the evidence. This makes the engine, completed stages, and any fallback clear to reviewers.

For the full request path, see [Flow Diagrams](../flows.md#simulator-request). To change the runtime setting, see [Configure the intent engine](../runtime/intent-engine.md).


---

## Source document: Use MCP with AgntID

Source: https://docs.agntid.ai/mcp/

# Use MCP with AgntID

Use AgntID to place access controls between MCP clients and the tools they use. You add an MCP server in the [AgntID portal](https://app.agntid.ai/), the customer-hosted runtime discovers its tools, and the runtime shows each client only the tools allowed by its protection profile.

  
> Visual reference: MCP journey from adding a server in the portal through runtime discovery and profile filtering to a connected client and reporting

  

## Before you begin

Complete the [Quick Start](../quick-start.md). Your runtime must be **Healthy**, **Connected**, and have **MCP Support** enabled.

Use the guides in this order:

1. [Add an MCP server](attach-server.md).
2. [Review its discovered actions and classifications](advanced.md).
3. [Connect Cursor, Claude, or Codex](connect-clients.md).
4. If required, [protect client access with OAuth](oauth.md).
5. Review activity in **MCP → Access Dashboard** and **Reporting**.

## Servers, tools, and clients

| Term | Meaning |
| --- | --- |
| **MCP server** | Provides tools, such as a remote service or a process started by the runtime |
| **Tool** | One action provided by a server, such as listing files or creating an issue |
| **MCP client** | Uses the tools, such as Cursor, Claude, or Codex |
| **AgntID runtime** | Discovers tools, filters the tool list, checks every call, and records the outcome |

## How tool visibility works

Adding a server does not make every tool available to every client. AgntID reviews each discovered action and applies the runtime's protection profile.

| Profile | Tools that can be shown after review |
| --- | --- |
| **Low** | All reviewed actions, unless an individual setting or policy blocks them |
| **Medium** | Reviewed read and normal-write actions; destructive and high-impact actions remain hidden |
| **High** | Reviewed read and list actions that do not change data |

A tool can also remain hidden while its classification is waiting for review, when it is disabled, or when a client role does not have access. Policies continue to check calls for tools that are visible.

  
> Visual reference: Tools page showing a discovered MCP tool surface, its Medium protection profile, and actions that need review

## Choose the right test

| Goal | Use |
| --- | --- |
| Call a tool directly | [Inspector](../quick-start.md#optional-debug-raw-mcp-behavior-with-mcp-inspector) |
| Send a plain-English request and let an AI model select a tool | [Simulator](../simulator/index.md) |
| Test the experience used by developers | [Cursor, Claude, or Codex](connect-clients.md) |

Inspector uses a secure AgntID tunnel. Simulator uses a portal-controlled runtime session. Neither test proves that an external client's OAuth login works. Test OAuth with the client that people will use.

If you want the model to work from a plain-English request, configure the [intent engine](../runtime/intent-engine.md). Then use [Read intent checks in Simulator](../simulator/intent.md) to understand tool shortlisting, output inspection, and final-answer validation.

## Two different kinds of authentication

- **Client access** protects the connection from Cursor, Claude, Codex, or another MCP client to the AgntID runtime. See [Protect MCP access with OAuth](oauth.md).
- **Server credentials** let the runtime connect to an external MCP server. Configure them while [adding the server](attach-server.md#server-credentials).

Keeping these directions separate makes it clear which connection is being protected.

## What’s next

- [Add an MCP server](attach-server.md)
- [Review Advanced access controls](advanced.md)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)
- [Troubleshooting](../troubleshooting.md)


---

## Source document: Add an MCP Server

Source: https://docs.agntid.ai/mcp/attach-server/

# Add an MCP Server

Add and test an MCP server from the [AgntID portal](https://app.agntid.ai/). The portal sends the saved configuration to your customer-hosted runtime; you do not need to edit a runtime configuration file or restart the runtime.

## Before you begin

You need:

- a runtime that is **Healthy** and **Connected**
- **MCP Support** enabled in the runtime's **Setup** tab
- the address or start command for the MCP server
- any required values available as environment variables on the runtime host

The built-in `demo` server is for learning and testing. Add a customer MCP server before using the runtime for real tool access.

  
> Visual reference: Runtime MCP Servers page showing the built-in demo server and the Add MCP button

## 1. Open MCP Servers

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select your runtime.
2. Open **Operations → MCP → Servers**.
3. Select **Add MCP**.

## 2. Choose how the runtime reaches the server

Use **Form** for normal setup. Use **JSON** only when you need fields that are not shown in the form.

| Connection style | Use it when |
| --- | --- |
| **Remote HTTP** | The MCP server is already running at a URL that the runtime can reach |
| **Local npx** | The runtime should start a Node.js MCP package |
| **Local uvx** | The runtime should start a Python MCP package |
| **Local Docker** | The runtime should start an MCP container |
| **Other local command** | The runtime should start another local program |
| **Service connector** | You are using an AgntID connector, such as AWS S3 |

  
> Visual reference: Add MCP Server dialog with the server template, connection style, server ID, prefix, and URL fields

For a remote server, enter its MCP URL. For a local server, enter the command and put each command argument on a separate line.

!!! note "Docker-based servers"
    Docker must be available to the runtime. If the runtime is in a container, Docker socket sharing must also be enabled before the connection test can pass.

## 3. Name the server and its tools

- **Server ID** is a short name for the connection, such as `github` or `files`.
- **Prefix** is added to tool names so users can see which server provides them.

Choose a short, stable prefix. For example, the `github` prefix can produce tool names such as `github.create_issue`.

## 4. Add variables and settings

The form separates values into three groups:

- **Environment** contains values read by a local MCP process.
- **Configuration** contains normal settings, such as a region or project name.
- **Credentials** controls how the runtime authenticates to a remote MCP server.

### Server credentials

Do not paste a secret into the portal form. Store the secret as an environment variable on the runtime host and refer to it by name, for example `${GITHUB_TOKEN}`.

The advanced JSON form supports these authentication choices for the connection from the runtime to the external server:

| Choice | What the runtime sends |
| --- | --- |
| `none` | No authentication |
| `bearer_token` | A bearer token read from a runtime environment variable |
| `static_key` | A value from a runtime environment variable in a chosen header |
| `oauth_passthrough` | The signed-in MCP client's OAuth token |

OAuth passthrough is different from protecting access to the runtime. See [Protect MCP access with OAuth](oauth.md) for the client-to-runtime connection.

## 5. Test and save

1. Select **Test Connection**.
2. Confirm **Test passed** and review the discovered-tool count.
3. Select **Save MCP**.
4. Wait for the server row to show **Apply: APPLIED**.

The test runs on the customer-hosted runtime before the portal saves the configuration. A test can confirm that tools were discovered even when a credential can only be checked during the first tool call.

## 6. Review the discovered tools

1. Open **Access Control → Tools**.
2. Filter by your runtime or server.
3. Review any action marked **Needs Review**.
4. Confirm which actions are **Ready** under the runtime's protection profile.

For classification evidence, catalog changes, or corrections, see [Review Advanced access controls](advanced.md).

The profile controls the starting tool list:

- **Low** includes reviewed actions unless another setting blocks them.
- **Medium** includes reviewed read and normal-write actions.
- **High** includes reviewed read and list actions that do not change data.

Changing the profile or an individual tool setting causes a new runtime synchronization. Wait for the update to show **Applied** before testing again.

## 7. Run one tool

Use [Inspector](../quick-start.md#optional-debug-raw-mcp-behavior-with-mcp-inspector) for a direct call, or use the [Simulator](../simulator/index.md) for a plain-English request. Confirm the outcome in **Reporting**.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| **Add MCP** is disabled | Enable MCP Support in the runtime's Setup tab |
| Connection test fails | Confirm that the runtime is connected and can reach the URL or start the command |
| Docker test fails | Confirm Docker availability and socket sharing on the runtime host |
| No tools are discovered | Check the server command, URL, runtime logs, and MCP transport |
| A discovered tool is missing from the client | Review its classification, protection profile, individual state, and client role |
| Server remains pending | Wait for synchronization, then check the runtime connection and logs |

## What’s next

- [Understand profile-based tool visibility](index.md#how-tool-visibility-works)
- [Review Advanced access controls](advanced.md)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)


---

## Source document: Review Advanced Access Controls

Source: https://docs.agntid.ai/mcp/advanced/

# Review Advanced access controls

Use **Advanced** in the [AgntID portal](https://app.agntid.ai/) to review how discovered MCP actions are classified, respond to changes in a server's tool catalog, and correct a classification that does not match the action.

## When to use Advanced

Open **Advanced** when you need to:

- approve an action whose classification is waiting for review
- understand why an action has a particular operation, sensitivity, effect, or execution surface
- review tools that were added, removed, or changed after MCP discovery
- correct a system-assigned classification label
- review or withdraw an active classification correction

Classification affects which actions are eligible under a runtime's protection profile. A correction can therefore change tool visibility and trigger a runtime policy synchronization.

## Before you begin

You need:

- an organization selected in the portal
- a registered runtime in that organization
- at least one MCP server whose actions have been discovered
- permission to review classifications and make administrative corrections

Use [Add an MCP server](attach-server.md) first if the runtime has not discovered any actions.

## Open Advanced

1. In the [AgntID portal](https://app.agntid.ai/), select the organization you want to review.
2. Open **Access Control → Advanced**.
3. Select the runtime whose discovered actions you want to inspect.

Advanced has three tabs:

| Tab | Use it to |
| --- | --- |
| **Action Classifications** | Review system-assigned labels, approve pending classifications, and open an action's classification details |
| **Catalog Drift** | Review changes detected between versions of an MCP server's discovered tool catalog |
| **Classification Overrides** | Review active and inactive admin corrections, open the affected action, or withdraw a correction |

## Review action classifications

The **Action Classifications** tab groups discovered actions by tool. Expand a tool to see each action's:

- operation type
- domain
- data sensitivity
- security-relevant effects
- execution surface
- review state

Use the filters to find actions by any of these labels. The data-sensitivity filter is inclusive: for example, **HIGH or higher** also includes critical actions.

To inspect one action:

1. Expand its tool.
2. Select **View Details**.
3. Review the current labels, supporting classification evidence, confidence, corrections, and history.
4. If the review state is **PENDING_REVIEW** and the labels are correct, select **Approve Classification**.
5. Enter a clear rationale and select **Approve**.

Approving accepts the current classification. It does not create a correction.

!!! note "Taxonomy backfill"
    A **Taxonomy backfill in progress** message means some actions still use an older classification taxonomy. Wait for the backfill to finish, then select **Refresh** before completing the review.

## Correct an action label

Use a correction only when the effective classification is wrong. A correction replaces one system-assigned dimension, such as operation type, domain, blast radius, data sensitivity, criticality, privilege level, execution surface, or effects.

1. From an action's classification details, select **Correct Label**.
2. Choose the dimension to correct.
3. Select the corrected value.
4. Enter the reason for the correction.
5. If the portal warns that the review state will change, review the new state and confirm it.
6. Select **Save Correction**.

After saving, wait for runtime synchronization before testing tool visibility again. Use **Access Policies** from the action details when the classification is correct but a call needs narrower input limits.

## Review catalog drift

Catalog drift is recorded when discovery finds that tools were added, removed, or modified. The portal assigns a change risk and records how the change was handled.

1. Open **Catalog Drift**.
2. Use the status filters to find changes waiting for review or previously handled changes.
3. For a pending change, select **Review**.
4. Review the added, removed, and modified tools.
5. Choose **Accept change** to apply the discovered catalog or **Dismiss change** to reject it.
6. Enter the reason for the decision and select **Save review**.

Do not accept a change based only on its risk label. Confirm that the changed tools match the MCP server version and configuration you intended to run.

## Review or withdraw corrections

The **Classification Overrides** tab shows the system value, corrected value, rationale, and current status for each correction.

To remove an active correction:

1. Find the action and confirm the corrected dimension and rationale.
2. Select **Withdraw**.
3. Enter the reason for withdrawing it.
4. Select **Withdraw Correction**.

Withdrawing makes the system-classified value effective again and records the change in the action's history. Recheck the action's review state and runtime eligibility afterward.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No runtime is listed | Confirm the runtime belongs to the selected organization and is registered in the portal |
| No classifications are shown | Confirm an MCP server is applied and has discovered tools; clear the classification filters |
| An action is not available to a client | Check its review state, protection profile, individual tool state, OAuth role grants, and policies |
| A catalog change is not listed | Select the correct runtime, clear the drift status filter, and run discovery again |
| A correction does not affect visibility | Wait for runtime synchronization, then check the protection profile and other access controls |

## What’s next

- [Understand MCP tool visibility](index.md#how-tool-visibility-works)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)
- [Troubleshooting](../troubleshooting.md)


---

## Source document: Connect Cursor, Claude, or Codex

Source: https://docs.agntid.ai/mcp/connect-clients/

# Connect Cursor, Claude, or Codex

Connect an MCP client directly to the AgntID runtime. The runtime gives the client a profile-filtered tool list and checks every tool call before execution.

## Before you begin

Confirm that:

- the runtime is **Healthy** and **Connected**
- **MCP Support** is enabled
- at least one MCP server is **Applied**
- the client can reach the runtime MCP address

If the client runs on the runtime host, the usual address is `http://localhost:8082/mcp`. For another machine, use an address that is reachable from that machine.

## 1. Generate the configuration

1. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes** and select your runtime.
2. Open **Operations → MCP → Clients**.
3. Select **Cursor**, **Claude**, or **Codex**.
4. Select where the client runs:

    - **Same machine** uses `localhost`.
    - **Same network** uses the runtime host on your network.
    - **Custom host** lets you enter another reachable address.

5. Confirm the **Runtime MCP URL**.
6. Select **Copy Config**.

  
> Visual reference: Connect MCP Client panel generating Cursor configuration for a runtime on the same machine

Always copy the current configuration from the portal. This keeps the endpoint and OAuth scopes in sync with the runtime.

## 2. Save it in the client

| Client | Configuration file | What to do next |
| --- | --- | --- |
| **Cursor** | `~/.cursor/mcp.json` or project `.cursor/mcp.json` | Merge the generated `mcpServers` entry and reload Cursor |
| **Claude** | Project `.mcp.json` or user `~/.claude.json` | Merge the generated `mcpServers` entry and reload Claude |
| **Codex** | `~/.codex/config.toml` or project `.codex/config.toml` | Merge the generated TOML block |

Do not replace unrelated client settings. Add or merge the generated `agntid` entry.

If OAuth is required, sign in when the client asks. For Codex, run:

```bash
codex mcp login agntid
```

See [Protect MCP access with OAuth](oauth.md) before testing an authenticated connection.

## 3. Confirm the connection

1. Open the client's MCP server or tools view.
2. Confirm that `agntid` is connected.
3. List the available tools.
4. Run a safe test tool.
5. In the [AgntID portal](https://app.agntid.ai/), open **Runtimes → Runtime → Operations → MCP → Access Dashboard**.
6. Confirm the client activity and tool result.

The client sees only tools allowed by all of these controls:

1. The tool was discovered and reviewed.
2. The runtime protection profile includes the action.
3. The tool is not disabled by an individual setting.
4. When OAuth role filtering is active, the signed-in user has a matching role grant.

Policies still check the inputs and context when a visible tool is called.

## Network guidance

- Use `localhost` only when the client and runtime are on the same machine.
- Do not publish port `8082` to the internet without network protection and OAuth.
- Prefer a private network, VPN, or another approved protected route for remote clients.
- The Inspector tunnel is separate from the direct client address generated on this page.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Client cannot connect | Confirm the selected client location, host, port, and firewall rules |
| `localhost` fails | Confirm the client runs on the same machine as the runtime |
| Login opens but tools do not load | Check the OAuth credential, MCP Server Address, required scopes, and client logs |
| Expected tool is missing | Check the protection profile, classification review, individual tool state, and role grants |
| Tool is listed but the call is denied | Review the policy result in Access Dashboard or Reporting |

## What’s next

- [Protect client access with OAuth](oauth.md)
- [Add another MCP server](attach-server.md)
- [Review tool visibility](index.md#how-tool-visibility-works)


---

## Source document: Protect MCP Access with OAuth

Source: https://docs.agntid.ai/mcp/oauth/

# Protect MCP Access with OAuth

Require people and agents to sign in before they connect an MCP client to the AgntID runtime. The runtime verifies the OAuth token and can use the verified identity and roles when deciding which tools to show.

!!! warning "Direct-client validation is still pending"
    The portal and runtime steps on this page match the current product. End-to-end OAuth tests for Cursor, Claude, and Codex are still pending. Treat each client as unverified until its complete sign-in, tool-list, tool-call, and reporting flow passes.

  
> Visual reference: OAuth flow from an MCP client and identity provider to the AgntID runtime, followed by a separately authenticated connection to an external MCP server

  

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

  
> Visual reference: Runtime Security page before a validated credential is selected, with Client Access unauthenticated and Require OAuth unavailable

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

  
> Visual reference: MCP Access Dashboard before OAuth is enabled, showing Open auth and the areas used to review scope, actors, role grants, and access events

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


---

## Source document: Use the AgntID SDK

Source: https://docs.agntid.ai/sdk/

# Use the AgntID SDK

Connect Python agents to protected MCP tools. The SDK records the user request, keeps every tool call linked to it, returns clean results, and makes policy denials easy to handle.

Start with the [Python Quick Start](python.md) to run one protected tool without an AI model.

  
> Visual reference: An application using the core AgntID SDK, Microsoft Semantic Kernel, LangChain and Deep Agents, or an OAuth-enabled AWS AgentCore integration before reaching the AgntID runtime and MCP tools

  

## Choose a path

| Your goal | Start here |
| --- | --- |
| Check the SDK and runtime without an AI model | [Python Quick Start](python.md) |
| Add task tracking to your own Python tool calls | [Python SDK Guide](python-guide.md) |
| Use a `ChatCompletionAgent` | [Microsoft Semantic Kernel](msk.md) |
| Use LangChain agents or Deep Agents | [LangChain and Deep Agents](langchain.md) |
| Run LangGraph locally or on AWS AgentCore with OAuth-protected tools | [AWS AgentCore](agentcore.md) |
| Run a complete repository example | [Examples](examples.md) |
| Look up a class, function, or constant | [API Reference](api-reference.md) |

## What the SDK adds

| Feature | What it means for your application |
| --- | --- |
| **Task lifecycle** | One task records the agent, user, and original request for a run. |
| **Call correlation** | The wrapped client adds the task ID to each tool call. |
| **Protected tool discovery** | Your application receives only the tools available under the runtime's protection profile and other access controls. |
| **Prompt-aware tool binding** | Task open returns the runtime intent snapshot so the application can give the model only the tools shortlisted for the current request. |
| **Clean results** | Runtime-only fields are removed before the result returns to your agent. |
| **Clear denials** | A policy denial becomes a `DenialResult` with a readable reason. |
| **Framework context** | The LangChain adapter can also send bounded conversation, plan, delegation, and approval context. |

The SDK does not replace runtime policy. A framework may choose a tool, but the AgntID runtime still decides whether that call can run.

## Current Python support

The current source version is **0.2.0** and requires Python 3.10 or later. The base package includes the MCP client and the framework-neutral LangChain/Deep Agents adapter. Microsoft Semantic Kernel and OpenAI integrations use optional dependencies.

The published GitHub wheel is still version 0.1.1. The guides for the new adapters therefore use a source checkout until a 0.2.0 release is published.

## Basic request flow

1. Connect to the runtime MCP address.
2. Read the profile-filtered tool list.
3. Create and open one task for the user request.
4. Filter the visible tools with the task's intent snapshot before model planning.
5. Call tools through the wrapped client.
6. Let `task_context` close the task.
7. Review the result or policy denial.

## What’s next

- [Run the Python Quick Start](python.md)
- [Add Microsoft Semantic Kernel](msk.md)
- [Add LangChain or Deep Agents](langchain.md)
- [Run the AWS AgentCore example](agentcore.md)
- [Connect Cursor, Claude, or Codex](../mcp/connect-clients.md)


---

## Source document: Python SDK Quick Start

Source: https://docs.agntid.ai/sdk/python/

# Python SDK Quick Start

Connect to an AgntID runtime and run the protected `demo_add_numbers` tool. This first test uses no AI model and needs no model API key.

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


---

## Source document: Python SDK Guide

Source: https://docs.agntid.ai/sdk/python-guide/

# Python SDK Guide

Use one clear pattern for every agent request: connect, open a task, call protected tools, handle the result, and close the task.

Run the [Python Quick Start](python.md) first if you have not yet completed a protected tool call.

## How a request moves through AgntID

  
> Visual reference: SDK request flow from a user request through task open, profile-filtered tool selection, runtime policy check, MCP execution, result or denial, and task close

  

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


---

## Source document: Python SDK Examples

Source: https://docs.agntid.ai/sdk/examples/

# Python SDK Examples

Start with a test that needs no model key. Then choose the framework that matches your application.

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


---

## Source document: Microsoft Semantic Kernel

Source: https://docs.agntid.ai/sdk/msk/

# Microsoft Semantic Kernel

Turn the profile-visible MCP tools from an AgntID runtime into a Semantic Kernel plugin, then let a `ChatCompletionAgent` select and call them.

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


---

## Source document: LangChain and Deep Agents

Source: https://docs.agntid.ai/sdk/langchain/

# LangChain and Deep Agents

Run LangChain agents and Deep Agents with profile-filtered MCP tools, trusted user and agent identity, task correlation, policy checks, and clear execution evidence.

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


---

## Source document: AWS AgentCore

Source: https://docs.agntid.ai/sdk/agentcore/

# AWS AgentCore

Run a LangGraph agent locally or on Amazon Bedrock AgentCore Runtime while AgntID controls which MCP tools it can see and whether each call is allowed.

The public `agntid-python` repository now includes a complete AgentCore CLI project. It follows AWS's current `agentcore create`, `agentcore dev`, and `agentcore deploy` workflow, not the retired Python starter toolkit.

  
> Visual reference: A trusted application refreshes the signed-in user

  

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


---

## Source document: Python SDK API Reference

Source: https://docs.agntid.ai/sdk/api-reference/

# Python SDK API Reference

Current public classes, functions, result types, and constants in Python source version 0.2.0.

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


---

## Source document: Troubleshooting

Source: https://docs.agntid.ai/troubleshooting/

# Troubleshooting

Find the first part of the AgntID path that is not working, complete its checks, and then test again. Start with runtime health because Setup, tool access, Inspector, and Simulator all depend on a connected runtime.

  
> Visual reference: Troubleshooting path from Docker services and runtime connection through Setup, MCP access, testing, and Reporting

  

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


---

## Source document: Flow Diagrams

Source: https://docs.agntid.ai/flows/

# Flow Diagrams

Use these diagrams to explain how the main parts of AgntID work together. Each diagram gives a current overview; follow the linked guide for exact steps and settings.

## Choose a flow

| If you want to understand… | Start here |
| --- | --- |
| First-time runtime setup | [Quick Start flow](#quick-start-flow) |
| What runs in the portal and in your environment | [Portal and runtime](#portal-and-runtime) |
| How an MCP server reaches a client | [MCP server to client](#mcp-server-to-client) |
| How to add an MCP server | [Add an MCP server](#add-an-mcp-server) |
| Where OAuth applies | [OAuth connections](#oauth-connections) |
| How Simulator runs a request | [Simulator request](#simulator-request) |
| How an SDK request is protected | [SDK request](#sdk-request) |

## Quick Start flow

Register and deploy the runtime, complete Setup, run a protected tool, and confirm its result in Reporting. The optional branch adds input limits and compares an allowed call with a denied call.

  
> Visual reference: Quick Start flow from runtime registration through Reporting, with an optional input-limit exercise

  

[Follow the Quick Start](quick-start.md)

## Portal and runtime

The [AgntID portal](https://app.agntid.ai/) is the control plane. It manages protection profiles, detailed policies, and reporting. The customer-hosted runtime receives signed updates, filters the tool list, checks every tool call locally, and connects clients to built-in or customer MCP servers.

  
> Visual reference: AgntID portal synchronizing profiles and policies to a customer runtime that filters and protects MCP tools

  

The protection profile sets the largest tool list available from the runtime. Individual settings, OAuth role grants, and policies can reduce access further.

## MCP server to client

Add the MCP server in the portal. The runtime applies the configuration, discovers its tools, and shows a client only the tools allowed by the selected profile and any client role. Reporting records each call's result.

  
> Visual reference: MCP journey from adding a server through discovery and profile filtering to a client and Reporting

  

[Use MCP with AgntID](mcp/index.md)

## Add an MCP server

The portal stores the server configuration. The customer runtime tests the connection, discovers tools, and applies the saved configuration. You then review tool availability and run a safe test.

  
> Visual reference: Flow for adding, testing, applying, reviewing, and using an MCP server

  

[Add an MCP server](mcp/attach-server.md)

## OAuth connections

OAuth can protect incoming client access to the AgntID runtime. The runtime may use a separate credential when it connects to an external MCP server. Keeping these two connections separate helps you configure and troubleshoot them correctly.

  
> Visual reference: OAuth-protected connection from an MCP client to the AgntID runtime and a separate authenticated connection to an external MCP server

  

[Protect MCP access with OAuth](mcp/oauth.md)

## Simulator request

Simulator sends a plain-English request to the selected AI model. The model chooses from profile-visible tools, and the runtime checks the chosen call before any tool runs. Simulator then shows the result, call flow, audit details, and timing.

Use [Configure the intent engine](runtime/intent-engine.md) to choose Standard or LLM-based intent. Use [Read intent checks in Simulator](simulator/intent.md) to understand the stages shown in Call Flow.

  
> Visual reference: Simulator request moving from the portal and AI model through the customer runtime policy check to an MCP tool

  

[Run a Simulator test](simulator/index.md)

## SDK request

The SDK keeps identity and task context with a request. The runtime lists eligible tools, checks the selected tool and inputs, and returns either the tool result or a denial. Reporting keeps the outcome for review.

  
> Visual reference: SDK request from user input through task context, profile-filtered tool choice, runtime protection, tool execution, and task completion

  

[Read the Python SDK guide](sdk/python-guide.md)

## How access decisions fit together

| Layer | Purpose |
| --- | --- |
| Protection profile | Sets the largest group of tool actions the runtime can show |
| Tool review and state | Confirms the action classification and whether the tool is enabled |
| OAuth role grants | Reduce the visible actions for a verified client role |
| Policy | Checks a visible tool call and its input values |
| Runtime | Enforces the current decision before the MCP tool runs |
| Reporting | Records the allowed or denied result |

A detailed policy for one tool does not block all other tools. Each tool continues to follow its own profile, state, role grants, and policy decision.

## Related guides

- [Troubleshooting](troubleshooting.md)
- [Connect Cursor, Claude, or Codex](mcp/connect-clients.md)
- [SDK examples](sdk/examples.md)
- [Release Notes](release-notes.md)
