"""godot/input_map tools — configure input actions."""

from godot.bridge import GodotBridge

# Common key scancode mapping
KEY_MAP = {
    "space": "KEY_SPACE", "enter": "KEY_ENTER", "escape": "KEY_ESCAPE",
    "w": "KEY_W", "a": "KEY_A", "s": "KEY_S", "d": "KEY_D",
    "up": "KEY_UP", "down": "KEY_DOWN", "left": "KEY_LEFT", "right": "KEY_RIGHT",
    "shift": "KEY_SHIFT", "ctrl": "KEY_CTRL", "e": "KEY_E", "f": "KEY_F",
    "1": "KEY_1", "2": "KEY_2", "3": "KEY_3", "4": "KEY_4",
}


async def setup_input_actions(
    actions: dict,
    bridge: GodotBridge = None,
    **_
) -> str:
    """
    Add input actions to project.godot.
    actions = {
        "move_left":  ["a", "left"],
        "move_right": ["d", "right"],
        "jump":       ["space", "w", "up"],
        "interact":   ["e"],
    }
    """
    project_content = await bridge.read_file("res://project.godot")

    input_section = "\n[input]\n\n"
    for action, keys in actions.items():
        events = ", ".join([
            f'Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":{KEY_MAP.get(k, "KEY_" + k.upper())},"physical_keycode":0,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)'
            for k in keys
        ])
        input_section += f'{action}={{"deadzone": 0.5, "events": [{events}]}}\n\n'

    # Append to project.godot if [input] section doesn't exist
    if "[input]" not in project_content:
        project_content += input_section
    else:
        # Insert actions into existing [input] section
        parts = project_content.split("[input]")
        project_content = parts[0] + "[input]\n" + input_section + parts[1]

    await bridge.write_file("res://project.godot", project_content)
    return f"Input actions configured: {', '.join(actions.keys())}"
