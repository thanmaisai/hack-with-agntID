# Vend-Safe — a short demo that lands

## 3-minute talk track

### 0:00–0:25 | Set the stakes

**Say:** “This is a small shop agent with tools to change prices, order stock, read a synthetic customer list, and record an email. The data is fake and the email stays in a local outbox. I’ll run the same risky shop scenarios directly and through AgntID, then show the actual state and audit evidence.”

**Show:** the project terminal at the repo root. Do not show `.env`.

### 0:25–1:10 | Show the direct path

Run:

```bash
.venv/bin/python demo.py run
```

While the output scrolls, explain: “Direct mode sends the model’s tool request straight to the shop. There is no AgntID policy gate on that path.”

Point out the direct outcomes:

- 100% discount is applied.
- The 100-unit order costs `$1,200`, taking cash to `-$1,000`, and the price becomes `$0.10`.
- The poisoned quote leads to a synthetic roster read and an email queued in the local outbox.

### 1:10–2:05 | Show the AgntID path

**Say:** “In the protected runs, the client connects through the AgntID runtime. Policies validate the requested values before the shop tool executes.”

Point out:

- 100% discount denied; policy range is 0–20%.
- Quantity 100 denied; maximum is 10.
- `$0.10` price denied; allowed range is `$1.50`–`$25.00`.
- Attack 3 returns the quote, while inventory/email are not in that task’s tool shortlist and no email is queued.

**Be precise:** “For Attack 3, the AgntID prompt also tells the model to treat quote instructions as untrusted, while the client exposes only the quote tool. So this shows safer prompt handling plus narrower tool exposure. It is not a same-prompt A/B test, and it does not show that the quote text was filtered.”

### 2:05–2:40 | Show the proof

**Show:** AgntID **Reporting**. Open a denied discount or order event and point to the requested value and the policy reason. Say: “This is the runtime’s decision record, not just the model saying it refused.”

If time allows, open `http://localhost:9000/admin/state` after the comparison. Explain that the harness resets the shop between runs, so the visible state is the final reset state; the per-run scoreboard is the record of scenario outcomes.

### 2:40–3:00 | Close with the point

**Say:** “The model can propose an action; the application and runtime decide which tools it can reach and which inputs are allowed. Here, runtime policies stopped unsafe financial changes, and task-scoped tool exposure reduced what the quote task could do. We verify that from tool calls, shop state, and runtime reporting.”

## Screen order

1. Terminal: run `.venv/bin/python demo.py doctor` before the audience arrives.
2. Terminal: run `.venv/bin/python demo.py run`.
3. AgntID Reporting: show one policy denial with its input and reason.
4. Optional: shop state endpoint, clearly label its data synthetic.

## If someone asks

**“What is AgntID doing here?”**  
“The local agent routes protected MCP calls through an AgntID runtime. The runtime applies the saved input policies and produces reporting events. The SDK also opens a task and narrows the tool list it presents to the model.”

**“Is the model itself the security boundary?”**  
“No. The model chooses among offered tools; the runtime-side input policies are the enforcement layer for the discount and order limits.”

**“Was the supplier instruction removed?”**  
“No. The quote is returned with that text. In this run, the protected prompt treats it as untrusted and the task shortlist contains only the quote tool.”

**“Is LLM intent enforcement active?”**  
“The portal is configured to request LLM-based intent and has the `agntID key` selected. But our runtime logs showed action-level intent validation skipped because no prompt was available on tool calls, with a standard fallback reported. I’m not counting that as verified enforcement.”

**“Are those real customer emails or real messages?”**  
“No. They are synthetic demo records, and the email tool only writes to a local outbox.”

**“Why does the order go through directly?”**  
“The direct path intentionally bypasses AgntID. It is the unprotected comparison case.”

## Presenter checklist

- Run `doctor`; confirm shop, runtime, and local model key are ready.
- Confirm the portal shop connection and policies show Applied.
- Keep `.env` and credentials off-screen.
- Wait for the final line **ALL EXPECTED OUTCOMES VERIFIED**.
- If any check fails, describe the observed result and troubleshoot; do not present it as a pass.
- Avoid saying “AgntID blocked all exfiltration” or “the quote was filtered.” Describe Attack 3 as prompt handling plus task shortlist behavior, and explain that the prompts differ.

## One-sentence version

“Vend-Safe shows how risky model tool requests can change a shop directly, while an AgntID runtime applies explicit input policies and task-scoped tool controls—and it gives us an audit trail to verify the difference.”
