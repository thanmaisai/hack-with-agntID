# FEEDBACK.md — Vend-Safe build log

Log of issues encountered while building. Each entry: scenario, what was tried, what happened, workaround, requested feature.

---

## 1. Cumulative limits not expressible

**Scenario**: Attack 2 allows ten separate orders of 10 cubes each — each passes the per-call cap of 10, but together they drain $1,200.

**Tried**: Looking for a cross-call or per-task budget limit in Access Control.

**Happened**: Only per-call numeric ranges are documented. No daily, per-task, or aggregate spend limit exists.

**Workaround**: None available in the runtime. Documented the gap.

**Requested feature**: Daily or per-task spend/quantity cumulative cap enforced by the runtime, not by the agent.

---

## 2. Allowlists and cost-floor rules not expressible

**Scenario**: Wanted to express "price must be above item cost" and "supplier must be in an approved list."

**Tried**: Reviewing all policy configuration options in Access Control.

**Happened**: Only min/max numeric ranges are documented and available. Approved-supplier allowlists and relative rules (e.g., price > cost field) cannot be expressed.

**Workaround**: None. Noted as *undocumented* rather than *missing* pending further review.

**Requested feature**: String allowlists and cross-field comparison rules in policy configuration.

---

## 3. Caller trust — message role vs. tool client role

**Scenario**: Attack 1 has a customer claiming to be the CEO in the message body. Wanted to refuse the discount on that basis.

**Tried**: Reviewing role grants and access control scopes.

**Happened**: Role grants apply to the MCP client identity (agent), not to the message author. A customer claiming to be the CEO in the prompt text cannot be distinguished from the agent at the tool-call boundary.

**Workaround**: Policy limit on `percent` (max 20) prevents the exploit regardless of claimed identity.

**Requested feature**: Per-prompt-author role annotation that flows through the task context.

---

## 4. Approval flow for plain MCP agents

**Scenario**: Wanted to add a human-approval pause before large orders.

**Tried**: Searching approval flow documentation for plain MCP (non-Deep Agents) usage.

**Happened**: Approval appears to be documented only in the Deep Agents example. Not clear if it is available to plain MCP + agntid SDK without using LangChain/Deep Agents.

**Workaround**: Not implemented for this build. Documented as *undocumented* for plain MCP path.

**Requested feature**: Approval flow documented and available for plain OpenAI function-calling agents using the core SDK.

---

## 5. Policy dry-run / preview mode

**Scenario**: Before saving policies, wanted to verify what calls would be denied without affecting live traffic.

**Tried**: Looking for a simulation or dry-run option in Access Control → Access Policies.

**Happened**: No dry-run or preview mode found. Changes go live on next sync.

**Workaround**: Tested in Simulator before enabling enforcement for the attack runs.

**Requested feature**: Policy dry-run that shows allow/deny decisions against sample inputs before enforcement is applied.
