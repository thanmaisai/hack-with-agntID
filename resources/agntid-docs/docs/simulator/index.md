---
title: Simulator
last_verified: 2026-10-09
owner: docs-team
---

<div class="page-intro" markdown>

# Simulator

Use the Simulator to send a plain-English request to an AI model and see how AgntID protects each tool call. This guide connects a runtime, runs one allowed request and one denied request, and reviews the result. It takes about 10 minutes after the [Quick Start](../quick-start.md) is complete.

</div>

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/simulator-journey.svg" alt="Simulator journey from preparation and connection to an allowed or denied request and review" />
  <img class="diagram-dark" src="../../assets/diagrams/simulator-journey-dark.svg" alt="Simulator journey from preparation and connection to an allowed or denied request and review" />
</div>

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

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/01-simulation-enabled.png" alt="Runtime Configuration with Simulation System enabled and Save Configuration available" />
</div>

Next, open **Access Control → Credentials**. Add a credential for your AI provider if you do not already have one. Save it and confirm that its status is **Healthy**. Never include the secret value in screenshots, tickets, or source control.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/02-llm-credential.png" alt="Credentials page with a healthy Simulator Demo AI model credential" />
</div>

AgntID securely provides the selected credential to the customer-hosted runtime for the simulation session.

## 2. Connect the Simulator

1. Open **Observe & Validate → Simulator**.
2. Select the runtime you prepared.
3. Select the AI model credential.
4. Keep the default model, or choose another available model.
5. Select **Connect**.

The model list depends on your provider and can change. The portal selects a default model automatically.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/03-session-setup.png" alt="Simulator session setup with a runtime, AI model credential, default model, and Connect button" />
</div>

After the connection succeeds, a request box and **Run** button appear.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/04-connected.png" alt="Connected Simulator with a plain-English request box and Run button" />
</div>

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../../assets/diagrams/simulator-runtime-flow.svg" alt="A Simulator request moving from the AgntID portal through the customer runtime policy check to an MCP tool" />
  <img class="diagram-dark" src="../../assets/diagrams/simulator-runtime-flow-dark.svg" alt="A Simulator request moving from the AgntID portal through the customer runtime policy check to an MCP tool" />
</div>

## 3. Run an allowed request

Enter this request and select **Run**:

```text
Use demo.add_numbers to add 11 and 21
```

Both values are within the policy limits, so the runtime allows the tool call. The **Results** tab shows **Query Results**, a green **Success** badge, and the result `32`.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/05-allowed-result.png" alt="Simulator Results tab showing a successful demo.add_numbers request and result 32" />
</div>

The tool name is included because this runtime has more than one addition tool. Naming the tool makes the example repeatable. For normal testing, you can use a request without a tool name and see which profile-visible tool the model selects.

## 4. Run a denied request

Enter this request and select **Run**:

```text
Use demo.add_numbers to add 50 and 21
```

`first_number` is outside the allowed range of 10 to 20. The runtime blocks the tool before it runs. The **Results** tab shows **Execution Denied**, **AgntID Policy Denied**, and the failed input rule.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/06-denied-result.png" alt="Simulator Results tab showing demo.add_numbers denied because first_number is outside its allowed range" />
</div>

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

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/07-denied-call-flow.png" alt="Simulator Call Flow tab showing passed steps followed by a denied policy step" />
</div>

The Audit tab shows the policy decision and the tool involved. It provides evidence that the denial happened before tool execution.

<div class="quick-start-screenshot">
  <img src="../../assets/simulator-2/08-denied-audit.png" alt="Simulator Audit Trail with passed guardrail and intent checks and a denied policy evaluation" />
</div>

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
