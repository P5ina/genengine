"""godot/scene tools — scene creation and manipulation."""

from godot.bridge import GodotBridge
from godot.lsp import GodotLSP


async def get_scene_tree(path: str, bridge: GodotBridge, **_) -> dict:
    return await bridge.get_scene_tree(path)


async def create_scene(path: str, root_type: str, root_name: str, bridge: GodotBridge, **_) -> str:
    uid = await bridge.generate_uid()
    content = f"""[gd_scene load_steps=1 format=3 uid="{uid}"]

[node name="{root_name}" type="{root_type}"]
"""
    await bridge.write_file(path, content)
    return f"Scene created: {path}"
