---
title: Configure the intent engine
last_verified: 2026-10-09
owner: docs-team
---

<div class="page-intro" markdown>

# Configure the intent engine

Choose the intent mode that matches the complexity of the user's request, then use the [Simulator](../simulator/index.md) to verify which mode protected the run.

</div>

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
