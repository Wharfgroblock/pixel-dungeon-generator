"""Abstract generator contract. Every generator is deterministic per seed."""
from __future__ import annotations

from abc import ABC, abstractmethod

from pixel_dungeon_generator.models.dungeon import Dungeon
from pixel_dungeon_generator.models.spec import DungeonSpec


class BaseGenerator(ABC):
    """Subclasses must be pure: same spec + seed => same Dungeon."""

    name: str = "base"

    @abstractmethod
    def generate(self, spec: DungeonSpec) -> Dungeon:
        """Return a fully-populated Dungeon. Must not mutate `spec`."""

    def describe(self) -> dict[str, str]:
        return {"name": self.name, "kind": "generator"}