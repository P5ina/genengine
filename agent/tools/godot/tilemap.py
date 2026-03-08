"""godot/tilemap tools — fill tilemaps from grids."""

from godot.bridge import GodotBridge


async def load_from_grid(
    scene_path: str,
    node_path: str,
    grid: list[list[int]],
    layer: int = 0,
    bridge: GodotBridge = None,
    **_
) -> str:
    result = await bridge.call("fill_tilemap", {
        "scene_path": scene_path,
        "node_path": node_path,
        "grid": grid,
        "layer": layer,
    })
    return f"TileMap filled: {len(grid)}x{len(grid[0])} tiles"
