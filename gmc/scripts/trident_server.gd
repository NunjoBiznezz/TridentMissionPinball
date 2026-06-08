extends GMCServer

## Custom BCP server for the Trident virtual cabinet.
## Subscribes to light and switch monitor categories so the
## cabinet UI can reflect real-time hardware state.

signal hardware_light_changed(light_name: String, color: Color)
signal hardware_switch_changed(switch_name: String, state: bool)

func on_connect() -> void:
	_send("monitor_start?category=lights")
	_send("monitor_start?category=switches")

func on_message(message: Dictionary):
	if message.cmd == "monitor_device_attribute_changed":
		_handle_hardware_change(message)
		return null
	return message

func _handle_hardware_change(msg: Dictionary) -> void:
	match msg.get("category", ""):
		"lights":
			if msg.get("attribute") == "color":
				hardware_light_changed.emit(
					msg.get("key", ""),
					_parse_mpf_color(msg.get("value"))
				)
		"switches":
			if msg.get("attribute") == "state":
				var v = msg.get("value", 0)
				hardware_switch_changed.emit(
					msg.get("key", ""),
					v == 1 or v == "1" or v == true
				)

# MPF sends colors as 6-char hex strings ("ff0000") or sometimes
# as a list. Handle both defensively.
func _parse_mpf_color(v) -> Color:
	if typeof(v) == TYPE_STRING:
		var s: String = v.strip_edges().lstrip("#")
		if s.length() >= 6:
			return Color(
				s.substr(0, 2).hex_to_int() / 255.0,
				s.substr(2, 2).hex_to_int() / 255.0,
				s.substr(4, 2).hex_to_int() / 255.0
			)
	elif typeof(v) == TYPE_ARRAY and v.size() >= 3:
		return Color(v[0] / 255.0, v[1] / 255.0, v[2] / 255.0)
	return Color.BLACK
