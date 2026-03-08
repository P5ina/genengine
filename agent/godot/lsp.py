"""
Godot LSP Client — connects to Godot's built-in Language Server.
Used to get errors and diagnostics.
"""

import asyncio
import json
import logging
from typing import Optional

log = logging.getLogger(__name__)


class GodotLSP:
    def __init__(self, port: int = 6005, host: str = "127.0.0.1"):
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None
        self._diagnostics: dict[str, list] = {}
        self._msg_id = 0

    async def connect(self, retries: int = 10, delay: float = 1.0):
        for i in range(retries):
            try:
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                await self._initialize()
                asyncio.create_task(self._listen())
                log.info(f"Connected to Godot LSP on :{self.port}")
                return
            except ConnectionRefusedError:
                log.info(f"Waiting for Godot LSP... ({i+1}/{retries})")
                await asyncio.sleep(delay)
        raise RuntimeError("Could not connect to Godot LSP")

    async def _initialize(self):
        await self._send({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "processId": None,
                "clientInfo": {"name": "genengine"},
                "capabilities": {},
                "rootUri": None,
            }
        })

    async def _listen(self):
        """Background task: receive LSP messages and update diagnostics."""
        while True:
            try:
                msg = await self._recv()
                if msg and msg.get("method") == "textDocument/publishDiagnostics":
                    uri = msg["params"]["uri"]
                    self._diagnostics[uri] = msg["params"]["diagnostics"]
            except Exception as e:
                log.error(f"LSP listen error: {e}")
                break

    async def get_errors(self, path: Optional[str] = None) -> list[dict]:
        """Return current diagnostics, optionally filtered by file path."""
        errors = []
        for uri, diagnostics in self._diagnostics.items():
            if path and path not in uri:
                continue
            for d in diagnostics:
                if d.get("severity", 1) <= 2:  # 1=Error, 2=Warning
                    errors.append({
                        "file": uri,
                        "line": d["range"]["start"]["line"],
                        "message": d["message"],
                        "severity": "error" if d.get("severity") == 1 else "warning",
                    })
        return errors

    def _next_id(self) -> int:
        self._msg_id += 1
        return self._msg_id

    async def _send(self, msg: dict):
        body = json.dumps(msg)
        header = f"Content-Length: {len(body)}\r\n\r\n"
        self.writer.write((header + body).encode())
        await self.writer.drain()

    async def _recv(self) -> Optional[dict]:
        header = await self.reader.readuntil(b"\r\n\r\n")
        length = int(header.split(b"Content-Length: ")[1].split(b"\r\n")[0])
        body = await self.reader.readexactly(length)
        return json.loads(body)
