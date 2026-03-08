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
