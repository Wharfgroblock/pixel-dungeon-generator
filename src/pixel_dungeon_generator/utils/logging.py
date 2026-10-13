"""Structured logger. JSON or human output depending on config."""
from __future__ import annotations

import json
import logging
import sys
from typing import Any

_configured = False


def _configure() -> None:
    global _configured
    if _configured:
        return
    root = logging.getLogger("pixel_dungeon_generator")
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(handler)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    _configure()
    return logging.getLogger(name)


def json_log(event: str, **fields: Any) -> str:
    return json.dumps({"event": event, **fields}, separators=(",", ":"))