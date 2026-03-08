@tool
extends EditorPlugin

const AGENT_PORT = 7821
const BRIDGE_PORT = 7822

var chat_panel: Control
var agent_pid: int = -1
var bridge: TCPServer
var bridge_peer: StreamPeerTCP


func _enable_plugin() -> void:
	_start_agent()
	_start_bridge()
	_add_chat_panel()


func _disable_plugin() -> void:
	_stop_agent()
	_remove_chat_panel()


# ─── Agent Process ────────────────────────────────────────────────────────────

func _start_agent() -> void:
	var binary = _get_binary_path()
	if binary.is_empty():
		push_error("genengine: unsupported OS")
		return

	if not FileAccess.file_exists(binary):
		push_error("genengine: binary not found at " + binary)
		return

	var env = {
		"ANTHROPIC_API_KEY": _get_setting("genengine/api/anthropic_key", ""),
		"GENSPRITE_API_KEY": _get_setting("genengine/api/gensprite_key", ""),
	}

	agent_pid = OS.create_process(binary, [], false)
	print("genengine: agent started (pid %d)" % agent_pid)


func _stop_agent() -> void:
	if agent_pid > 0:
		OS.kill(agent_pid)
		agent_pid = -1
		print("genengine: agent stopped")


func _get_binary_path() -> String:
	var base = get_script().resource_path.get_base_dir() + "/bin/"
	match OS.get_name():
		"Linux":   return base + "genengine-linux-x64"
		"Windows": return base + "genengine-windows-x64.exe"
		"macOS":   return base + "genengine-macos-arm64"
	return ""


# ─── Godot Bridge (TCP server for agent to call back into Godot) ──────────────

func _start_bridge() -> void:
	bridge = TCPServer.new()
	var err = bridge.listen(BRIDGE_PORT, "127.0.0.1")
	if err != OK:
		push_error("genengine: failed to start bridge on :%d" % BRIDGE_PORT)
		return
	print("genengine: bridge listening on :%d" % BRIDGE_PORT)


func _process(_delta: float) -> void:
	# Accept new bridge connections
	if bridge and bridge.is_connection_available():
		bridge_peer = bridge.take_connection()

	# Handle bridge commands
	if bridge_peer and bridge_peer.get_status() == StreamPeerTCP.STATUS_CONNECTED:
		var available = bridge_peer.get_available_bytes()
		if available > 0:
			var line = bridge_peer.get_utf8_string(available)
			_handle_bridge_command(line)


func _handle_bridge_command(raw: String) -> void:
	var json = JSON.new()
	if json.parse(raw) != OK:
		_bridge_respond({"error": "invalid json"})
		return

	var msg = json.get_data()
	var cmd = msg.get("cmd", "")
	var params = msg.get("params", {})
	var result = null

	match cmd:
		"generate_uid":
			result = ResourceUID.id_to_text(ResourceUID.create_id())
		"read_file":
			result = _read_file(params.get("path", ""))
		"write_file":
			result = _write_file(params.get("path", ""), params.get("content", ""))
		"list_files":
			result = _list_files(params.get("path", ""))
		"get_scene_tree":
			result = _get_scene_tree(params.get("path", ""))
		"get_project_path":
			result = ProjectSettings.globalize_path("res://")
		"setup_input_actions":
			result = _setup_input_actions(params.get("actions", {}))
		_:
			_bridge_respond({"error": "unknown command: " + cmd})
			return

	_bridge_respond({"result": result})


func _bridge_respond(data: Dictionary) -> void:
	if bridge_peer:
		bridge_peer.put_utf8_string(JSON.stringify(data) + "\n")


# ─── Bridge Commands ──────────────────────────────────────────────────────────

func _read_file(path: String) -> String:
	var f = FileAccess.open(path, FileAccess.READ)
	if not f:
		return ""
	return f.get_as_text()


func _write_file(path: String, content: String) -> bool:
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	var f = FileAccess.open(path, FileAccess.WRITE)
	if not f:
		return false
	f.store_string(content)
	return true


func _list_files(path: String) -> Array:
	var files = []
	var dir = DirAccess.open(path)
	if not dir:
		return files
	dir.list_dir_begin()
	var name = dir.get_next()
	while name != "":
		files.append(path + name)
		name = dir.get_next()
	return files


func _get_scene_tree(path: String) -> Dictionary:
	# Return raw .tscn content for now; agent parses it
	return {"content": _read_file(path)}


func _setup_input_actions(actions: Dictionary) -> Dictionary:
	# Add input actions via InputMap + ProjectSettings API
	# This runs natively inside the editor — no file parsing needed
	var added = []
	for action_name in actions:
		var keys: Array = actions[action_name]

		# Add action if it doesn't exist
		if not InputMap.has_action(action_name):
			InputMap.add_action(action_name, 0.5)

		for key_name in keys:
			var event = InputEventKey.new()
			event.keycode = _key_name_to_keycode(key_name)
			if event.keycode != KEY_NONE:
				InputMap.action_add_event(action_name, event)

		# Persist to ProjectSettings so it survives restart
		var events_array = InputMap.action_get_events(action_name)
		ProjectSettings.set_setting("input/" + action_name, {
			"deadzone": 0.5,
			"events": events_array,
		})
		added.append(action_name)

	ProjectSettings.save()
	return {"added": added}


func _key_name_to_keycode(key: String) -> Key:
	match key.to_lower():
		"space":  return KEY_SPACE
		"enter":  return KEY_ENTER
		"escape": return KEY_ESCAPE
		"up":     return KEY_UP
		"down":   return KEY_DOWN
		"left":   return KEY_LEFT
		"right":  return KEY_RIGHT
		"shift":  return KEY_SHIFT
		"ctrl":   return KEY_CTRL
		"a":      return KEY_A
		"b":      return KEY_B
		"c":      return KEY_C
		"d":      return KEY_D
		"e":      return KEY_E
		"f":      return KEY_F
		"g":      return KEY_G
		"h":      return KEY_H
		"i":      return KEY_I
		"j":      return KEY_J
		"k":      return KEY_K
		"l":      return KEY_L
		"m":      return KEY_M
		"n":      return KEY_N
		"o":      return KEY_O
		"p":      return KEY_P
		"q":      return KEY_Q
		"r":      return KEY_R
		"s":      return KEY_S
		"t":      return KEY_T
		"u":      return KEY_U
		"v":      return KEY_V
		"w":      return KEY_W
		"x":      return KEY_X
		"y":      return KEY_Y
		"z":      return KEY_Z
		"1":      return KEY_1
		"2":      return KEY_2
		"3":      return KEY_3
		"4":      return KEY_4
		"5":      return KEY_5
		_:        return KEY_NONE


# ─── UI ───────────────────────────────────────────────────────────────────────

func _add_chat_panel() -> void:
	var scene = load(get_script().resource_path.get_base_dir() + "/ui/chat_panel.tscn")
	if scene:
		chat_panel = scene.instantiate()
		add_control_to_dock(DOCK_SLOT_RIGHT_BL, chat_panel)


func _remove_chat_panel() -> void:
	if chat_panel:
		remove_control_from_docks(chat_panel)
		chat_panel.queue_free()
		chat_panel = null


# ─── Settings ─────────────────────────────────────────────────────────────────

func _get_setting(key: String, default: Variant) -> Variant:
	if ProjectSettings.has_setting(key):
		return ProjectSettings.get_setting(key)
	return default
