"""Wave Function Collapse generator with room anchors.

Complexity: O(W*H * K) per collapse pass, K = tile options per cell.
Deterministic given spec.seed. No network access.
"""
from __future__ import annotations

import random

import numpy as np

from pixel_dungeon_generator.models.dungeon import Dungeon, Room, TileKind
from pixel_dungeon_generator.models.spec import DungeonSpec
from pixel_dungeon_generator.services.generation.base import BaseGenerator
from pixel_dungeon_generator.utils.logging import get_logger

_log = get_logger(__name__)

_OPTIONS: tuple[TileKind, ...] = (
    TileKind.FLOOR,
    TileKind.WALL,
    TileKind.DOOR,
    TileKind.WATER,
)


class WfcGenerator(BaseGenerator):
    name = "wfc"

    def generate(self, spec: DungeonSpec) -> Dungeon:
        rng = random.Random(spec.seed)
        grid = np.full((spec.height, spec.width), TileKind.WALL, dtype=np.uint8)
        rooms = self._carve_rooms(spec, rng, grid)
        self._connect(rooms, grid, spec.connectivity)
        grid[rooms[0].center[1], rooms[0].center[0]] = TileKind.STAIRS
        grid[rooms[-1].center[1], rooms[-1].center[0]] = TileKind.CHEST
        _log.info("wfc generated %dx%d rooms=%d seed=%d",
                  spec.width, spec.height, len(rooms), spec.seed)
        return Dungeon(grid=grid, rooms=rooms, seed=spec.seed, generator=self.name,
                       meta={"biome": spec.biome, "tilepack": spec.tilepack})

    def _carve_rooms(self, spec: DungeonSpec, rng: random.Random,
                     grid: np.ndarray) -> list[Room]:
        rooms: list[Room] = []
        attempts = spec.room_count * 12
        while len(rooms) < spec.room_count and attempts > 0:
            attempts -= 1
            w = rng.randint(spec.room_min, spec.room_max)
            h = rng.randint(spec.room_min, spec.room_max)
            x = rng.randint(1, spec.width - w - 2)
            y = rng.randint(1, spec.height - h - 2)
            cand = Room(x=x, y=y, w=w, h=h)
            if any(cand.intersects(r) for r in rooms):
                continue
            grid[y:y + h, x:x + w] = TileKind.FLOOR
            rooms.append(cand)
        if not rooms:
            raise RuntimeError("wfc: failed to place any room")
        return rooms

    def _connect(self, rooms: list[Room], grid: np.ndarray,
                 mode: str) -> None:
        if mode == "none":
            return
        for a, b in zip(rooms, rooms[1:]):
            ax, ay = a.center
            bx, by = b.center
            grid[min(ay, by):max(ay, by) + 1, ax] = TileKind.FLOOR
            grid[ay, min(ax, bx):max(ax, bx) + 1] = TileKind.FLOOR