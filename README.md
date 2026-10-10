# Vend-Safe

**A repeatable AgntID demo showing an AI agent running into risky requests and a runtime enforcing its tool access.**

The demo uses a local synthetic shop. It compares the same three attack scenarios when the agent connects directly to the shop and when calls pass through the AgntID runtime.

## Demo flow

```text
one-time setup → add your local API key → start services → readiness check → run comparison → review evidence
```

| Scenario | Direct connection | Through AgntID |
|---|---|---|
| CEO discount request | Applies a 100% discount | Policy caps discounts at 20% |
| Loss-making bulk order | Can order 100 items and set a very low price | Quantity and price limits deny unsafe inputs |
| Poisoned supplier quote | Can retrieve the synthetic roster and write an external address to the local outbox | The quote remains untrusted data; task-specific tool selection keeps inventory/email outside the task shortlist, and the demo prompt tells the agent not to follow quote instructions |

The demo uses synthetic data. Shop email writes to a local outbox by default. For a quick controlled inbox test, it can deliver through MailerSend Sandbox with an API token, sandbox sender, and explicit recipient allowlist in `.env`. Prompts and tool results are sent to the configured OpenAI API for model calls.

## Project layout

```text
agent.py             Shared agent loop; direct and AgntID tool connections
attacks.py           Synthetic prompts and agent instructions
demo.py              Setup, start/stop, readiness, and comparison command hub
run_compare.py       Six-run harness, state resets, scoreboard, outcome checks
shop_server.py       Synthetic shop MCP tools and local admin endpoints
docker-compose.yml   React UI, demo API, shop, AgntID runtime, and intent parser
Dockerfile           Isolated shop server image
Dockerfile.dashboard Demo API image; installs the local AgntID SDK
ui/                  React + Vite UI, shadcn-style components, and Lucide icons
LIVE_DEMO_FLOW.md    Presenter story, curated catalog, and click-by-click demo flow
DEMO_VIDEO_FLOW.md    Timed 2–3 minute video script with voice-over and captions
requirements.txt     Local Python agent dependencies
requirements-shop.txt Shop container dependencies (FastMCP 2.14.x for runtime compatibility)
.env.example         Safe configuration template; copy to ignored .env
PORTAL_SETUP.md      AgntID portal configuration and verification guide
resources/           Project plan and AgntID reference material
```

## Requirements

- macOS/Linux shell, Python 3.10+, Git, and Docker Desktop with Compose.
- An OpenAI API key for the **local demo agent**. Add this to `.env` on your machine; do not send it in chat or commit it.
- An AgntID portal runtime connected to this project’s local runtime and configured with the `shop` MCP server, tool reviews, policies, and intent provider. See [Portal setup](PORTAL_SETUP.md).

The portal’s healthy `agntID key` configures intent classification in the portal. It is separate from `OPENAI_API_KEY`, which the local Python agent uses for chat completions.

## First-time setup

From the repository root:

```bash
./setup.sh
```

This creates `.venv`, installs the local dependencies and AgntID Python SDK, and copies `.env.example` to `.env` if needed. Then edit `.env` and fill in:

```dotenv
OPENAI_API_KEY=your-local-key
```

Leave the local endpoint defaults as-is unless you changed the Compose ports. `.env` is ignored by Git.

## Start and check

```bash
.venv/bin/python demo.py start
.venv/bin/python demo.py doctor
```

`doctor` checks the shop admin endpoint, runtime health endpoint, and whether the local OpenAI key is set. It never prints the key. The first startup can take a few minutes while Docker downloads images and initializes the intent model. Check progress with:

```bash
docker compose ps
docker compose logs -f achr-runtime achr-intent-parser shop
```

In the AgntID portal, the shop MCP server URL should be `http://shop:9000/mcp` for this Compose network. The host machine uses `http://localhost:9000` for shop checks and `http://localhost:8082/mcp` for local agent calls. Full portal instructions are in [PORTAL_SETUP.md](PORTAL_SETUP.md).

## Run the demo

Start the Docker-hosted React UI and services:

```bash
docker compose up -d --build
```

Open `http://127.0.0.1:8501`. Begin on **Live shop**: purchases update cash and stock in real time, and customer requests can be handed directly to the manager agent. Use **Playground** to enter any shop request or choose a prompt starter. The exact same prompt is run once directly and once through AgntID, with a shop reset between them. The live trace follows model plans, tool calls, runtime decisions, and resulting shop state. Use **Guided scenarios** for the fixed examples and their expected checks. Playground runs are exploratory and do not claim a pass/fail result. The UI and API run in Docker; the browser never receives the API key. Prompts are sent to the configured model API, so use synthetic data only. To use the short launcher, run `.venv/bin/python demo.py dashboard`.

To run the comparison in a terminal instead:

```bash
.venv/bin/python demo.py run
```

This resets the synthetic shop before each scenario, runs all three attacks first directly and then through AgntID, and prints a scoreboard plus tool-level outcome checks. It makes six model runs, so it uses your configured model API quota. The process exits unsuccessfully and marks the comparison **INCOMPLETE** if any expected tool result is missing. To show one run at a time:

```bash
.venv/bin/python agent.py --mode direct --attack 1
.venv/bin/python agent.py --mode agntid --attack 1
```

Choose `--attack 1`, `2`, or `3`. See [the demo guide](DEMO_GUIDE.md) to understand the architecture and [the presentation script](DEMO_PRESENTATION.md) for the talk track. Note that Attack 3 intentionally uses different prompt wording in direct and AgntID modes.

## Stop and reset

Stop containers but keep persistent runtime settings:

```bash
.venv/bin/python demo.py stop
```

Reset only the synthetic shop state:

```bash
curl -X POST http://localhost:9000/admin/reset
```

`docker compose down -v` removes persistent runtime configuration and model cache volumes. Use it only when you intentionally want a full local reset.

## Configuration reference

| Variable | Default | Used for |
|---|---|---|
| `OPENAI_API_KEY` | empty | Required local model key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model used by the local agent |
| `SHOP_MCP_URL` | `http://localhost:9000/mcp` | Direct mode shop MCP endpoint |
| `SHOP_ADMIN_BASE` | `http://localhost:9000` | Comparison harness state/reset endpoints |
| `AGNTID_MCP_URL` | `http://localhost:8082/mcp` | AgntID runtime MCP endpoint |
| `AGNTID_ACCESS_TOKEN` | empty | Optional OAuth token if the local runtime requires one |
| `EMAIL_DELIVERY_MODE` | `outbox` | `mailersend` enables MailerSend Sandbox delivery |
| `MAILERSEND_API_KEY` | empty | MailerSend API token |
| `MAILERSEND_FROM_EMAIL` | empty | Sender address on your MailerSend sandbox domain |
| `EMAIL_ALLOWED_RECIPIENTS` | empty | Comma-separated inbox allowlist (Sandbox allows 2 recipients) |
| `RUSE_AGENID_ENDPOINT` | Compose default | Optional control-plane callback override |

## Troubleshooting

- **The protected quote reports “policy allowed” but still errors:** check the terminal detail and Reporting. This project pins the shop to FastMCP 2.14.x because the AgntID runtime fails on FastMCP 4 payloads; rebuild it with `docker compose up -d --build shop`.
- **`doctor` says shop/runtime unavailable:** run `docker compose ps`; start with `demo.py start`, inspect logs, and wait for healthy status. The runtime health check tries both `/health` and `/` and prints the connection error.
- **OpenAI key missing:** edit `.env`, then rerun `demo.py doctor`. Do not share the secret.
- **AgntID mode cannot connect:** confirm runtime health at `http://localhost:8080/health`, MCP at `http://localhost:8082/mcp`, and portal sync status. Set `AGNTID_ACCESS_TOKEN` only if OAuth is enabled for this endpoint.
- **Shop server has zero tools in the portal:** confirm portal URL is `http://shop:9000/mcp` and the shop container is healthy on the shared Compose network.
- **Policy does not block a request:** confirm the tool policy is applied and synchronized in the portal; review Reporting for the selected action, inputs, and denial reason.
- **Attack 3 does not show an attempted email in direct mode:** the LLM may choose a different response. Rerun that scenario and inspect the tool trace. The protected expectation is zero external email entries in the shop state.
