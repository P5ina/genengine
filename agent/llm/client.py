"""
LLM Client — wraps Anthropic API with tool use support.
"""

import os
from typing import AsyncGenerator, Callable, Any
import anthropic

SYSTEM_PROMPT = """You are genengine — an AI agent that helps create games inside Godot Engine.

You have access to tools that let you:
- Read and write files in the Godot project
- Create and edit scenes (.tscn)
- Generate sprites and assets via gensprite
- Generate tilemaps from descriptions
- Check for errors via Godot LSP
- Run scenes to test them

When the user describes what they want:
1. Break it down into concrete steps
2. Use tools to implement each step
3. Check for errors after writing code
4. Fix errors if found
5. Report what you built

Be direct. Don't explain what you're about to do — just do it.
After completing, give a brief summary of what was created.

Important Godot rules:
- Always generate UIDs for new resources using generate_uid tool
- Use @export for variables that should be editable in Inspector
- CharacterBody2D for players/enemies, Area2D for triggers/pickups
- Signals over direct function calls when possible
"""


class LLMClient:
    def __init__(self, tools: list[dict]):
        self.client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.tools = tools
        self.history = []

    async def run(
        self,
        user_message: str,
        tool_handler: Callable[[str, dict], Any],
    ) -> AsyncGenerator[dict, None]:
        self.history.append({"role": "user", "content": user_message})

        while True:
            response = await self.client.messages.create(
                model="claude-opus-4-5",
                max_tokens=8096,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=self.history,
            )

            # Stream text to plugin
            for block in response.content:
                if block.type == "text":
                    yield {"type": "text", "text": block.text}

            # Handle tool use
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        yield {"type": "tool_call", "name": block.name, "input": block.input}

                        result = await tool_handler(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        })

                        yield {"type": "tool_result", "name": block.name, "result": str(result)}

                self.history.append({"role": "assistant", "content": response.content})
                self.history.append({"role": "user", "content": tool_results})

            else:
                # Done
                self.history.append({"role": "assistant", "content": response.content})
                yield {"type": "done"}
                break
