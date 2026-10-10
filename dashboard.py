"""Local web dashboard for the Vend-Safe live demo trace."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sqlite3
import threading
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

load_dotenv()

SHOP_ADMIN_BASE = os.getenv("SHOP_ADMIN_BASE", "http://localhost:9000").rstrip("/")
AGNTID_MCP_URL = os.getenv("AGNTID_MCP_URL", "http://localhost:8082/mcp")
RUNTIME_HEALTH_URL = AGNTID_MCP_URL.removesuffix("/mcp").removesuffix("/") + "/health"

_runs: dict[str, dict] = {}
_runs_lock = threading.Lock()
_run_lock = threading.Lock()
_active_run_id: str | None = None

SETTINGS_DB = os.getenv("DEMO_SETTINGS_DB", os.path.join(os.path.dirname(__file__), "data", "demo_settings.sqlite3"))
DEFAULT_SETTINGS = {
    "cash": 200.0,
    "inventory": {
        "chips": {"cost": 0.80, "price": 2.00, "stock": 20},
        "cola": {"cost": 1.00, "price": 2.50, "stock": 15},
        "tungsten_cube": {"cost": 12.00, "price": 20.00, "stock": 0},
    },
    "policy": {"max_discount_percent": 20, "max_order_quantity": 10, "min_price": 1.50, "max_price": 25.00},
}


def _settings_connection():
    os.makedirs(os.path.dirname(SETTINGS_DB) or ".", exist_ok=True)
    connection = sqlite3.connect(SETTINGS_DB, timeout=5)
    connection.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    return connection


def _load_settings() -> dict:
    with _settings_connection() as db:
        row = db.execute("SELECT value FROM settings WHERE key = 'shop' ").fetchone()
        if not row:
            settings = DEFAULT_SETTINGS
            db.execute("INSERT INTO settings(key, value) VALUES('shop', ?)", (json.dumps(settings),))
            return json.loads(json.dumps(settings))
        try:
            saved = json.loads(row[0])
            return {**DEFAULT_SETTINGS, **saved, "inventory": saved.get("inventory", DEFAULT_SETTINGS["inventory"]), "policy": {**DEFAULT_SETTINGS["policy"], **saved.get("policy", {})}}
        except (ValueError, TypeError):
            return json.loads(json.dumps(DEFAULT_SETTINGS))


def _save_settings(settings: dict) -> None:
    with _settings_connection() as db:
        db.execute("INSERT INTO settings(key, value) VALUES('shop', ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (json.dumps(settings),))


def _validate_settings(settings: object) -> tuple[dict | None, str | None]:
    if not isinstance(settings, dict) or not isinstance(settings.get("inventory"), dict) or not isinstance(settings.get("policy"), dict):
        return None, "Settings must include inventory and policy objects"
    try:
        value = {
            "cash": round(float(settings["cash"]), 2),
            "inventory": {},
            "policy": {
                "max_discount_percent": float(settings["policy"]["max_discount_percent"]),
                "max_order_quantity": int(settings["policy"]["max_order_quantity"]),
                "min_price": round(float(settings["policy"]["min_price"]), 2),
                "max_price": round(float(settings["policy"]["max_price"]), 2),
            },
        }
        if value["cash"] < 0 or value["policy"]["max_discount_percent"] < 0 or value["policy"]["max_discount_percent"] > 100 or value["policy"]["max_order_quantity"] < 1 or value["policy"]["min_price"] < 0 or value["policy"]["max_price"] < value["policy"]["min_price"]:
            return None, "Cash, discount, order, and price limits are outside valid ranges"
        if set(settings["inventory"]) != set(DEFAULT_SETTINGS["inventory"]):
            return None, "Inventory must contain chips, cola, and tungsten_cube"
        for item, defaults in DEFAULT_SETTINGS["inventory"].items():
            entry = settings["inventory"][item]
            cost, price, stock = float(entry["cost"]), float(entry["price"]), int(entry["stock"])
            if cost < 0 or price < 0 or stock < 0:
                return None, f"{item}: cost, price, and stock must be zero or greater"
            value["inventory"][item] = {"cost": round(cost, 2), "price": round(price, 2), "stock": stock}
        return value, None
    except (KeyError, TypeError, ValueError, OverflowError):
        return None, "Enter valid numeric values for all shop and policy settings"


def _probe(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=2.5) as response:
            return {"ok": 200 <= response.status < 400, "status": response.status}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def _shop_json(path: str, method: str = "GET", payload: dict | None = None) -> tuple[int, dict]:
    """Proxy local storefront actions so the browser never talks to the shop container directly."""
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"{SHOP_ADMIN_BASE}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if body else {},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read())
        except (ValueError, json.JSONDecodeError):
            return exc.code, {"error": "The shop rejected this request"}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 503, {"error": f"Shop unavailable: {exc}"}


def _publish(run_id: str, payload: dict) -> None:
    with _runs_lock:
        run = _runs.get(run_id)
        if not run:
            return
        event = {
            **payload,
            "seq": len(run["events"]) + 1,
            "time": payload.get("time") or datetime.now(timezone.utc).isoformat(),
        }
        run["events"].append(event)
        if payload.get("type") == "comparison_finished":
            run["summary"] = {
                "rows": payload.get("rows", []),
                "checks": payload.get("checks", []),
                "passed": payload.get("passed", False),
                "kind": payload.get("kind", "guided"),
                "completed": payload.get("completed", False),
            }


def _run_worker(run_id: str, attacks: list[int], prompt: str | None = None) -> None:
    global _active_run_id
    try:
        from run_compare import run_comparison, run_playground

        on_event = lambda event: _publish(run_id, event)
        result = asyncio.run(
            run_playground(prompt, on_event=on_event)
            if prompt is not None
            else run_comparison(on_event=on_event, attacks=attacks)
        )
        with _runs_lock:
            _runs[run_id]["status"] = (
                "complete" if result.get("completed") or result.get("passed") is True
                else "incomplete"
            )
            _runs[run_id]["summary"] = result
    except Exception as exc:
        _publish(run_id, {"type": "run_error", "message": str(exc)})
        with _runs_lock:
            _runs[run_id]["status"] = "error"
    finally:
        with _run_lock:
            _active_run_id = None


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "VendSafeDashboard/1.0"

    def log_message(self, format_string: str, *args) -> None:
        # Keep the terminal readable while the demo is in progress.
        print(f"[dashboard] {format_string % args}")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data: dict) -> None:
        self._send(status, json.dumps(data).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._json(200, {
                "shop": _probe(f"{SHOP_ADMIN_BASE}/admin/state"),
                "runtime": _probe(RUNTIME_HEALTH_URL),
                "model_key_ready": bool(os.getenv("OPENAI_API_KEY")),
            })
            return
        if parsed.path == "/api/settings":
            self._json(200, _load_settings())
            return
        if parsed.path == "/api/store":
            status, result = _shop_json("/admin/state")
            self._json(status, result)
            return
        if parsed.path.startswith("/api/runs/"):
            run_id = parsed.path.removeprefix("/api/runs/")
            after = int(parse_qs(parsed.query).get("after", ["0"])[0])
            with _runs_lock:
                run = _runs.get(run_id)
                if run is None:
                    self._json(404, {"error": "Run not found"})
                    return
                result = {
                    "id": run_id,
                    "status": run["status"],
                    "events": [event for event in run["events"] if event["seq"] > after],
                    "summary": run["summary"],
                }
            self._json(200, result)
            return

        self._json(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        global _active_run_id
        if self.path == "/api/settings":
            origin = self.headers.get("Origin")
            if origin:
                parsed_origin = urlparse(origin)
                allowed_port = int(os.getenv("DEMO_UI_PORT", str(self.server.server_port)))
                if parsed_origin.hostname not in {"127.0.0.1", "localhost"} or parsed_origin.port != allowed_port:
                    self._json(403, {"error": "Requests must come from this local dashboard"})
                    return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size > 8192:
                    self._json(413, {"error": "Request too large"})
                    return
                settings, error = _validate_settings(json.loads(self.rfile.read(size) or b"{}"))
                if error:
                    self._json(400, {"error": error})
                    return
                _save_settings(settings)
                self._json(200, settings)
            except (json.JSONDecodeError, ValueError) as exc:
                self._json(400, {"error": f"Invalid request: {exc}"})
            return
        if self.path in {"/api/store/checkout", "/api/store/request"}:
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size > 2048:
                    self._json(413, {"error": "Request too large"})
                    return
                payload = json.loads(self.rfile.read(size) or b"{}")
                target = "/admin/checkout" if self.path.endswith("checkout") else "/admin/requests"
                status, result = _shop_json(target, "POST", payload)
                self._json(status, result)
            except (json.JSONDecodeError, ValueError) as exc:
                self._json(400, {"error": f"Invalid request: {exc}"})
            return
        if self.path != "/api/run":
            self._json(404, {"error": "Not found"})
            return
        origin = self.headers.get("Origin")
        if origin:
            parsed_origin = urlparse(origin)
            allowed_hosts = {"127.0.0.1", "localhost"}
            allowed_port = int(os.getenv("DEMO_UI_PORT", str(self.server.server_port)))
            if parsed_origin.hostname not in allowed_hosts or parsed_origin.port != allowed_port:
                self._json(403, {"error": "Requests must come from this local dashboard"})
                return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 4096:
                self._json(413, {"error": "Request too large"})
                return
            body = json.loads(self.rfile.read(size) or b"{}")
            kind = body.get("kind", "guided")
            prompt = None
            attacks = body.get("attacks", [1, 2, 3])
            if kind == "playground":
                prompt = body.get("prompt")
                if not isinstance(prompt, str) or not 4 <= len(prompt.strip()) <= 500:
                    self._json(400, {"error": "Enter a prompt between 4 and 500 characters"})
                    return
                attacks = []
            elif kind != "guided" or not isinstance(attacks, list) or not attacks or any(
                type(attack) is not int or attack not in (1, 2, 3) for attack in attacks
            ):
                self._json(400, {"error": "Choose valid guided scenarios or submit a playground prompt"})
                return
            attacks = list(dict.fromkeys(attacks))
            if not os.getenv("OPENAI_API_KEY"):
                self._json(400, {"error": "Add OPENAI_API_KEY to the local .env before running scenarios"})
                return
            with _run_lock:
                if _active_run_id:
                    self._json(409, {"error": "A comparison is already running", "run_id": _active_run_id})
                    return
                run_id = uuid.uuid4().hex
                _active_run_id = run_id
                with _runs_lock:
                    _runs[run_id] = {"status": "running", "events": [], "summary": None, "kind": kind}
            worker = threading.Thread(target=_run_worker, args=(run_id, attacks, prompt), daemon=True)
            worker.start()
            self._json(202, {"run_id": run_id, "status": "running"})
        except (json.JSONDecodeError, ValueError) as exc:
            self._json(400, {"error": f"Invalid request: {exc}"})


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Vend-Safe visual demo dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (defaults to local machine only)")
    parser.add_argument("--port", type=int, default=8501)
    args = parser.parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Vend-Safe comparison API listening on {args.host}:{args.port}")
    print("The React interface is served by the Docker demo-ui container.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
