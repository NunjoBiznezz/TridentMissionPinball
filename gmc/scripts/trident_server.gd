extends GMCServer

signal hardware_light_changed(light_name: String, color: Color)
signal hardware_switch_changed(switch_name: String, state: bool)
signal hardware_drop_target_changed(target_name: String, complete: bool)

func on_connect() -> void:
	# "devices" is the correct MPF category for light + all device state changes.
	# "switches" gives us dedicated switch messages on every state transition.
	_send("monitor_start?category=devices")
	_send("monitor_start?category=switches")
	# Re-register every event handler added via add_event_handler(). Those
	# calls happen in _ready(), before MPF has connected, and _send() drops
	# messages when there is no client — so the registrations must be
	# replayed on every (re)connect or MPF never sends the triggers.
	for event in registered_handlers:
		print("[trident_server] registering MPF trigger '%s'" % event)
		_send("register_trigger?event=%s" % event)

func stop(is_exiting: bool = false) -> void:
	super.stop(true)
	if not is_exiting:
		call_deferred("listen")

# Guard against the double-listen bug: when MPF sends "goodbye" and then the
# socket also closes, two deferred stop() calls are queued. The second listen()
# would fail with "port in use", then call set_process(false) and break
# reconnection. Bail out early if the server is already listening.
func listen() -> void:
	if _server.is_listening():
		return
	super.listen()

# Return null to swallow the message (prevent the base-class match from
# logging a spurious "No handler" warning).
func on_message(message: Dictionary):
	match message.get("cmd", ""):
		"device":
			match message.get("type", ""):
				"light":
					var st = message.get("state", {})
					var raw = st.get("color", null) if typeof(st) == TYPE_DICTIONARY else null
					if raw != null:
						hardware_light_changed.emit.call_deferred(
							message.get("name", ""),
							_rgb_to_color(raw)
						)
				"drop_target":
					var dst = message.get("state", {})
					var complete = bool(dst.get("complete", false)) if typeof(dst) == TYPE_DICTIONARY else false
					hardware_drop_target_changed.emit.call_deferred(
						message.get("name", ""),
						complete
					)
			return null
		"switch":
			var v = message.get("state", 0)
			hardware_switch_changed.emit.call_deferred(
				message.get("name", ""),
				int(v) == 1
			)
			return null
	return message


func _rgb_to_color(v) -> Color:
	if typeof(v) == TYPE_ARRAY and v.size() >= 3:
		return Color(v[0] / 255.0, v[1] / 255.0, v[2] / 255.0)
	if typeof(v) == TYPE_STRING:
		var s: String = v.strip_edges().lstrip("#")
		if s.length() >= 6:
			return Color(
				s.substr(0, 2).hex_to_int() / 255.0,
				s.substr(2, 2).hex_to_int() / 255.0,
				s.substr(4, 2).hex_to_int() / 255.0
			)
	return Color.BLACK
