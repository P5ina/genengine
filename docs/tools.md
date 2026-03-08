# Agent Tools Reference

All tools available to the AI agent.

## godot/fs — File System

| Tool | Description |
|------|-------------|
| `read_file` | Read any file in the project |
| `write_file` | Write/overwrite a file |
| `create_script` | Create a new GDScript file |
| `list_files` | List files in a directory |
| `delete_file` | Delete a file |

## godot/scene — Scene Management

| Tool | Description |
|------|-------------|
| `get_scene_tree` | Get the node tree of a .tscn file |
| `create_scene` | Create a new .tscn file |
| `add_node` | Add a node to a scene |
| `set_property` | Set a node property |
| `add_script` | Attach a script to a node |

## godot/engine — Engine Operations

| Tool | Description |
|------|-------------|
| `generate_uid` | Generate a valid Godot UID via ResourceUID |
| `run_scene` | Run a scene headless, return stdout/errors |
| `validate_scene` | Load a scene and check for errors |
| `get_project_settings` | Read project.godot settings |

## godot/lsp — Language Server

| Tool | Description |
|------|-------------|
| `get_errors` | Get current diagnostics (errors, warnings) |
| `get_file_errors` | Get errors for a specific file |

## godot/animation — Animations

| Tool | Description |
|------|-------------|
| `setup_8dir_sprite` | Unpack gensprite 8-direction archive, configure AnimatedSprite2D + direction helper script |
| `setup_animated_sprite` | Configure AnimatedSprite2D from a spritesheet with named animations |

## godot/ui — UI & HUD

| Tool | Description |
|------|-------------|
| `create_hud` | Create a HUD scene (labels, health bars, buttons) |
| `create_menu` | Create a menu scene with title and buttons |

## godot/signals — Signals

| Tool | Description |
|------|-------------|
| `connect_signal` | Connect a signal between two nodes in a .tscn file |

## godot/input_map — Input

| Tool | Description |
|------|-------------|
| `setup_input_actions` | Add input actions to project.godot (keyboard/gamepad bindings) |

## godot/resources — Resources

| Tool | Description |
|------|-------------|
| `create_tileset` | Create a TileSet .tres from a tileset texture |
| `create_save_system` | Generate a SaveManager.gd autoload with save/load/reset |

## godot/tilemap — TileMap Operations

| Tool | Description |
|------|-------------|
| `create_tilemap` | Create a TileMap node with a TileSet |
| `set_tile` | Set a single tile at coordinates |
| `fill_region` | Fill a rectangular region with tiles |
| `load_from_grid` | Load a tilemap from a 2D int array |

## gensprite/assets — Asset Generation

| Tool | Description |
|------|-------------|
| `generate_sprite` | Generate a sprite from text description |
| `generate_tileset` | Generate a tileset image |
| `generate_background` | Generate a background image |

## Example Agent Loop

```
User: "Make a platformer with a player that collects coins"

Agent:
1. generate_sprite("pixel art player character, idle pose, 32x32")
   → res://assets/player.png

2. generate_sprite("pixel art gold coin, spinning, 16x16")
   → res://assets/coin.png

3. create_script("res://scripts/Player.gd", content=<player movement code>)

4. create_script("res://scripts/Coin.gd", content=<coin pickup code>)

5. create_scene("res://scenes/Main.tscn") with:
   - CharacterBody2D (Player.gd)
   - Area2D (Coin.gd) x3
   - TileMap (ground)

6. get_errors() → check for issues

7. fix if needed

→ "Done! Press F5 to play."
```
