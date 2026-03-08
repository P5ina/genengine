"""
Godot Bridge Client — communicates with bridge.gd running inside Godot.
Sends commands, receives results over TCP.
"""

import asyncio
import json
import logging
from typing import Any

log = logging.getLogger(__name__)


class GodotBridge:
    def __init__(self, port: int = 7822, host: str = "127.0.0.1"):
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self._lock = asyncio.Lock()

    async def connect(self, retries: int = 10, delay: float = 1.0):
        for i in range(retries):
            try:
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                log.info(f"Connected to Godot bridge on :{self.port}")
                return
            except ConnectionRefusedError:
                log.info(f"Waiting for Godot bridge... ({i+1}/{retries})")
                await asyncio.sleep(delay)
        raise RuntimeError("Could not connect to Godot bridge")

    async def call(self, command: str, params: dict = {}) -> Any:
        async with self._lock:
            payload = json.dumps({"cmd": command, "params": params}) + "\n"
            self.writer.write(payload.encode())
            await self.writer.drain()

            response = await self.reader.readline()
            result = json.loads(response.decode())

            if "error" in result:
                raise RuntimeError(f"Bridge error: {result['error']}")

            return result.get("result")

    async def read_file(self, path: str) -> str:
        return await self.call("read_file", {"path": path})

    async def write_file(self, path: str, content: str) -> bool:
        return await self.call("write_file", {"path": path, "content": content})

    async def list_files(self, path: str) -> list[str]:
        return await self.call("list_files", {"path": path})

    async def get_scene_tree(self, path: str) -> dict:
        return await self.call("get_scene_tree", {"path": path})

    async def generate_uid(self) -> str:
        return await self.call("generate_uid")

    async def run_scene(self, path: str, timeout: int = 5) -> str:
        return await self.call("run_scene", {"path": path, "timeout": timeout})
