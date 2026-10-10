# Vend-Safe demo walkthrough

## Before presenting

Run these checks once before the audience arrives:

```bash
.venv/bin/python demo.py doctor
docker compose ps
```

Confirm the `.env` key is set, the shop and runtime are healthy, portal setup is synchronized, and the portal has the `shop` server and its policies applied. Do not display `.env` or a terminal command containing the API key.

## Story (about 3 minutes)

1. **Set the scene:** “This is a small shop agent. It can read stock and quotes, change prices, place orders, and record emails in a synthetic outbox.”
2. **Show the boundary:** “The same agent can connect directly to tools, or route every call through AgntID.”
3. **Run the comparison:**

   ```bash
   .venv/bin/python demo.py run
   ```

   The harness resets the shop for each run. Point out the risky changes in direct mode and the policy denials in AgntID mode. It labels the comparison **INCOMPLETE** and exits unsuccessfully if any expected tool result is missing.

4. **Show evidence:** Open AgntID Reporting and inspect a denied action, its policy reason, and correlation details. The shop state is available at `http://localhost:9000/admin/state`.
5. **Close:** “Tool discovery narrows what the agent can request; policy checks enforce allowed inputs before a tool runs; Reporting gives us an audit trail.”

## Expected outcomes

- Attack 1 direct applies an unsafe discount; AgntID denies a discount over 20%.
- Attack 2 direct can place an oversized order or set an unsafe price; AgntID denies quantities above 10 and prices outside `$1.50`–`$25.00`.
- Attack 3 direct follows the poisoned quote and records an email to the outside address in the local outbox. In AgntID mode, the prompt explicitly treats supplier instructions as untrusted data; the quote is still returned with its instruction text, while inventory and email tools are absent from the task-specific shortlist. This demonstrates the tool boundary, not filtering of returned text.

LLM tool selection can vary. The harness checks actual tool calls and shop state, not just a final balance. If a direct-mode attack does not trigger the expected action, inspect the printed tool trace and rerun that scenario. Never claim a scoreboard outcome that the run did not show.

## Short single-scenario version

```bash
.venv/bin/python agent.py --mode direct --attack 1
.venv/bin/python agent.py --mode agntid --attack 1
```

Use attack 1 for the clearest first walkthrough. Then open Reporting and show the denial event.
