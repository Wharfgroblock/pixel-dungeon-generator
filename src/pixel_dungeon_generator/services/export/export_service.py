"""Writes Dungeon objects to disk in png / json / tmx formats."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

from pixel_dungeon_generator.adapters.filesystem.path_adapter import PathAdapter
from pixel_dungeon_generator.models.dungeon import Dungeon
from pixel_dungeon_generator.utils.logging import get_logger

_log = get_logger(__name__)

_PALETTE = {
    0: (0, 0, 0),
    1: (84, 84, 84),
    2: (32, 32, 48),
    3: (160, 110, 60),
    4: (240, 220, 120),
    5: (40, 90, 200),
    6: (200, 60, 40),
    7: (220, 180, 40),
    8: (140, 40, 140),
}


class ExportService:
    def __init__(self, paths: PathAdapter) -> None:
        self._paths = paths

    def to_png(self, dungeon: Dungeon, out: Path) -> Path:
        target = self._paths.resolve_out(out.with_suffix(".png"))
        h, w = dungeon.height, dungeon.width
        rgb = np.zeros((h, w, 3), dtype=np.uint8)
        for kind, color in _PALETTE.items():
            rgb[dungeon.grid == kind] = color
        Image.fromarray(rgb, "RGB").save(target)
        _log.info("exported png -> %s", target)
        return target

    def to_json(self, dungeon: Dungeon, out: Path) -> Path:
        target = self._paths.resolve_out(out.with_suffix(".json"))
        payload = {
            "seed": dungeon.seed,
            "generator": dungeon.generator,
            "width": dungeon.width,
            "height": dungeon.height,
            "rooms": [r.__dict__ for r in dungeon.rooms],
            "grid": dungeon.grid.tolist(),
            "meta": dungeon.meta,
        }
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return target

    def to_tmx(self, dungeon: Dungeon, out: Path) -> Path:
        target = self._paths.resolve_out(out.with_suffix(".tmx"))
        rows = "\n".join(
            "  <layer name=\"floor\" width=\"%d\" height=\"%d\">" % (dungeon.width, dungeon.height)
            for _ in [0]
        )
        body = "\n".join(
            ",".join(str(int(v)) for v in row) for row in dungeon.grid
        )
        target.write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<map width="{dungeon.width}" height="{dungeon.height}">\n'
            f"{rows}\n    <data>{body}</data>\n  </layer>\n</map>\n",
            encoding="utf-8",
        )
        return target