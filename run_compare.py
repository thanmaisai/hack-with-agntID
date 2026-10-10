"""
run_compare.py - Run all attacks in both modes, reset between runs, print comparison table.

Usage:
    python run_compare.py

Requires the shop server running on port 9000 and (for agntid mode) the
AgntID runtime on port 8082.
"""

import asyncio
import json
import os

import httpx

from agent import run_direct, run_agntid
from attacks import ATTACKS

SHOP_MCP_URL = os.getenv("SHOP_MCP_URL", "http://localhost:9000/mcp")
SHOP_ADMIN_BASE = os.getenv("SHOP_ADMIN_BASE", "http://localhost:9000")


# ---------------------------------------------------------------------------
# Harness helpers
# ---------------------------------------------------------------------------


async def reset_shop():
    async with httpx.AsyncClient() as h:
        r = await h.post(f"{SHOP_ADMIN_BASE}/admin/reset")
        r.raise_for_status()


async def get_shop_state() -> dict:
    async with httpx.AsyncClient() as h:
        r = await h.get(f"{SHOP_ADMIN_BASE}/admin/state")
        r.raise_for_status()
        return r.json()


def _format_row(
    attack: int,
    mode: str,
    state: dict,
    agent_denials: int,
) -> dict:
    return {
        "attack": attack,
        "mode": mode,
        "cash": f"${state['cash']:.2f}",
        "discounts": len(state["discounts_given"]),
        "ext_emails": state["external_emails_sent"],
        "orders": len(state["order_log"]),
        "denials": agent_denials,
    }


# ---------------------------------------------------------------------------
# Main comparison run
# ---------------------------------------------------------------------------


async def main():
    rows = []

    for attack in [1, 2, 3]:
        # --- Direct mode ---
        print(f"\n{'='*60}")
        print(f"ATTACK {attack} | DIRECT MODE")
        print("="*60)
        await reset_shop()
        agent_stats = await run_direct(attack)
        state = await get_shop_state()
        rows.append(_format_row(attack, "direct", state, agent_stats["denials"]))

        # --- AgntID mode ---
        print(f"\n{'='*60}")
        print(f"ATTACK {attack} | AGNTID MODE")
        print("="*60)
        await reset_shop()
        agent_stats = await run_agntid(attack)
        state = await get_shop_state()
        rows.append(_format_row(attack, "agntid", state, agent_stats["denials"]))

    # ---------------------------------------------------------------------------
    # Print scoreboard table
    # ---------------------------------------------------------------------------

    print("\n")
    print("=" * 75)
    print("VEND-SAFE SCOREBOARD")
    print("=" * 75)
    header = (
        f"{'Attack':>6}  {'Mode':>7}  {'Cash':>10}  "
        f"{'Discounts':>9}  {'Ext Emails':>10}  {'Orders':>6}  {'Denials':>7}"
    )
    print(header)
    print("-" * 75)

    for row in rows:
        line = (
            f"{row['attack']:>6}  {row['mode']:>7}  {row['cash']:>10}  "
            f"{row['discounts']:>9}  {row['ext_emails']:>10}  "
            f"{row['orders']:>6}  {row['denials']:>7}"
        )
        print(line)

    print("=" * 75)
    print("\nLegend:")
    print("  Cash        - Remaining cash after run (start: $200.00)")
    print("  Discounts   - Number of discounts applied")
    print("  Ext Emails  - Emails sent to non-@example.com addresses")
    print("  Orders      - Number of supplier orders placed")
    print("  Denials     - Policy denials from AgntID runtime")
    print()


if __name__ == "__main__":
    asyncio.run(main())
