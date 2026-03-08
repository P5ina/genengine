"""
Tool Registry — registers all tools and routes calls.
"""

from typing import Any
from godot.bridge import GodotBridge
from godot.lsp import GodotLSP
from tools.godot import fs, scene, engine, tilemap, animation, ui, signals, input_map, resources
from tools.gensprite import assets


class ToolRegistry:
    def __init__(self, bridge: GodotBridge, lsp: GodotLSP):
        self.bridge = bridge
        self.lsp = lsp
        self._handlers = {
            # godot/fs
            "read_file": fs.read_file,
            "write_file": fs.write_file,
            "create_script": fs.create_script,
            "list_files": fs.list_files,
            "delete_file": fs.delete_file,
            # godot/scene
            "get_scene_tree": scene.get_scene_tree,
            "create_scene": scene.create_scene,
            # godot/engine
            "generate_uid": engine.generate_uid,
            "run_scene": engine.run_scene,
            "get_errors": engine.get_errors,
            # godot/tilemap
            "load_tilemap_from_grid": tilemap.load_from_grid,
            # godot/animation
            "setup_8dir_sprite": animation.setup_8dir_sprite,
            "setup_animated_sprite": animation.setup_animated_sprite,
            # godot/ui
            "create_hud": ui.create_hud,
            "create_menu": ui.create_menu,
            # godot/signals
            "connect_signal": signals.connect_signal,
            # godot/input_map
            "setup_input_actions": input_map.setup_input_actions,
            # godot/resources
            "create_tileset": resources.create_tileset,
            "create_save_system": resources.create_save_system,
            # gensprite
            "generate_sprite": assets.generate_sprite,
            "generate_tileset": assets.generate_tileset,
        }

    def get_definitions(self) -> list[dict]:
        """Return tool definitions for Claude."""
        return TOOL_DEFINITIONS

    async def call(self, name: str, input: dict) -> Any:
        handler = self._handlers.get(name)
        if not handler:
            return f"Unknown tool: {name}"
        try:
            return await handler(bridge=self.bridge, lsp=self.lsp, **input)
        except Exception as e:
            return f"Tool error ({name}): {e}"


TOOL_DEFINITIONS = [
    {
        "name": "read_file",
        "description": "Read a file from the Godot project",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Project path, e.g. res://scripts/Player.gd"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file in the Godot project",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "create_script",
        "description": "Create a new GDScript file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "e.g. res://scripts/Player.gd"},
                "content": {"type": "string", "description": "GDScript code"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "list_files",
        "description": "List files in a project directory",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "e.g. res://scripts/"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "get_scene_tree",
        "description": "Get the node tree of a .tscn scene file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "e.g. res://scenes/Main.tscn"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "create_scene",
        "description": "Create a new Godot scene (.tscn) with nodes",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "root_type": {"type": "string", "description": "Root node type, e.g. Node2D"},
                "root_name": {"type": "string"}
            },
            "required": ["path", "root_type", "root_name"]
        }
    },
    {
        "name": "generate_uid",
        "description": "Generate a valid Godot resource UID",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_errors",
        "description": "Get current errors and warnings from Godot LSP",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Optional: filter by file path"}
            }
        }
    },
    {
        "name": "run_scene",
        "description": "Run a scene headless and return output/errors",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "e.g. res://scenes/Main.tscn"},
                "timeout": {"type": "integer", "description": "Seconds to run, default 5"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "load_tilemap_from_grid",
        "description": "Fill a TileMap node from a 2D array of tile IDs",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path": {"type": "string"},
                "node_path": {"type": "string", "description": "Path to TileMap node"},
                "grid": {"type": "array", "description": "2D array of tile IDs"},
                "layer": {"type": "integer", "default": 0}
            },
            "required": ["scene_path", "node_path", "grid"]
        }
    },
    {
        "name": "generate_sprite",
        "description": "Generate a sprite image via gensprite API",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Description of the sprite"},
                "output_path": {"type": "string", "description": "Where to save in project, e.g. res://assets/player.png"},
                "width": {"type": "integer", "default": 64},
                "height": {"type": "integer", "default": 64}
            },
            "required": ["prompt", "output_path"]
        }
    },
    {
        "name": "generate_tileset",
        "description": "Generate a tileset image via gensprite API",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "output_path": {"type": "string"},
                "tile_size": {"type": "integer", "default": 16}
            },
            "required": ["prompt", "output_path"]
        }
    },
]
