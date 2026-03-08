"""godot/fs tools — file system operations."""

from godot.bridge import GodotBridge
from godot.lsp import GodotLSP


async def read_file(path: str, bridge: GodotBridge, **_) -> str:
    return await bridge.read_file(path)


async def write_file(path: str, content: str, bridge: GodotBridge, **_) -> str:
    await bridge.write_file(path, content)
    return f"Written: {path}"


async def create_script(path: str, content: str, bridge: GodotBridge, **_) -> str:
    if not path.endswith(".gd"):
        return "Error: path must end with .gd"
    await bridge.write_file(path, content)
    return f"Script created: {path}"


async def list_files(path: str, bridge: GodotBridge, **_) -> list[str]:
    return await bridge.list_files(path)


async def delete_file(path: str, bridge: GodotBridge, **_) -> str:
    await bridge.call("delete_file", {"path": path})
    return f"Deleted: {path}"
