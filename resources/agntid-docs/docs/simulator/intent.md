---
title: Read intent checks in Simulator
last_verified: 2026-10-09
owner: docs-team
---

<div class="page-intro" markdown>

# Read intent checks in Simulator

Use this page to understand the intent stages shown during a Simulator run. To configure Standard or LLM-based intent on a runtime, see [Configure the intent engine](../runtime/intent-engine.md).

</div>

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
