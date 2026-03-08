"""godot/ui tools — HUD, menus, UI scenes."""

from godot.bridge import GodotBridge


async def create_hud(
    scene_path: str,
    elements: list[dict],
    bridge: GodotBridge = None,
    **_
) -> str:
    """
    Create a HUD scene with UI elements.
    elements = [
        {"type": "label", "name": "ScoreLabel", "text": "Score: 0", "position": [16, 16]},
        {"type": "health_bar", "name": "HealthBar", "max": 100},
    ]
    """
    uid = await bridge.generate_uid()
    nodes = []

    for el in elements:
        t = el.get("type", "label")
        name = el.get("name", "Element")
        pos = el.get("position", [0, 0])

        if t == "label":
            nodes.append(
                f'[node name="{name}" type="Label" parent="."]\n'
                f'position = Vector2({pos[0]}, {pos[1]})\n'
                f'text = "{el.get("text", "")}"\n'
            )
        elif t == "health_bar":
            max_val = el.get("max", 100)
            nodes.append(
                f'[node name="{name}" type="ProgressBar" parent="."]\n'
                f'position = Vector2({pos[0]}, {pos[1]})\n'
                f'size = Vector2(200, 20)\n'
                f'max_value = {max_val}\n'
                f'value = {max_val}\n'
            )
        elif t == "button":
            nodes.append(
                f'[node name="{name}" type="Button" parent="."]\n'
                f'position = Vector2({pos[0]}, {pos[1]})\n'
                f'text = "{el.get("text", "Button")}"\n'
            )

    content = f'[gd_scene load_steps=1 format=3 uid="{uid}"]\n\n'
    content += '[node name="HUD" type="CanvasLayer"]\n\n'
    content += "\n".join(nodes)

    await bridge.call("write_file", {"path": scene_path, "content": content})
    return f"HUD created: {scene_path} with {len(elements)} elements"


async def create_menu(
    scene_path: str,
    title: str,
    buttons: list[str],
    bridge: GodotBridge = None,
    **_
) -> str:
    """Create a simple menu scene with title and buttons."""
    uid = await bridge.generate_uid()

    btn_nodes = ""
    for i, btn_text in enumerate(buttons):
        btn_nodes += (
            f'[node name="Btn{i}" type="Button" parent="VBox"]\n'
            f'text = "{btn_text}"\n\n'
        )

    content = f"""[gd_scene load_steps=1 format=3 uid="{uid}"]

[node name="Menu" type="Control"]
anchor_right = 1.0
anchor_bottom = 1.0

[node name="VBox" type="VBoxContainer" parent="."]
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -100.0
offset_top = -100.0
offset_right = 100.0
offset_bottom = 100.0

[node name="Title" type="Label" parent="VBox"]
text = "{title}"

{btn_nodes}"""

    await bridge.call("write_file", {"path": scene_path, "content": content})
    return f"Menu created: {scene_path} with buttons: {', '.join(buttons)}"
