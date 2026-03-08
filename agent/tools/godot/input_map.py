"""godot/input_map tools — configure input actions via bridge (InputMap API)."""

from godot.bridge import GodotBridge


async def setup_input_actions(
    actions: dict,
    bridge: GodotBridge = None,
    **_
) -> str:
    """
    Add input actions via Godot's InputMap/ProjectSettings API through the bridge.
    The bridge executes this natively inside the editor — no manual file editing.

    actions = {
        "move_left":  ["a", "left"],
        "move_right": ["d", "right"],
        "jump":       ["space", "w", "up"],
        "interact":   ["e"],
    }
    """
    result = await bridge.call("setup_input_actions", {"actions": actions})
    return f"Input actions configured: {', '.join(actions.keys())}"
