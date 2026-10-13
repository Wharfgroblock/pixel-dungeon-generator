# Contributing to pixel-dungeon-generator

Thanks for wanting to push tiles. This repo is a hobbyist/open-source
pixel dungeon and level generator. We use it to study procedural
generation, wave function collapse, and diffusion-based tile synthesis.
Pull requests that add generators, tile packs, exporters, or fixes to the
existing pipeline are welcome.

## Ground rules

- Python 3.11+ is the target runtime. Windows is the primary platform,
  but nothing should hard-break on Linux/macOS.
- One feature per PR. Large refactors need an issue first.
- Every new service must ship with at least one unit test under `tests/`.
- Do not commit model checkpoints (`.pt`, `.onnx`, `.pdn`). They go in
  `models/checkpoints/` locally and are gitignored.
- Keep the public API in `services/` stable. Handlers are allowed to
  churn.

## Dev setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest -q
```

## Style

- `ruff` for lint, `black` for format, `mypy --strict` on `services/`.
- Type hints are mandatory on public functions.
- No `print()` in library code. Use the `utils.logging` logger.

## Adding a generator

1. Subclass `services.generation.base.BaseGenerator`.
2. Implement `generate(spec: DungeonSpec) -> Dungeon`.
3. Register it in `services/generation/registry.py`.
4. Add a fixture dungeon to `tests/test_generators.py`.

## Reporting bugs

Open an issue with: Python version, generator used, the seed, and the
spec you passed in. Dungeons are deterministic given a seed — include it.