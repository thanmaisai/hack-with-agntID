"""
agent.py - Vend-Safe agent runner.

Usage:
    python agent.py --mode direct  --attack 1
    python agent.py --mode agntid  --attack 2
    python agent.py --mode direct  --attack 3

Environment variables:
    OPENAI_API_KEY       - Required for both modes
    AGNTID_MCP_URL       - AgntID runtime MCP endpoint (default: http://localhost:8082/mcp)
    AGNTID_ACCESS_TOKEN  - Optional bearer token for OAuth-protected runtimes (raw, no "Bearer" prefix)
    SHOP_MCP_URL         - Shop server MCP endpoint (default: http://localhost:9000/mcp)
"""

import argparse
import asyncio
import json
import os

import openai
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from attacks import ATTACKS, SYSTEM_PROMPT

# Load project-local configuration for direct invocation and `python -m` alike.
load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_ID = "vend-safe-agent"
USER_ID = "user-42"

SHOP_MCP_URL = os.getenv("SHOP_MCP_URL", "http://localhost:9000/mcp")
AGNTID_MCP_URL = os.getenv("AGNTID_MCP_URL", "http://localhost:8082/mcp")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# ---------------------------------------------------------------------------
# Tool schema helpers
# ---------------------------------------------------------------------------


def _tools_to_openai(tools) -> list[dict]:
    """Convert MCP tool objects to OpenAI function definitions."""
    result = []
    for t in tools:
        schema = getattr(t, "inputSchema", None) or {
            "type": "object",
            "properties": {},
        }
        result.append(
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": getattr(t, "description", "") or "",
                    "parameters": schema,
                },
            }
        )
    return result


# ---------------------------------------------------------------------------
# Model loop (shared by both modes)
# ---------------------------------------------------------------------------


async def _run_model_loop(
    prompt: str,
    tools,
    call_tool_fn,
    mode: str,
    attack: int,
) -> dict:
    """
    Drive the OpenAI function-calling loop.

    Args:
        prompt:       The attack prompt.
        tools:        List of MCP tool objects visible to the model.
        call_tool_fn: Async callable(name, args) -> result string.
        mode:         "direct" or "agntid" (for printing).
        attack:       Attack number (for printing).

    Returns:
        dict with keys: denials (int), answer (str)
    """
    client = await _create_openai_client()
    openai_tools = _tools_to_openai(tools)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    denials = 0
    max_rounds = 10

    print(f"\n[{mode.upper()} | Attack {attack}] Starting agent loop...")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}\n")

    for _round in range(max_rounds):
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=openai_tools if openai_tools else openai.NOT_GIVEN,
            temperature=0,
        )

        msg = response.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))

        if msg.tool_calls:
            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments or "{}")

                print(f"  -> Tool call: {fn_name}({fn_args})")
                result = await call_tool_fn(fn_name, fn_args)

                # Handle AgntID denial
                if getattr(result, "denied", False):
                    denials += 1
                    tool_result_str = f"[DENIED] {result.message}"
                    print(f"  <- DENIED: {result.message}")
                else:
                    # Scalar or dict result
                    if hasattr(result, "value"):
                        tool_result_str = str(result.value)
                    elif hasattr(result, "content"):
                        # Raw MCP result
                        parts = []
                        for c in result.content:
                            if hasattr(c, "text"):
                                parts.append(c.text)
                            else:
                                parts.append(str(c))
                        tool_result_str = "\n".join(parts)
                    else:
                        tool_result_str = str(result)
                    print(f"  <- Result: {tool_result_str[:200]}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_result_str,
                    }
                )
        else:
            # No more tool calls - final answer
            answer = msg.content or ""
            print(f"\nFinal answer: {answer}")
            return {"denials": denials, "answer": answer}

    return {"denials": denials, "answer": "[max rounds reached]"}


async def _create_openai_client() -> openai.AsyncOpenAI:
    """Build the OpenAI client only when a run starts, with a clear key error."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to run the agent")
    return openai.AsyncOpenAI()


# ---------------------------------------------------------------------------
# Direct mode
# ---------------------------------------------------------------------------


async def run_direct(attack: int) -> dict:
    """Run attack directly against the shop MCP server (no AgntID)."""
    prompt = ATTACKS[attack]

    async with streamable_http_client(SHOP_MCP_URL) as (read, write, _get_session_id):
        async with ClientSession(read, write) as session:
            await session.initialize()
            raw_tools = await session.list_tools()
            tools = raw_tools.tools

            async def call_tool(name: str, args: dict):
                return await session.call_tool(name, args)

            stats = await _run_model_loop(prompt, tools, call_tool, "direct", attack)

    return stats


# ---------------------------------------------------------------------------
# AgntID mode
# ---------------------------------------------------------------------------


async def run_agntid(attack: int) -> dict:
    """Run attack through the AgntID runtime (enforced mode)."""
    try:
        import agntid
    except ImportError as exc:
        raise RuntimeError(
            "AgntID mode requires the AgntID Python SDK. Install it from "
            "https://github.com/AGNTID-AI/agntid-python and its OpenAI extra."
        ) from exc

    prompt = ATTACKS[attack]
    access_token = os.getenv("AGNTID_ACCESS_TOKEN") or None

    async with agntid.AgntidMCPClient(
        AGNTID_MCP_URL,
        access_token=access_token,
    ) as client:
        # Discover profile-visible tools
        visible = await agntid.get_tools_list(client)

        # Create task and wrap client
        task_id = agntid.create_task(AGENT_ID, USER_ID, prompt)
        wrapped = agntid.wrap_client(client, task_id)

        async with agntid.task_context(client, task_id):
            task_open = await agntid.send_task_open_details(
                client, task_id, AGENT_ID, USER_ID, prompt
            )
            if not task_open.ok:
                raise RuntimeError(
                    f"Task open failed: {task_open.reason}"
                )

            # Narrow to the intent-shortlisted tools
            tools = agntid.filter_tools_for_task(visible, task_open)
            print(
                f"  [AgntID] {len(visible)} visible -> "
                f"{len(tools)} shortlisted for this task"
            )

            async def call_tool(name: str, args: dict):
                return await wrapped.call_tool_async(name, args)

            stats = await _run_model_loop(
                prompt, tools, call_tool, "agntid", attack
            )

    return stats


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Vend-Safe agent runner")
    parser.add_argument(
        "--mode",
        choices=["direct", "agntid"],
        required=True,
        help="Run directly against shop or through AgntID runtime",
    )
    parser.add_argument(
        "--attack",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Attack number to run",
    )
    args = parser.parse_args()

    try:
        if args.mode == "direct":
            stats = asyncio.run(run_direct(args.attack))
        else:
            stats = asyncio.run(run_agntid(args.attack))
    except KeyboardInterrupt:
        raise
    except Exception as exc:
        parser.exit(1, f"Error: {exc}\n")

    print(f"\nDenials: {stats['denials']}")


if __name__ == "__main__":
    main()
