"""Generator registry. Look up by name; config-driven defaults."""
from __future__ import annotations

from typing import Any

from pixel_dungeon_generator.adapters.onnx.onnx_adapter import OnnxAdapter
from pixel_dungeon_generator.services.generation.base import BaseGenerator
from pixel_dungeon_generator.services.generation.wfc_generator import WfcGenerator


class GeneratorRegistry:
    def __init__(self, generators: dict[str, BaseGenerator], default: str) -> None:
        if default not in generators:
            raise KeyError(f"default generator {default!r} not registered")
        self._gens = generators
        self._default = default

    @classmethod
    def from_config(cls, cfg: dict[str, Any], onnx: OnnxAdapter) -> "GeneratorRegistry":
        gens: dict[str, BaseGenerator] = {"wfc": WfcGenerator()}
        # diffusion generator is loaded lazily if a checkpoint is present
        _ = onnx
        return cls(gens, default=cfg["generation"]["default_generator"])

    def get(self, name: str | None) -> BaseGenerator:
        key = name or self._default
        if key not in self._gens:
            raise KeyError(f"unknown generator {key!r}; have {sorted(self._gens)}")
        return self._gens[key]

    def names(self) -> list[str]:
        return sorted(self._gens)