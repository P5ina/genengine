"""
Tool Registry — registers all tools and routes calls.
"""

from typing import Any
from godot.bridge import GodotBridge
from godot.lsp import GodotLSP
from tools.godot import fs, scene, engine, tilemap, animation, ui, signals, input_map, resources, project
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
            # godot/project
            "add_autoload": project.add_autoload,
            "remove_autoload": project.remove_autoload,
            "set_collision_layer_name": project.set_collision_layer_name,
            "set_window_size": project.set_window_size,
            "rescan_filesystem": project.rescan_filesystem,
            "get_current_scene": project.get_current_scene,
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
        "description": "Write content to a file in the Godot project. Use for .gd scripts only. For scenes (.tscn) use create_scene. For resources (.tres) use the appropriate resource tool. Never write UIDs manually — always get them from generate_uid.",
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

    # ── Animation ─────────────────────────────────────────────────────────────
    {
        "name": "setup_8dir_sprite",
        "description": "Unpack a gensprite 8-direction archive (n/ne/e/se/s/sw/w/nw) and configure AnimatedSprite2D with a direction helper script",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path":      {"type": "string", "description": "Scene that contains the AnimatedSprite2D"},
                "node_path":       {"type": "string", "description": "Path to AnimatedSprite2D node"},
                "archive_path":    {"type": "string", "description": "Path to .zip from gensprite"},
                "animation_name":  {"type": "string", "default": "walk"},
                "fps":             {"type": "integer", "default": 8}
            },
            "required": ["scene_path", "node_path", "archive_path"]
        }
    },
    {
        "name": "setup_animated_sprite",
        "description": "Configure AnimatedSprite2D from a spritesheet with named animations",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path":   {"type": "string"},
                "node_path":    {"type": "string"},
                "texture_path": {"type": "string"},
                "animations": {
                    "type": "object",
                    "description": "e.g. {\"idle\": {\"frames\": 4, \"fps\": 8}, \"run\": {\"frames\": 6, \"fps\": 12}}"
                }
            },
            "required": ["scene_path", "node_path", "texture_path", "animations"]
        }
    },

    # ── UI ────────────────────────────────────────────────────────────────────
    {
        "name": "create_hud",
        "description": "Create a HUD CanvasLayer scene with labels, health bars, and buttons",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path": {"type": "string"},
                "elements": {
                    "type": "array",
                    "description": "List of UI elements. Each: {type: label|health_bar|button, name, text?, position, max?}"
                }
            },
            "required": ["scene_path", "elements"]
        }
    },
    {
        "name": "create_menu",
        "description": "Create a menu scene with a title and buttons",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path": {"type": "string"},
                "title":      {"type": "string"},
                "buttons":    {"type": "array", "items": {"type": "string"}}
            },
            "required": ["scene_path", "title", "buttons"]
        }
    },

    # ── Signals ───────────────────────────────────────────────────────────────
    {
        "name": "connect_signal",
        "description": "Connect a signal between two nodes in a .tscn file",
        "input_schema": {
            "type": "object",
            "properties": {
                "scene_path":   {"type": "string"},
                "from_node":    {"type": "string", "description": "Node path, e.g. Player"},
                "signal_name":  {"type": "string"},
                "to_node":      {"type": "string"},
                "method":       {"type": "string"}
            },
            "required": ["scene_path", "from_node", "signal_name", "to_node", "method"]
        }
    },

    # ── Project Settings ──────────────────────────────────────────────────────
    {
        "name": "add_autoload",
        "description": "Add an autoload singleton to the project (e.g. SaveManager, GameManager)",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Autoload name, e.g. SaveManager"},
                "path": {"type": "string", "description": "Script path, e.g. res://scripts/SaveManager.gd"}
            },
            "required": ["name", "path"]
        }
    },
    {
        "name": "remove_autoload",
        "description": "Remove an autoload singleton from the project",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "set_collision_layer_name",
        "description": "Name a 2D physics collision layer for readability",
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {"type": "integer", "description": "Layer number 1-32"},
                "name":  {"type": "string", "description": "e.g. player, enemies, world"}
            },
            "required": ["layer", "name"]
        }
    },
    {
        "name": "set_window_size",
        "description": "Set the game window/viewport size",
        "input_schema": {
            "type": "object",
            "properties": {
                "width":  {"type": "integer"},
                "height": {"type": "integer"}
            },
            "required": ["width", "height"]
        }
    },
    {
        "name": "rescan_filesystem",
        "description": "Tell Godot Editor to rescan the project filesystem. Call this after writing files so Godot picks up the changes.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_current_scene",
        "description": "Get the path of the scene currently open in the Godot Editor",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
]
