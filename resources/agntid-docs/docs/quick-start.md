---
title: Quick Start
last_verified: 2026-03-10
owner: docs-team
version: "2"
---

<div class="page-intro" markdown>

# Quick Start

Deploy a customer-hosted AgntID runtime, add input limits to a built-in MCP tool, simulate AI-agent requests, and verify that AgntID allows or denies tool execution before the tool runs. The required path takes about 15 minutes, plus the first model download.

</div>

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/quick-start-flow.svg" alt="Runtime setup, profile review, demo tool availability, input policy, Simulator allowed and denied calls, and Reporting audit; MCP Inspector is an optional debugging branch" />
  <img class="diagram-dark" src="../assets/diagrams/quick-start-flow-dark.svg" alt="Runtime setup, profile review, demo tool availability, input policy, Simulator allowed and denied calls, and Reporting audit; MCP Inspector is an optional debugging branch" />
</div>

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

<div class="quick-start-screenshot">
  <img src="../assets/quick-start-2/01-register-runtime.png" alt="Register Runtime dialog with the Quick Start Runtime name, before the bootstrap token is shown" />
</div>

**Checkpoint:** The portal lists `Quick Start Runtime`, and you have its bootstrap token ready for connection.

## 3. Connect the runtime

1. Open the **local runtime UI** at [http://localhost:8080](http://localhost:8080).

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/02-local-runtime-connect.png" alt="Local runtime UI ready for a bootstrap token" />
    </div>

2. Paste the bootstrap token and select **Connect to Control Plane**.
3. Confirm that the local runtime UI shows **Operational** and **Connected**.

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/03-local-runtime-operational.png" alt="Local runtime UI showing Operational and Connected status" />
    </div>

4. Return to **Runtimes** in the [AgntID portal](https://app.agntid.ai/) and open `Quick Start Runtime`.

The AgntID portal is the control plane. The local runtime UI runs on your machine and shows whether the runtime is connected and ready.

<div class="diagram-container" style="max-width:100%">
  <img class="diagram-light" src="../assets/diagrams/architecture-flow.svg" alt="AgntID portal synchronizing profiles and policies to a customer runtime that filters and enforces access to MCP servers" />
  <img class="diagram-dark" src="../assets/diagrams/architecture-flow-dark.svg" alt="AgntID portal synchronizing profiles and policies to a customer runtime that filters and enforces access to MCP servers" />
</div>

**Checkpoint:** The local runtime UI shows **Operational** and **Connected**.

## 4. Complete Setup and review the profile

1. Open the runtime's **Setup** tab. Its five rows are **Runtime Registered**, **Runtime Healthy**, **MCP Support**, **CLI Enforcement**, and **Protection Profile**.

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/04-setup-profile-next.png" alt="Runtime Setup tab showing four of five checks complete and Protection Profile as the next step" />
    </div>

2. Leave optional CLI enforcement off for this quick start. The built-in `demo` MCP server is already available.
3. Open **Protection Profile**, review **Medium / READ_WRITE**, and mark the profile reviewed.

    | Profile | Actions available after review |
    | --- | --- |
    | Low | All reviewed actions can run unless a policy blocks them |
    | Medium | Reviewed read and normal-write actions can run. Delete, execute, and other high-impact actions cannot run. |
    | High | Only reviewed read and list actions that do not change data can run |

    The protection profile controls the largest set of tool actions the runtime may expose. Tool policies then decide whether a specific visible tool call is allowed based on details such as inputs.

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/05-medium-profile-review.png" alt="Protection Profile Review with Medium selected, the projected enabled and disabled action counts, classification review status, and saved runtime settings applied" />
    </div>

4. Confirm **5 of 5** setup checks and **Runtime sync: Applied**.

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/06-setup-complete.png" alt="Runtime Setup tab showing all five setup checks complete" />
    </div>

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

    <div class="quick-start-screenshot">
      <img src="../assets/quick-start-2/08-baseline-input-constraints.png" alt="Baseline policy for demo.add_numbers with input ranges 10 to 20 and 20 to 30" />
    </div>

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

    <div class="quick-start-screenshot">
      <img src="../assets/simulator-2/03-session-setup.png" alt="Simulator setup with a runtime, healthy model credential, selected model, and Connect button" />
    </div>

8. Enter this allowed prompt and select **Run**:

    ```text
    Use demo.add_numbers to add 11 and 21.
    ```

9. Confirm **Success** and `Result: 32` in **Results**.

    <div class="quick-start-screenshot">
      <img src="../assets/simulator-2/05-allowed-result.png" alt="Simulator showing Success and result 32 for demo.add_numbers with inputs 11 and 21" />
    </div>

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

    <div class="quick-start-screenshot">
      <img src="../assets/simulator-2/06-denied-result.png" alt="Simulator showing AgntID Policy Denied because first_number 50 violates the input limits" />
    </div>

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
