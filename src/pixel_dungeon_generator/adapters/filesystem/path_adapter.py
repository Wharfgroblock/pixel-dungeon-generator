"""Resolves and sandboxes filesystem paths for packs and outputs."""
from __future__ import annotations

from pathlib import Path

from pixel_dungeon_generator.utils.sandbox import safe_join


class PathAdapter:
    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    @property
    def root(self) -> Path:
        return self._root

    def packs_dir(self) -> Path:
        return self._root / "tilepacks"

    def out_dir(self) -> Path:
        d = self._root / "out"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def resolve_out(self, path: Path) -> Path:
        target = safe_join(self.out_dir(), str(path))
        target.parent.mkdir(parents=True, exist_ok=True)
        return target