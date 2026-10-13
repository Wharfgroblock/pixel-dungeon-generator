from __future__ import annotations

import numpy as np

from pixel_dungeon_generator.models.dungeon import TileKind
from pixel_dungeon_generator.models.spec import DungeonSpec
from pixel_dungeon_generator.services.generation.registry import GeneratorRegistry
from pixel_dungeon_generator.services.generation.wfc_generator import WfcGenerator


def _spec(**over: object) -> DungeonSpec:
    base = dict(name="t", generator="wfc", width=48, height=48, seed=6767,
                room_count=8, room_min=4, room_max=8)
    base.update(over)
    return DungeonSpec(**base)  # type: ignore[arg-type]


def test_wfc_is_deterministic() -> None:
    gen =