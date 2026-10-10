1. Prepare and deploy runtime 2.0.0¶
Create a clean working directory.


Linux / macOS
Windows PowerShell

mkdir agntid-runtime
cd agntid-runtime

Download the customer compose file.


Linux / macOS
Windows PowerShell

curl -L -o docker-compose.yml https://raw.githubusercontent.com/AGNTID-AI/agntid-python/main/docker-compose.yml

Start both services. The runtime images are public on GitHub Container Registry, so no registry login is required.


docker compose up -d
Wait for both services to report healthy.


docker compose ps
If either service remains unhealthy, run docker compose logs -f and see Troubleshooting.

Checkpoint: docker compose ps shows both services as healthy.

2. Register a runtime¶
In the AgntID portal, open Runtimes and select Add Runtime.
Name it Quick Start Runtime, then generate its bootstrap token.
Copy the token and use it in the next step to connect your prepared runtime. Treat it like a password; do not paste it into tickets, chat, screenshots, or source control.
The token is shown only for bootstrapping this runtime.

Register Runtime dialog with the Quick Start Runtime name, before the bootstrap token is shown
Checkpoint: The portal lists Quick Start Runtime, and you have its bootstrap token ready for connection.

3. Connect the runtime¶
Open the local runtime UI at http://localhost:8080.

Local runtime UI ready for a bootstrap token
Paste the bootstrap token and select Connect to Control Plane.

Confirm that the local runtime UI shows Operational and Connected.

Local runtime UI showing Operational and Connected status
Return to Runtimes in the AgntID portal and open Quick Start Runtime.

The AgntID portal is the control plane. The local runtime UI runs on your machine and shows whether the runtime is connected and ready.

AgntID portal synchronizing profiles and policies to a customer runtime that filters and enforces access to MCP servers
Checkpoint: The local runtime UI shows Operational and Connected.

4. Complete Setup and review the profile¶
Open the runtime's Setup tab. Its five rows are Runtime Registered, Runtime Healthy, MCP Support, CLI Enforcement, and Protection Profile.

Runtime Setup tab showing four of five checks complete and Protection Profile as the next step
Leave optional CLI enforcement off for this quick start. The built-in demo MCP server is already available.

Open Protection Profile, review Medium / READ_WRITE, and mark the profile reviewed.

Profile	Actions available after review
Low	All reviewed actions can run unless a policy blocks them
Medium	Reviewed read and normal-write actions can run. Delete, execute, and other high-impact actions cannot run.
High	Only reviewed read and list actions that do not change data can run
The protection profile controls the largest set of tool actions the runtime may expose. Tool policies then decide whether a specific visible tool call is allowed based on details such as inputs.

Protection Profile Review with Medium selected, the projected enabled and disabled action counts, classification review status, and saved runtime settings applied
Confirm 5 of 5 setup checks and Runtime sync: Applied.

Runtime Setup tab showing all five setup checks complete
Checkpoint: Setup shows 5 of 5 complete and Runtime sync: Applied.

5. Confirm demo MCP tools are available¶
In the portal, open Quick Start Runtime.
Open Operations → MCP → Servers.
Confirm the built-in demo MCP server is enabled and connected.
Confirm demo.add_numbers is available.
If you made any changes, wait for Runtime sync: Applied.
Checkpoint: You have a healthy runtime with the demo MCP server available. Do not test the tool yet; first add a policy so the test demonstrates enforcement.

6. Add input limits to demo.add_numbers¶
Now add a simple policy that makes one call succeed and another call fail. This creates a clear end-to-end enforcement test.

Open Access Control → Access Policies.
Select the demo server.
Select demo.add_numbers.
Open the Baseline Allow Policy.
Add these input constraints:

Input	Minimum	Maximum
first_number	10	20
second_number	20	30
Baseline policy for demo.add_numbers with input ranges 10 to 20 and 20 to 30
Save the policy.

Wait for Runtime sync: Applied. The runtime signs policy changes automatically during synchronization.
Checkpoint: demo.add_numbers has input limits for both inputs. The runtime allows it only when first_number is between 10 and 20 and second_number is between 20 and 30, inclusive.

These limits affect only demo.add_numbers. Other tools continue to follow their own protection profile, review state, OAuth role grants, and policy decisions.

7. Test policy in Simulator¶
Simulator is the native AgntID way to test how an AI-agent request will behave. The model receives a plain-English request, chooses from profile-visible tools, and the AgntID runtime checks the selected tool call before execution. An allowed call runs the real demo tool on your runtime.

On Quick Start Runtime, open Operations → Configuration, enable Simulation System under Simulation, and select Save Configuration. Wait for synchronization to show Applied so the runtime appears in Simulator.
Confirm you have a Healthy AI model credential under Access Control → Credentials. Add one for your AI provider if needed.
Open Observe & Validate → Simulator.
Select Quick Start Runtime.
Select the healthy model credential.
Select a model, or keep the default model for your provider.
Select Connect. After connection, a request box and Run button appear.

Simulator setup with a runtime, healthy model credential, selected model, and Connect button
Enter this allowed prompt and select Run:


Use demo.add_numbers to add 11 and 21.
Confirm Success and Result: 32 in Results.

Simulator showing Success and result 32 for demo.add_numbers with inputs 11 and 21
Checkpoint: Simulator shows Success and Result: 32. The AI request selected and ran an approved tool call.

Enter this denied prompt and select Run:


Use demo.add_numbers to add 50 and 21.
Confirm Execution Denied and a message like:


AgntID Policy Denied
Policy denied: first_number must satisfy {'min': 10, 'max': 20}
Simulator showing AgntID Policy Denied because first_number 50 violates the input limits
Checkpoint: Simulator shows AgntID Policy Denied and mentions first_number. The runtime blocked the policy-violating tool call before execution.

8. Verify results in Reporting¶
Reporting is the audit trail. It shows what the agent requested, which tool was selected, whether the runtime allowed or denied execution, which policy applied, and why.

Open Reporting.
Find the latest demo.add_numbers event groups from your two Simulator runs.
Expand each event group.
Confirm these outcomes:

Event	Allowed run (11, 21)	Denied run (50, 21)
Intent Check	Success	Success
Intercept	Success	Success
Tool Execution	Success	Denied
For the denied run, confirm the denial reason identifies first_number and its minimum of 10 and maximum of 20. The denied Tool Execution event records the blocked attempt; the tool did not run.

Checkpoint: Reporting shows both successful and denied tool execution events for demo.add_numbers, including the input-policy denial reason.

Optional: Debug raw MCP behavior with MCP Inspector¶
MCP Inspector is useful for testing the raw MCP endpoint directly. It is not required for this Quick Start and is less representative of the native AgntID workflow than Simulator.

Use MCP Inspector to verify the runtime's tool list, call demo_add_numbers without an AI model, debug MCP client/runtime connectivity, or compare raw MCP calls with Simulator-driven calls.

Open Inspector in the portal.
Select Quick Start Runtime.
Select Create Link, then Open Inspector.
If Connection Type is Via Proxy, select Direct.
Select Connect. The connection uses the runtime's secure AgntID tunnel; it does not require a public runtime port.
Open Tools and select List Tools. The list contains only tools allowed by the runtime's protection profile. Inspector exposes demo.add_numbers as demo_add_numbers.
Run demo_add_numbers with first_number: 11 and second_number: 21.
Confirm result 32.
Run demo_add_numbers with first_number: 50 and second_number: 21.
Confirm policy denial.
Checkpoint: MCP Inspector returns 32 for the allowed inputs and a policy denial for first_number: 50.

