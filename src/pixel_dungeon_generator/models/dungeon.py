"""Core dungeon data model. Immutable grid + metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Iterator

import numpy as np
import numpy.typing as npt


class TileKind(IntEnum):
    VOID = 0
    FLOOR = 1
    WALL = 2
    DOOR = 3
    STAIRS = 4
    WATER = 5
    LAVA = 6
    CHEST = 7
    TRAP = 8


@dataclass(frozen=True, slots=True)
class Room:
    x: int
    y: int
    w: int
    h: int
    kind: str = "generic"

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def intersects(self, other: "Room", pad: int = 1) -> bool:
        return not (
            self.x + self.w + pad <= other.x
            or other.x + other.w + pad <= self.x
            or self.y + self.h + pad <= other.y
            or other.y + other.h + pad <= self.y
        )


@dataclass(slots=True)
class Dungeon:
    grid: npt.NDArray[np.uint8]
    rooms: list[Room] = field(default_factory=list)
    seed: int = 0
    generator: str = "unknown"
    meta: dict[str, str] = field(default_factory=dict)

    @property
    def width(self) -> int:
        return int(self.grid.shape[1])

    @property
    def height(self) -> int:
        return int(self.grid.shape[0])

    def iter_rooms(self) -> Iterator[Room]:
        yield from self.rooms

    def tile(self, x: int, y: int) -> TileKind:
        return TileKind(int(self.grid[y, x]))

    def walkable_count(self) -> int:
        return int(np.count_nonzero(self.grid == TileKind.FLOOR))