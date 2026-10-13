"""Thin CLI handlers. All logic lives in services."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from pixel_dungeon_generator.bootstrap.app import Container
from pixel_dungeon_generator.models.spec import DungeonSpec
from pixel_dungeon_generator.utils.config import load_spec

console = Console()


def register_commands(app: typer.Typer, container: Container) -> None:
    @app.command("generate")
    def generate(
        spec: Path = typer.Option(..., "--spec", "-s", help="Path to spec YAML."),
        out: Path = typer.Option(Path("out/dungeon"), "--out", "-o"),
        fmt: str = typer.Option("png", "--format", "-f"),
    ) -> None:
        """Generate a dungeon from a spec file."""
        parsed: DungeonSpec = load_spec(spec)
        for w in container.validator.validate(parsed):
            console.print(f"[yellow]warn[/yellow] {w}")
        gen = container.registry.get(parsed.generator)
        dungeon = gen.generate(parsed)
        if fmt == "png":
            path = container.export.to_png(dungeon, out)
        elif fmt == "json":
            path = container.export.to_json(dungeon, out)
        elif fmt == "tmx":
            path = container.export.to_tmx(dungeon, out)
        else:
            raise typer.BadParameter(f"unknown format {fmt!r}")
        console.print(f"[green]ok[/green] {path}")

    @app.command("packs")
    def packs() -> None:
        """List available tilepacks."""
        for name in container.tilepacks.list_available():
            console.print(f"  {name}")

    @app.command("generators")
    def generators() -> None:
        """List registered generators."""
        for name in container.registry.names():
            console.print(f"  {name}")