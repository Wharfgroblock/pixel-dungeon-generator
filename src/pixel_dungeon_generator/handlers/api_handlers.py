"""Optional local HTTP facade. Wraps services; no business logic here."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from pixel_dungeon_generator.bootstrap.app import Container
from pixel_dungeon_generator.models.spec import DungeonSpec


class _Handler(BaseHTTPRequestHandler):
    container: Container

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json(200, {"ok": True})
        elif self.path == "/generators":
            self._json(200, {"generators": self.container.registry.names()})
        else:
            self._json(404, {"error": "not found"})

    def _json(self, code: int, payload: dict[str, Any]) -> None:
        import json
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(container: Container, host: str = "127.0.0.1", port: int = 6767) -> None:
    handler = type("BoundHandler", (_Handler,), {"container": container})
    HTTPServer((host, port), handler).serve_forever()


def parse_spec_payload(payload: dict[str, Any]) -> DungeonSpec:
    return DungeonSpec.model_validate(payload)