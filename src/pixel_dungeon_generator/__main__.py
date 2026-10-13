"""CLI entrypoint. `pdn generate --spec dungeon.yaml --seed 6767`."""
from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from pixel_dungeon_generator.bootstrap.app import build_container
from pixel_dungeon_generator.handlers.cli_handlers import register_commands

app = typer.Typer(
    name="pdn",
    help="AI pixel dungeon / level generator.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def _main() -> None:
    container = build_container(Path("config/default.yaml"))
    register_commands(app, container)
    app()


if __name__ == "__main__":
    try:
        _main()
    except KeyboardInterrupt:
        console.print("[yellow]interrupted[/yellow]")
        sys.exit(130)