"""Loads and validates tile packs (folder of PNGs + pack.yaml)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from PIL import Image

from pixel_dungeon_generator.adapters.filesystem.path_adapter import PathAdapter
from pixel_dungeon_generator.utils.sandbox import safe_join


@dataclass(frozen=True, slots=True)
class Tilepack:
    name: str
    tile_size: int
    tiles: dict[str, Path]


class TilepackService:
    def __init__(self, paths: PathAdapter) -> None:
        self._paths = paths

    def load(self, name: str) -> Tilepack:
        root = safe_join(self._paths.packs_dir(), name)
        manifest = root / "pack.yaml"
        if not manifest.is_file():
            raise FileNotFoundError(f"tilepack {name!r} missing pack.yaml")
        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        tiles: dict[str, Path] = {}
        for key, rel in data.get("tiles", {}).items():
            p = safe_join(root, rel)
            if not p.is_file():
                raise FileNotFoundError(f"tile {key} -> {rel} not found")
            with Image.open(p) as im:
                if im.size != (data["tile_size"], data["tile_size"]):
                    raise ValueError(f"tile {key} wrong size: {im.size}")
            tiles[key] = p
        return Tilepack(name=name, tile_size=int(data["tile_size"]), tiles=tiles)

    def list_available(self) -> list[str]:
        packs = self._paths.packs_dir()
        if not packs.is_dir():
            return []
        return sorted(p.name for p in packs.iterdir() if (p / "pack.yaml").is_file())