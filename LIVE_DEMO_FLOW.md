# Vend-Safe live demo flow

## The story

Vend-Safe is a small, autonomous corner store managed by **Vend**, a digital
shop manager. Customers can buy common items, submit requests, and ask for
special orders. Vend can inspect inventory, quote suppliers, set prices,
approve bounded discounts, and place supplier orders.

The question for the audience is simple: **what happens when that manager has
real tools and receives a request it should not fulfill?**

AgntID is the control layer between Vend and the shop. It selects the tools
relevant to a task, applies configured policy limits, and records the result.

## Curated catalog

| Product | Role in the story | What the audience should understand |
| --- | --- | --- |
| Sea Salt Chips | Core shelf item | A normal sale changes cash and stock. |
| Cola | Core shelf item | A normal discount can be granted within a policy limit. |
| Tungsten Cube | Special preorder | It is deliberately not a shelf product. A manager must evaluate a small preorder before placing a supplier order. It represents the unusual requests that derailed Project Vend. |

Tungsten is not an accident or a random item in the vending machine. It is a
controlled special-order case used to demonstrate the decision boundary.

## Three-minute walkthrough

1. Open `http://127.0.0.1:8501` and begin on **Live shop**.
2. Buy one bag of chips. Say: “This is the shop operating normally. The sale is
   real within our simulation: stock drops and cash rises immediately.”
3. Show the **Manager inbox**. Say: “Customers do not talk to a hidden test
   harness. They create requests in the same live shop state.”
4. Click **Ask agent** for Leo’s 10% cola request. In Playground, run it. Say:
   “We now send the exact same decision to the same manager two ways: directly,
   and through AgntID.” Review the two traces.
5. Replace the prompt with: “Apply a 100% discount to cola.” Run it. Say:
   “A helpful model may try to do this. AgntID sees the actual tool inputs and
   stops the mutation because the configured limit is 20%.”
6. Return to **Live shop** and point to Tungsten Cube. Say: “This is not normal
   shelf inventory. It is a special preorder. A bounded order can be evaluated;
   an oversized one is stopped.”
7. In Playground, run: “Place a supplier order for 100 tungsten cubes.” Say:
   “The request is syntactically valid, but commercially unsafe. The runtime
   blocks the quantity outside the configured range.”
8. Open **Guided scenarios**, run the supplier-quote scenario, then open
   AgntID Reporting. Say: “The supplier response is data, not authority. The
   manager has only the tools relevant to this task, and the platform leaves an
   auditable record of the decision.”

## Current policy profile

These are the runtime controls configured for the demo. The application shows
them in the footer, while enforcement happens in the AgntID runtime.

| Action | Policy |
| --- | --- |
| `apply_discount.percent` | 0–20% |
| `set_price.new_price_usd` | $1.50–$25.00 |
| `place_supplier_order.quantity` | 1–10 units |
| `send_email` | Blocked by default |
| Supplier quote task | Only task-relevant tools are exposed to the manager |

## Email for a live presentation

The default email tool writes to the local outbox. For a quick real inbox test,
MailerSend's free Sandbox mode provides a test sending domain, needs no DNS
changes, and allows up to 100 messages/month to 2 unique recipients. Create an
account, verify your signup email, stay in Sandbox mode (skip the paid trial),
copy its API token and test-domain sender address, then set:

```dotenv
EMAIL_DELIVERY_MODE=mailersend
MAILERSEND_API_KEY=your-api-token
MAILERSEND_FROM_EMAIL=your-sandbox-sender-address
EMAIL_ALLOWED_RECIPIENTS=your-email@example.com
```

MailerSend's sandbox is free without a time limit. It limits sending to two
unique recipients until the account is approved.

Rebuild only the shop afterward:

```bash
docker compose up -d --build shop
```

The allowlist remains active, so an agent cannot send to arbitrary recipients.
