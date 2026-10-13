"""Composition root. Wires services + adapters into a single container."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pixel_dungeon_generator.services.generation.registry import GeneratorRegistry
from pixel_dungeon_generator.services.export.export_service import ExportService
from pixel_dungeon_generator.services.tiles.tilepack_service import TilepackService
from pixel_dungeon_generator.services.validation.spec_validator import SpecValidator
from pixel_dungeon_generator.adapters.filesystem.path_adapter import PathAdapter
from pixel_dungeon_generator.adapters.onnx.onnx_adapter import OnnxAdapter
from pixel_dungeon_generator.utils.config import load_config


@dataclass(slots=True)
class Container:
    registry: GeneratorRegistry
    export: ExportService
    tilepacks: TilepackService
    validator: SpecValidator
    paths: PathAdapter
    onnx: OnnxAdapter


def build_container(config_path: Path) -> Container:
    cfg = load_config(config_path)
    paths = PathAdapter(root=Path(cfg["paths"]["root"]))
    onnx = OnnxAdapter(policy_path=Path(cfg["onnx"]["policy"]))
    registry = GeneratorRegistry.from_config(cfg, onnx=onnx)
    return Container(
        registry=registry,
        export=ExportService(paths=paths),
        tilepacks=TilepackService(paths=paths),
        validator=SpecValidator(),
        paths=paths,
        onnx=onnx,
    )