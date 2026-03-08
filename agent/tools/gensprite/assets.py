"""gensprite/assets tools — generate sprites and tilesets."""

import os
import httpx
from godot.bridge import GodotBridge


GENSPRITE_API = os.environ.get("GENSPRITE_API_URL", "https://gensprite.ai/api")
GENSPRITE_KEY = os.environ.get("GENSPRITE_API_KEY", "")


async def generate_sprite(
    prompt: str,
    output_path: str,
    width: int = 64,
    height: int = 64,
    bridge: GodotBridge = None,
    **_
) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GENSPRITE_API}/generate",
            json={"prompt": prompt, "width": width, "height": height},
            headers={"Authorization": f"Bearer {GENSPRITE_KEY}"},
            timeout=60,
        )
        response.raise_for_status()
        image_bytes = response.content

    # Write image to Godot project via bridge
    import base64
    b64 = base64.b64encode(image_bytes).decode()
    await bridge.call("write_file_b64", {"path": output_path, "content": b64})

    return f"Sprite saved: {output_path} ({width}x{height})"


async def generate_tileset(
    prompt: str,
    output_path: str,
    tile_size: int = 16,
    bridge: GodotBridge = None,
    **_
) -> str:
    # Tileset = sprite sheet, prompt it appropriately
    full_prompt = f"tileset spritesheet, {prompt}, {tile_size}x{tile_size} tiles, pixel art"
    return await generate_sprite(
        prompt=full_prompt,
        output_path=output_path,
        width=tile_size * 8,
        height=tile_size * 8,
        bridge=bridge,
    )
