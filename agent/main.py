"""
genengine Agent Server
Listens on localhost:7821, communicates with Godot plugin.
"""

import asyncio
import json
import logging
import signal
import sys
from typing import Optional

from llm.client import LLMClient
from tools import ToolRegistry
from godot.bridge import GodotBridge
from godot.lsp import GodotLSP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

AGENT_PORT = 7821
BRIDGE_PORT = 7822
LSP_PORT = 6005


class AgentServer:
    def __init__(self):
        self.bridge = GodotBridge(port=BRIDGE_PORT)
        self.lsp = GodotLSP(port=LSP_PORT)
        self.tools = ToolRegistry(bridge=self.bridge, lsp=self.lsp)
        self.llm = LLMClient(tools=self.tools.get_definitions())

    async def start(self):
        log.info("Starting genengine agent server...")

        # Wait for Godot bridge and LSP to be ready
        await self.bridge.connect()
        await self.lsp.connect()

        server = await asyncio.start_server(
            self.handle_client,
            host="127.0.0.1",
            port=AGENT_PORT,
        )
        log.info(f"Agent listening on 127.0.0.1:{AGENT_PORT}")

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        log.info("Plugin connected")
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                message = json.loads(data.decode())
                log.info(f"User: {message.get('text', '')}")

                # Stream response back to plugin
                async for chunk in self.llm.run(
                    user_message=message["text"],
                    tool_handler=self.tools.call,
                ):
                    writer.write((json.dumps(chunk) + "\n").encode())
                    await writer.drain()

        except Exception as e:
            log.error(f"Client error: {e}")
        finally:
            writer.close()
            log.info("Plugin disconnected")


async def main():
    server = AgentServer()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    await server.start()


async def shutdown():
    log.info("Shutting down...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
