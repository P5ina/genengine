@tool
extends Control

const AGENT_PORT = 7821

var stream: StreamPeerTCP
var connected: bool = false

@onready var output: RichTextLabel = $VBox/Output
@onready var input: LineEdit = $VBox/HBox/Input
@onready var send_btn: Button = $VBox/HBox/SendBtn
@onready var status_label: Label = $VBox/Status


func _ready() -> void:
	send_btn.pressed.connect(_on_send)
	input.text_submitted.connect(func(_t): _on_send())
	_connect_to_agent()


func _connect_to_agent() -> void:
	stream = StreamPeerTCP.new()
	var err = stream.connect_to_host("127.0.0.1", AGENT_PORT)
	if err == OK:
		status_label.text = "● Connected"
		status_label.modulate = Color.GREEN
		connected = true
	else:
		status_label.text = "● Connecting..."
		status_label.modulate = Color.YELLOW


func _process(_delta: float) -> void:
	if not connected:
		return

	var available = stream.get_available_bytes()
	if available > 0:
		var data = stream.get_utf8_string(available)
		_handle_response(data)


func _handle_response(raw: String) -> void:
	for line in raw.split("\n", false):
		var json = JSON.new()
		if json.parse(line) != OK:
			continue
		var msg = json.get_data()
		match msg.get("type", ""):
			"text":
				output.append_text(msg.get("text", ""))
			"tool_call":
				output.append_text("\n[i]→ %s[/i]\n" % msg.get("name", ""))
			"done":
				output.append_text("\n")


func _on_send() -> void:
	var text = input.text.strip_edges()
	if text.is_empty() or not connected:
		return

	output.append_text("\n[b]You:[/b] %s\n[b]Agent:[/b] " % text)

	var payload = JSON.stringify({"text": text}) + "\n"
	stream.put_utf8_string(payload)

	input.text = ""
