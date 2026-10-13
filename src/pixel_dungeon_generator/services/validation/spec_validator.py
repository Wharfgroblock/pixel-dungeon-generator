"""Cross-field validation that pydantic can't express on its own."""
from __future__ import annotations

from pixel_dungeon_generator.models.spec import DungeonSpec


class SpecValidator:
    def validate(self, spec: DungeonSpec) -> list[str]:
        warnings: list[str] = []
        area = spec.width * spec.height
        max_rooms = spec.room_count * spec.room_max * spec.room_max
        if max_rooms > area * 0.6:
            warnings.append(
                f"room budget {max_rooms} exceeds 60% of grid area {area}; "
                "generation may fail to place all rooms"
            )
        if spec.generator == "diffusion" and spec.biome not in {"stone", "crypt", "forest"}:
            warnings.append(f"biome {spec.biome!r} not trained for diffusion generator")
        return warnings

    def assert_valid(self, spec: DungeonSpec) -> None:
        problems = self.validate(spec)
        if problems:
            raise ValueError("; ".join(problems))