---
title: Review Advanced Access Controls
last_verified: 2026-10-08
owner: docs-team
---

<div class="page-intro" markdown>

# Review Advanced access controls

Use **Advanced** in the [AgntID portal](https://app.agntid.ai/) to review how discovered MCP actions are classified, respond to changes in a server's tool catalog, and correct a classification that does not match the action.

</div>

## When to use Advanced

Open **Advanced** when you need to:

- approve an action whose classification is waiting for review
- understand why an action has a particular operation, sensitivity, effect, or execution surface
- review tools that were added, removed, or changed after MCP discovery
- correct a system-assigned classification label
- review or withdraw an active classification correction

Classification affects which actions are eligible under a runtime's protection profile. A correction can therefore change tool visibility and trigger a runtime policy synchronization.

## Before you begin

You need:

- an organization selected in the portal
- a registered runtime in that organization
- at least one MCP server whose actions have been discovered
- permission to review classifications and make administrative corrections

Use [Add an MCP server](attach-server.md) first if the runtime has not discovered any actions.

## Open Advanced

1. In the [AgntID portal](https://app.agntid.ai/), select the organization you want to review.
2. Open **Access Control → Advanced**.
3. Select the runtime whose discovered actions you want to inspect.

Advanced has three tabs:

| Tab | Use it to |
| --- | --- |
| **Action Classifications** | Review system-assigned labels, approve pending classifications, and open an action's classification details |
| **Catalog Drift** | Review changes detected between versions of an MCP server's discovered tool catalog |
| **Classification Overrides** | Review active and inactive admin corrections, open the affected action, or withdraw a correction |

## Review action classifications

The **Action Classifications** tab groups discovered actions by tool. Expand a tool to see each action's:

- operation type
- domain
- data sensitivity
- security-relevant effects
- execution surface
- review state

Use the filters to find actions by any of these labels. The data-sensitivity filter is inclusive: for example, **HIGH or higher** also includes critical actions.

To inspect one action:

1. Expand its tool.
2. Select **View Details**.
3. Review the current labels, supporting classification evidence, confidence, corrections, and history.
4. If the review state is **PENDING_REVIEW** and the labels are correct, select **Approve Classification**.
5. Enter a clear rationale and select **Approve**.

Approving accepts the current classification. It does not create a correction.

!!! note "Taxonomy backfill"
    A **Taxonomy backfill in progress** message means some actions still use an older classification taxonomy. Wait for the backfill to finish, then select **Refresh** before completing the review.

## Correct an action label

Use a correction only when the effective classification is wrong. A correction replaces one system-assigned dimension, such as operation type, domain, blast radius, data sensitivity, criticality, privilege level, execution surface, or effects.

1. From an action's classification details, select **Correct Label**.
2. Choose the dimension to correct.
3. Select the corrected value.
4. Enter the reason for the correction.
5. If the portal warns that the review state will change, review the new state and confirm it.
6. Select **Save Correction**.

After saving, wait for runtime synchronization before testing tool visibility again. Use **Access Policies** from the action details when the classification is correct but a call needs narrower input limits.

## Review catalog drift

Catalog drift is recorded when discovery finds that tools were added, removed, or modified. The portal assigns a change risk and records how the change was handled.

1. Open **Catalog Drift**.
2. Use the status filters to find changes waiting for review or previously handled changes.
3. For a pending change, select **Review**.
4. Review the added, removed, and modified tools.
5. Choose **Accept change** to apply the discovered catalog or **Dismiss change** to reject it.
6. Enter the reason for the decision and select **Save review**.

Do not accept a change based only on its risk label. Confirm that the changed tools match the MCP server version and configuration you intended to run.

## Review or withdraw corrections

The **Classification Overrides** tab shows the system value, corrected value, rationale, and current status for each correction.

To remove an active correction:

1. Find the action and confirm the corrected dimension and rationale.
2. Select **Withdraw**.
3. Enter the reason for withdrawing it.
4. Select **Withdraw Correction**.

Withdrawing makes the system-classified value effective again and records the change in the action's history. Recheck the action's review state and runtime eligibility afterward.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No runtime is listed | Confirm the runtime belongs to the selected organization and is registered in the portal |
| No classifications are shown | Confirm an MCP server is applied and has discovered tools; clear the classification filters |
| An action is not available to a client | Check its review state, protection profile, individual tool state, OAuth role grants, and policies |
| A catalog change is not listed | Select the correct runtime, clear the drift status filter, and run discovery again |
| A correction does not affect visibility | Wait for runtime synchronization, then check the protection profile and other access controls |

## What’s next

- [Understand MCP tool visibility](index.md#how-tool-visibility-works)
- [Connect Cursor, Claude, or Codex](connect-clients.md)
- [Protect MCP access with OAuth](oauth.md)
- [Troubleshooting](../troubleshooting.md)
