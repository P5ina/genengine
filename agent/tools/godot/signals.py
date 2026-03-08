"""godot/signals tools — connect signals between nodes."""

from godot.bridge import GodotBridge


async def connect_signal(
    scene_path: str,
    from_node: str,
    signal_name: str,
    to_node: str,
    method: str,
    bridge: GodotBridge = None,
    **_
) -> str:
    """
    Add a signal connection to a .tscn file.
    Appends connection metadata that Godot reads on scene load.
    """
    connection_line = (
        f'\n[connection signal="{signal_name}" '
        f'from="{from_node}" '
        f'to="{to_node}" '
        f'method="{method}"]\n'
    )

    content = await bridge.read_file(scene_path)
    content += connection_line
    await bridge.write_file(scene_path, content)

    return f"Signal connected: {from_node}.{signal_name} → {to_node}.{method}"
