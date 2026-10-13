"""Path-join helper that refuses to escape a base directory."""
from __future__ import annotations

from pathlib import Path


def safe_join(base: Path, *parts: str) -> Path:
    base_r = base.resolve()
    candidate = base_r.joinpath(*parts).resolve()
    if base_r != candidate and base_r not in candidate.parents:
        raise PermissionError(f"path escapes sandbox: {candidate} not under {base_r}")
    return candidate