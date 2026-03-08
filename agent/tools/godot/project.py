"""godot/project tools — project settings via bridge."""

from godot.bridge import GodotBridge


async def add_autoload(name: str, path: str, bridge: GodotBridge = None, **_) -> str:
    await bridge.call("add_autoload", {"name": name, "path": path})
    return f"Autoload added: {name} → {path}"


async def remove_autoload(name: str, bridge: GodotBridge = None, **_) -> str:
    await bridge.call("remove_autoload", {"name": name})
    return f"Autoload removed: {name}"


async def set_collision_layer_name(layer: int, name: str, bridge: GodotBridge = None, **_) -> str:
    await bridge.call("set_collision_layer_name", {"layer": layer, "name": name})
    return f"Collision layer {layer} named: {name}"


async def set_window_size(width: int, height: int, bridge: GodotBridge = None, **_) -> str:
    await bridge.call("set_window_size", {"width": width, "height": height})
    return f"Window size set: {width}x{height}"


async def rescan_filesystem(bridge: GodotBridge = None, **_) -> str:
    await bridge.call("rescan_filesystem")
    return "Filesystem rescanned"


async def get_current_scene(bridge: GodotBridge = None, **_) -> str:
    return await bridge.call("get_current_scene")
