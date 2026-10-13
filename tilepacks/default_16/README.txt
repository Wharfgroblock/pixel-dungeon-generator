default_16 — the stock 16x16 stone-biome tilepack.

Drop a `pack.yaml` in a folder next to your PNGs and point `--tilepack`
at the folder name. Tiles are validated for size against `tile_size`
at load time. Anything that resolves outside the pack root is refused
by utils.sandbox.safe_join.

Naming convention: keys must match the TileKind names in
models/dungeon.py (lowercase), e.g. floor, wall, door, water, lava.