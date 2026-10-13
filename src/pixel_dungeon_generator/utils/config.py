"""Config + spec loading with strict YAML parsing."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from pixel_dungeon_generator.models.spec import DungeonSpec


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"config must be a mapping: {path}")
    return data


def load_spec(path: Path) -> DungeonSpec:
    if not path.is_file():
        raise FileNotFoundError(f"spec not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return DungeonSpec.model_validate(data)