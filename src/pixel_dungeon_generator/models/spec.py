"""Pydantic spec loaded from YAML — the input contract for generators."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

GeneratorName = Literal["wfc", "bsp", "cellular", "diffusion"]


class DungeonSpec(BaseModel):
    model_config = {"extra": "forbid"}

    name: str = Field(min_length=1, max_length=64)
    generator: GeneratorName = "wfc"
    width: int = Field(ge=16, le=256)
    height: int = Field(ge=16, le=256)
    seed: int = Field(default=0, ge=0, le=2**31 - 1)
    room_count: int = Field(default=12, ge=1, le=64)
    room_min: int = Field(default=4, ge=3, le=32)
    room_max: int = Field(default=10, ge=4, le=48)
    connectivity: Literal["none", "loose", "strict"] = "loose"
    tilepack: str = "default_16"
    biome: str = "stone"

    @model_validator(mode="after")
    def _check_room_bounds(self) -> "DungeonSpec":
        if self.room_min > self.room_max:
            raise ValueError("room_min must be <= room_max")
        if self.room_max * 2 >= min(self.width, self.height):
            raise ValueError("room_max too large for grid")
        return self

    def fingerprint(self) -> str:
        return f"{self.generator}:{self.width}x{self.height}:{self.seed}:{self.biome}"