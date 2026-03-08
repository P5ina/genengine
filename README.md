# genengine

> AI-powered game development inside Godot. Describe your idea — the agent writes code, generates assets, builds scenes.

Part of the [gensprite](https://gensprite.ai) ecosystem.

## What is this?

genengine is a Godot plugin that bundles an AI agent capable of:

- Writing GDScript code
- Generating sprites and tilesets via gensprite
- Creating and editing scenes (.tscn)
- Generating tilemaps from text descriptions
- Catching and fixing errors via Godot LSP

You describe what you want. The agent does it inside your Godot project.

## How it works

```
[Godot Editor]
      ↕ TCP
[genengine plugin]
      ↕
[Agent Server]  ←→  [Claude API]
      ↕                   ↕
[Godot Bridge]      [gensprite API]
      ↕
[Godot Headless (LSP + UID + validation)]
```

The plugin launches the agent binary automatically when enabled. No separate installation needed.

## Installation

1. Download the latest release
2. Copy `addons/genengine` into your Godot project
3. Enable the plugin in Project → Project Settings → Plugins
4. Enter your genengine API key in the plugin settings
5. Start describing your game

## Architecture

See [docs/architecture.md](docs/architecture.md) for full technical details.

## Status

🚧 Early development
