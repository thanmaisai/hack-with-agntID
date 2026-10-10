"""Small command hub for setup, service readiness, and the Vend-Safe demo."""

import argparse
import asyncio
import os
import shutil
import subprocess
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

SHOP_ADMIN_BASE = os.getenv("SHOP_ADMIN_BASE", "http://localhost:9000").rstrip("/")
AGNTID_MCP_URL = os.getenv("AGNTID_MCP_URL", "http://localhost:8082/mcp")
RUNTIME_HEALTH_URL = AGNTID_MCP_URL.removesuffix("/mcp").removesuffix("/") + "/health"


async def _check_url(label: str, url: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.get(url)
            response.raise_for_status()
        print(f"  READY  {label}: {url}")
        return True
    except Exception as exc:
        detail = str(exc) or type(exc).__name__
        print(f"  WAIT   {label}: {url} ({detail})")
        return False


async def _check_services() -> bool:
    shop_ok = await _check_url("Shop API", f"{SHOP_ADMIN_BASE}/admin/state")
    runtime_ok, runtime_detail = await _runtime_health()
    print(f"  {'READY' if runtime_ok else 'WAIT'}   AgntID runtime: {runtime_detail}")
    return shop_ok and runtime_ok


async def _runtime_health() -> tuple[bool, str]:
    """Try runtime health routes and preserve useful connection diagnostics."""
    candidates = [RUNTIME_HEALTH_URL]
    if RUNTIME_HEALTH_URL.endswith("/health"):
        candidates.append(RUNTIME_HEALTH_URL.removesuffix("/health") + "/")

    errors = []
    async with httpx.AsyncClient(timeout=4.0) as client:
        for url in dict.fromkeys(candidates):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return True, f"{url} ({response.status_code})"
            except Exception as exc:
                errors.append(f"{url}: {str(exc) or type(exc).__name__}")
    return False, "; ".join(errors)


async def doctor() -> int:
    print("Vend-Safe readiness check")
    key_ready = bool(os.getenv("OPENAI_API_KEY"))
    print(f"  {'READY' if key_ready else 'NEEDS SETUP'}  OpenAI key in .env")
    shop_ok = await _check_url("Shop API", f"{SHOP_ADMIN_BASE}/admin/state")
    runtime_ok, runtime_detail = await _runtime_health()
    print(f"  {'READY' if runtime_ok else 'WAIT'}   AgntID runtime: {runtime_detail}")

    if not (shop_ok and runtime_ok):
        print("\nStart local services with: docker compose up -d --build")
    if not key_ready:
        print("Add OPENAI_API_KEY=... to .env. Do not share the key in chat or screenshots.")
    if shop_ok and runtime_ok and key_ready:
        print("\nReady for the six-run comparison: .venv/bin/python demo.py run")
        return 0
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Vend-Safe demo setup and run commands",
        epilog="Flow: setup → configure .env → start → doctor → run → review results.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor", help="Check local services and required configuration")
    subparsers.add_parser("run", help="Run all three attacks in both modes")
    subparsers.add_parser("dashboard", help="Build and open the Docker-hosted demo UI")
    subparsers.add_parser("start", help="Start the Docker Compose services")
    subparsers.add_parser("stop", help="Stop services while preserving demo data")
    args = parser.parse_args()

    if args.command == "doctor":
        raise SystemExit(asyncio.run(doctor()))
    if args.command == "run":
        if not os.getenv("OPENAI_API_KEY"):
            parser.error("OPENAI_API_KEY is missing; add it to .env first")
        if not asyncio.run(_check_services()):
            parser.error("local services are not ready; run `python demo.py doctor` for details")
        from run_compare import main as run_comparison

        raise SystemExit(asyncio.run(run_comparison()))
    if args.command in {"start", "stop", "dashboard"}:
        if not shutil.which("docker"):
            parser.error("Docker Desktop must be installed and available on PATH")
        command = ["docker", "compose", "down"] if args.command == "stop" else ["docker", "compose", "up", "-d", "--build"]
        subprocess.run(command, cwd=ROOT, check=True)
        if args.command in {"dashboard", "start"}:
            port = os.getenv("DEMO_UI_PORT", "8501")
            print(f"Vend-Safe demo UI: http://127.0.0.1:{port}")


if __name__ == "__main__":
    main()
