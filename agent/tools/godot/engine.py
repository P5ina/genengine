"""godot/engine tools — UID generation, scene running, errors."""

import asyncio
import os
from godot.bridge import GodotBridge
from godot.lsp import GodotLSP


async def generate_uid(bridge: GodotBridge, **_) -> str:
    """Ask the plugin to generate a UID via ResourceUID.create_id()."""
    return await bridge.generate_uid()


async def run_scene(path: str, bridge: GodotBridge, timeout: int = 5, **_) -> str:
    """
    Run a scene for testing. Spawns a temporary Godot headless process,
    captures output, then kills it. Only used for test runs.
    """
    godot_bin = os.environ.get("GODOT_BIN", "godot")
    project_path = await bridge.call("get_project_path")
    try:
        proc = await asyncio.create_subprocess_exec(
            godot_bin, "--headless", "--path", project_path, path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        return stdout.decode()
    except asyncio.TimeoutError:
        proc.kill()
        return f"Scene ran for {timeout}s (timeout), no crash detected"


async def get_errors(lsp: GodotLSP, path: str = None, **_) -> list:
    """Get errors from Godot Editor's built-in LSP."""
    return await lsp.get_errors(path)
