"""Guarded ONNX loader for diffusion-based tile synthesis."""
from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from pixel_dungeon_generator.utils.logging import get_logger

_log = get_logger(__name__)


class OnnxAdapter:
    def __init__(self, policy_path: Path) -> None:
        self._policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))

    def _verify_hash(self, model: Path) -> None:
        if not self._policy.get("require_sha256", True):
            return
        allowed = set(self._policy.get("trusted_hashes") or [])
        if not allowed:
            _log.warning("no trusted_hashes configured; skipping pin check")
            return
        digest = hashlib.sha256(model.read_bytes()).hexdigest()
        if digest not in allowed:
            raise PermissionError(f"model hash {digest} not in trusted set")

    def load(self, model: Path):
        if model.stat().st_size > self._policy["max_model_bytes"]:
            raise ValueError("model exceeds max_model_bytes policy")
        self._verify_hash(model)
        import onnxruntime as ort
        providers = list(self._policy["allowed_providers"])
        return ort.InferenceSession(str(model), providers=providers)