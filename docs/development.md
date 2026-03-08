# Development Setup

How to run genengine locally without building a binary.

## Requirements

- Python 3.11+
- Godot 4.x
- API keys: Anthropic, gensprite

## 1. Clone the repo

```bash
git clone https://github.com/P5ina/genengine
cd genengine
```

## 2. Set up Python environment

```bash
cd agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure API keys

Create `agent/.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
GENSPRITE_API_KEY=...
GODOT_BIN=godot          # or full path: /usr/bin/godot4
```

## 4. Install the plugin in a Godot project

Copy the plugin folder into your Godot project:

```bash
cp -r godot-plugin/addons/genengine /path/to/your/godot/project/addons/
```

Then in Godot:
- **Project → Project Settings → Plugins**
- Enable **genengine**

The plugin will try to launch a binary from `addons/genengine/bin/` — in dev mode we skip this and run the agent manually.

## 5. Disable auto-launch in dev mode

In `plugin.gd`, comment out `_start_agent()` in `_enable_plugin()`:

```gdscript
func _enable_plugin() -> void:
    # _start_agent()  ← comment this out during development
    _start_bridge()
    _add_chat_panel()
```

## 6. Run the agent manually

```bash
cd agent
source .venv/bin/activate
python main.py
```

You should see:
```
2026-03-09 [INFO] Waiting for Godot bridge... (1/10)
2026-03-09 [INFO] Connected to Godot bridge on :7822
2026-03-09 [INFO] Connected to Godot LSP on :6005
2026-03-09 [INFO] Agent listening on 127.0.0.1:7821
```

## 7. Open Godot

Open your project in Godot Editor. The plugin should be active — you'll see the genengine chat panel in the dock.

**Order matters:**
1. Start agent first (`python main.py`)
2. Then open Godot (or re-enable the plugin)

The agent waits up to 10 seconds for the bridge, so you have some margin.

## 8. Test the bridge

To quickly verify the bridge works without the full agent, run:

```bash
cd agent
python -c "
import asyncio
from godot.bridge import GodotBridge

async def test():
    b = GodotBridge()
    await b.connect()
    uid = await b.generate_uid()
    print('UID from Godot:', uid)

asyncio.run(test())
"
```

If you see a `uid://...` string — the bridge is working.

## Project Structure

```
agent/
├── main.py              # Entry point
├── .env                 # Your API keys (not committed)
├── llm/client.py        # Claude integration
├── godot/
│   ├── bridge.py        # TCP client → plugin bridge server
│   └── lsp.py           # LSP client → Godot editor LSP
└── tools/
    ├── __init__.py      # Tool registry + Claude definitions
    ├── godot/           # fs, scene, engine, tilemap, animation, ui, signals, input_map, project, resources
    └── gensprite/       # assets

godot-plugin/addons/genengine/
├── plugin.cfg
├── plugin.gd            # Bridge server + editor integration
├── ui/
│   ├── chat_panel.gd
│   └── chat_panel.tscn
└── bin/                 # Compiled binaries (for releases only)
```

## Ports

| Port | What |
|------|------|
| 7821 | Agent server (plugin → agent) |
| 7822 | Bridge server (agent → plugin) |
| 6005 | Godot LSP (built into editor) |

## Common Issues

**Agent can't connect to bridge**
→ Make sure the plugin is enabled in Godot and `_start_bridge()` ran.
→ Check that port 7822 is not taken: `ss -tlnp | grep 7822`

**LSP connection refused**
→ Godot LSP starts after the editor fully loads. Wait a few seconds and retry.
→ LSP port can be changed in Editor Settings → Network → Language Server.

**`generate_uid` returns empty**
→ Bridge connected but Godot returned an error. Check Godot's Output panel for errors in plugin.gd.

**Chat panel missing**
→ `chat_panel.tscn` must be in `addons/genengine/ui/`. Re-copy the plugin folder.
