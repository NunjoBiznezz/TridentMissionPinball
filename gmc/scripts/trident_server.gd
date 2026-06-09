extends GMCServer

signal hardware_light_changed(light_name: String, color: Color)
signal hardware_switch_changed(switch_name: String, state: bool)

func on_connect() -> void:
	# "devices" is the correct MPF category for light + all device state changes.
	# "switches" gives us dedicated switch messages on every state transition.
	_send("monitor_start?category=devices")
	_send("monitor_start?category=switches")
	_send("register_trigger?event=start_attract_mode")
	_send("register_trigger?event=stop_attract_mode")

func stop(is_exiting: bool = false) -> void:
	super.stop(true)
	if not is_exiting:
		call_deferred("listen")

# Return null to swallow the message (prevent the base-class match from
# logging a spurious "No handler" warning).
func on_message(message: Dictionary):
	match message.get("cmd", ""):
		"device":
			if message.get("type", "") == "light":
				var st = message.get("state", {})
				var raw = st.get("color", null) if typeof(st) == TYPE_DICTIONARY else null
				if raw != null:
					hardware_light_changed.emit.call_deferred(
						message.get("name", ""),
						_rgb_to_color(raw)
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

func force_switch(switch_name: String, active: bool) -> void:
	var msg := "switch?name=%s&state=%d" % [switch_name, 1 if active else 0]
	print("[TridentServer] force_switch sending: ", msg)
	_send(msg)

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
