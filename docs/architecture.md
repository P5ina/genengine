# Architecture

## Overview

genengine consists of two main parts:

1. **Godot Plugin** (GDScript) — UI panel inside Godot Editor, bridge server, launched by the user enabling the plugin
2. **Agent Server** (Python binary) — AI agent with tools, launched automatically by the plugin

## Component Diagram

```
┌─────────────────────────────────────────────┐
│                Godot Editor                  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         genengine Plugin             │   │
│  │  ┌─────────────┐  ┌──────────────┐  │   │
│  │  │  Chat Panel │  │Bridge Server │  │   │
│  │  │  (UI)       │  │ (TCP :7822)  │  │   │
│  │  └─────────────┘  └──────▲───────┘  │   │
│  │                           │          │   │
│  │  ┌────────────────────┐   │          │   │
│  │  │  Built-in LSP      │   │          │   │
│  │  │  (:6005)           │   │          │   │
│  │  └────────────────────┘   │          │   │
│  └───────────────────────────┼──────────┘   │
└──────────────────────────────┼──────────────┘
                               │
┌──────────────────────────────▼──────────────┐
│              Agent Server (Python)           │
│                                              │
│  ┌─────────────┐    ┌──────────────────┐    │
│  │ LLM Client  │    │  Tool Registry   │    │
│  │ (Anthropic) │    │                  │    │
│  └──────┬──────┘    │  godot/fs        │    │
│         │           │  godot/scene     │    │
│         └──────────►│  godot/lsp       │    │
│                     │  godot/engine    │    │
│                     │  godot/tilemap   │    │
│                     │  gensprite/asset │    │
│                     └──────────────────┘    │
└─────────────────────────────────────────────┘
           │                    │
           ▼                    ▼
    [Claude API]        [gensprite API]
```

## Communication Flow

### Plugin → Agent
Plugin launches the agent binary on startup. User messages are sent over TCP (port 7821, localhost only).

### Agent → Godot (Bridge)
Agent calls tools that send commands to the Bridge Server running inside the plugin (port 7822).
The plugin handles everything natively: file I/O via `FileAccess`, UID via `ResourceUID`, scene parsing, etc.
No separate Godot headless instance needed — the plugin **is** the bridge into Godot.

### Agent → LSP
Agent connects to Godot Editor's built-in LSP server (port 6005) to get diagnostics and errors.
The LSP is already running as part of the editor — no extra process needed.

### Run Scene (special case)
When the agent needs to actually *run* a scene for testing, it spawns a temporary Godot headless process just for that, then kills it. This is the only case where a separate Godot process is used.

## Ports

| Port | Service |
|------|---------|
| 7821 | Agent Server (plugin connects here) |
| 7822 | Bridge Server inside plugin (agent connects here) |
| 6005 | Godot Editor built-in LSP |

## Startup Sequence

```
1. User enables plugin in Godot Editor
2. plugin.gd starts Bridge Server on :7822
3. plugin.gd detects OS, picks correct binary from bin/
4. Launches binary: ./bin/genengine-linux-x64
5. Agent starts, connects to Bridge on :7822
6. Agent connects to LSP on :6005
7. Agent listens for plugin on :7821
8. Plugin connects to agent on :7821
9. Ready — chat panel is active
```

## Agent Tools

See [tools.md](tools.md) for full tool reference.

## Build

Agent is built into a single binary per platform using PyInstaller:

```
bin/genengine-linux-x64
bin/genengine-windows-x64.exe
bin/genengine-macos-arm64
```

Binaries are distributed via GitHub Releases, not committed to the repo.
