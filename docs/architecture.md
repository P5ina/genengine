# Architecture

## Overview

genengine consists of two main parts:

1. **Godot Plugin** (GDScript) — UI panel inside Godot Editor, bridge to agent
2. **Agent Server** (Python binary) — AI agent with tools, launched by the plugin

## Component Diagram

```
┌─────────────────────────────────────────────┐
│                Godot Editor                  │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │         genengine Plugin             │   │
│  │  ┌─────────────┐  ┌──────────────┐  │   │
│  │  │  Chat Panel │  │ Bridge Client│  │   │
│  │  │  (UI)       │  │ (TCP :7821)  │  │   │
│  │  └─────────────┘  └──────┬───────┘  │   │
│  └─────────────────────────-┼──────────┘   │
│                              │               │
│  ┌───────────────────────────┼──────────┐   │
│  │       Godot Headless      │          │   │
│  │  ┌──────────┐  ┌──────────▼───────┐  │   │
│  │  │ LSP :6005│  │  Bridge Server   │  │   │
│  │  │ (errors) │  │  (commands)      │  │   │
│  │  └────┬─────┘  └──────────────────┘  │   │
│  └───────┼────────────────────────────--┘   │
└──────────┼──────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────┐
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
Plugin sends user messages over TCP to agent server (port 7821, localhost only).

### Agent → Godot
Agent calls tools that communicate with Godot via the Bridge (GDScript TCP server on port 7822).

### Agent → LSP
Agent connects to Godot's built-in LSP server (port 6005) to get diagnostics and errors.

## Ports

| Port | Service |
|------|---------|
| 7821 | Agent Server (plugin connects here) |
| 7822 | Godot Bridge (agent connects here) |
| 6005 | Godot LSP |

## Startup Sequence

```
1. User enables plugin
2. plugin.gd detects OS, picks correct binary from bin/
3. Launches binary: ./bin/genengine-linux-x64
4. Agent starts, listens on :7821
5. Agent launches Godot headless with bridge.gd
6. Godot headless starts LSP on :6005, bridge on :7822
7. Agent connects to both
8. Plugin connects to agent on :7821
9. Ready
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
