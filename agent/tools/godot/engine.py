"""godot/engine tools — UID generation, scene running, errors."""

from godot.bridge import GodotBridge
from godot.lsp import GodotLSP


async def generate_uid(bridge: GodotBridge, **_) -> str:
    return await bridge.generate_uid()


async def run_scene(path: str, bridge: GodotBridge, timeout: int = 5, **_) -> str:
    return await bridge.run_scene(path, timeout)


async def get_errors(lsp: GodotLSP, path: str = None, **_) -> list:
    return await lsp.get_errors(path)
