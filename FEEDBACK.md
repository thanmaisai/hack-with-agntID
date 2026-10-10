# AgntID platform feedback from Vend-Safe

Thanks for building AgntID. We used a local MCP shop and a plain Python/OpenAI function-calling agent to test runtime policies, task setup, tool selection, and reporting. This feedback is limited to behaviors we reproduced in the demo; local setup mistakes are intentionally excluded.

**Test context:** 10 October 2026; local AgntID runtime image `ghcr.io/agntid-ai/achr-runtime:main`; shop initially on FastMCP 4.1.0, then pinned to FastMCP 2.14.7 for the working run; Python MCP SDK integration. The portal runtime settings showed LLM-based intent selected with the `agntID key` credential.

## 1. Task prompt is not visible to action-level intent validation

**Priority:** High — affects whether intent controls can be relied on for plain MCP agents.

**What we did:** Opened a task through the AgntID Python SDK with the complete user prompt, then made a tool call through the SDK’s wrapped MCP client with the task ID attached.

**What we observed:** Tool calls were processed and policies ran, but runtime logs repeatedly reported `prompt_length=0` and `No prompt available - skipping intent validation (graceful degradation)`. For example, the quote and discount tool calls entered the intent flow but intent validation was skipped.

**Why it matters:** The portal can show an intent engine configured while action-level validation for this execution path does not receive the task prompt. A developer may assume intent was evaluated when it was actually skipped.

**Suggested improvement:** Ensure task-open prompt context is correlated with subsequent MCP calls in the documented plain MCP/SDK flow. If that is not supported, document the required context propagation explicitly and provide a clear, configurable fail-closed option for cases where intent validation is required.

**Evidence/verification:** Runtime log entries during our successful runs contained `prompt_length=0` and `No prompt available - skipping intent validation`; input policies still correctly denied the unsafe discount and order values.

## 2. Configured intent engine and effective engine are hard to reconcile

**Priority:** High — configuration and observability clarity.

**What we did:** Selected **LLM-based** intent in the portal Settings page and selected the healthy `agntID key` credential.

**What we observed:** The UI showed LLM-based selected. Runtime sync logs later reported `Applying intent_config from portal sync (engine=contextual)` and `Intent engine selection applied (engine=contextual fallback=standard)`. Tool-call logs also showed intent validation skipped because no prompt was available.

**Why it matters:** It was difficult to tell whether `contextual` is the expected runtime mapping for the portal’s LLM-based option, whether the configured provider was actually used, or whether execution fell back. We do not claim the mapping itself is a defect; the effective behavior was not clear from the UI and logs.

**Suggested improvement:** Show the effective engine/provider and model used by the runtime, credential health, fallback state/reason, and per-call outcome in one place. Make skipped validation visually distinct from a successful intent decision, and surface a warning when the selected engine cannot evaluate a call.

**Evidence/verification:** Portal Settings showed LLM-based plus `agntID key`; runtime logs showed the engine/fallback messages above and skipped intent decisions. We therefore did not present runtime-side LLM intent as verified protection in the demo.

## 3. FastMCP 4 upstream response failed with an opaque runtime error

**Priority:** Medium — MCP ecosystem compatibility and diagnostics.

**What we did:** Connected the local shop, initially using FastMCP 4.1.0, as an upstream MCP server in the AgntID runtime and called its supplier-quote tool.

**What we observed:** The portal/runtime recorded policy evaluation as allowed, but tool execution failed with `No module named 'fastmcp.server.providers.prefab_payload'`. The same shop worked after pinning its server to FastMCP 2.14.7 and using the Compose-network URL `http://shop:9000/mcp`.

**Why it matters:** The policy result and upstream execution failure looked contradictory at first and were easy to misread as a policy denial. The compatibility issue was diagnosable only after inspecting the underlying runtime error.

**Suggested improvement:** Validate supported upstream MCP/FastMCP versions during connection testing, or return an actionable incompatibility message that distinguishes policy evaluation from upstream transport/result parsing failures. A compatibility matrix for supported server SDK versions would also help.

**Evidence/verification:** FastMCP 4.1.0 produced the missing-module error; rebuilding the shop with FastMCP 2.14.7 and changing the endpoint to `http://shop:9000/mcp` made the quote call succeed. The connection test then discovered seven tools and showed Applied.

## Scope note

The demo also uncovered local integration mistakes: our Python client initially unpacked the MCP transport result incorrectly, and the portal upstream URL initially used a host-only address that was unreachable from the Compose runtime. Those were project configuration/code issues, not AgntID product gaps, so they are not included as platform feedback.

We also have ideas such as cumulative budgets, allowlists, approval flows, and policy previews. We have not verified their availability across current plans/configurations or reproduced them as blockers in this integration, so they are omitted from this issue-focused report.
