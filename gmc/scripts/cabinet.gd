extends Control

# ---------------------------------------------------------------------------
# Lamp definitions: [mpf_name, color_when_on]
# Colors approximate the physical lamp colors on the Stern Trident.
# ---------------------------------------------------------------------------
const LAMPS: Array = [
	["l_bonus_1",            Color(1.00, 0.67, 0.00)],  # amber
	["l_bonus_2",            Color(1.00, 0.67, 0.00)],
	["l_bonus_3",            Color(1.00, 0.67, 0.00)],
	["l_bonus_4",            Color(1.00, 0.67, 0.00)],
	["l_bonus_5",            Color(1.00, 0.67, 0.00)],
	["l_bonus_6",            Color(1.00, 0.67, 0.00)],
	["l_bonus_7",            Color(1.00, 0.67, 0.00)],
	["l_bonus_8",            Color(1.00, 0.67, 0.00)],
	["l_bonus_9",            Color(1.00, 0.67, 0.00)],
	["l_bonus_10",           Color(1.00, 0.67, 0.00)],
	["l_drop_target_5",      Color(1.00, 0.40, 0.00)],  # orange
	["l_standup_special",    Color(1.00, 1.00, 1.00)],  # white
	["l_left_spinner_amber", Color(1.00, 0.67, 0.00)],
	["l_left_spinner_white", Color(1.00, 1.00, 1.00)],
	["l_standup_amber",      Color(1.00, 0.67, 0.00)],
	["l_standup_white",      Color(1.00, 1.00, 1.00)],
	["l_right_spinner_yellow",Color(1.00, 1.00, 0.00)],  # yellow
	["l_right_spinner_green", Color(0.00, 1.00, 0.20)],  # green
	["l_standup_yellow",     Color(1.00, 1.00, 0.00)],
	["l_standup_green",      Color(0.00, 1.00, 0.20)],
	["l_drop_target_4",      Color(1.00, 0.40, 0.00)],
	["l_drop_target_3",      Color(1.00, 0.40, 0.00)],
	["l_drop_target_2",      Color(1.00, 0.40, 0.00)],
	["l_drop_target_1",      Color(1.00, 0.40, 0.00)],
	["l_top_eject_30k",      Color(1.00, 1.00, 1.00)],
	["l_top_eject_20k",      Color(1.00, 1.00, 1.00)],
	["l_top_eject_10k",      Color(1.00, 1.00, 1.00)],
	["l_top_eject_5k",       Color(1.00, 1.00, 1.00)],
	["l_bonus_5x_feature",   Color(0.00, 1.00, 1.00)],  # cyan
	["l_bonus_4x_feature",   Color(0.00, 1.00, 1.00)],
	["l_bonus_3x_feature",   Color(0.00, 1.00, 1.00)],
	["l_bonus_2x_feature",   Color(0.00, 1.00, 1.00)],
	["l_bonus_5x",           Color(0.00, 1.00, 1.00)],
	["l_bonus_4x",           Color(0.00, 1.00, 1.00)],
	["l_bonus_3x",           Color(0.00, 1.00, 1.00)],
	["l_bonus_2x",           Color(0.00, 1.00, 1.00)],
	["l_left_lane_8k",       Color(0.00, 1.00, 0.20)],
	["l_left_lane_6k",       Color(0.00, 1.00, 0.20)],
	["l_left_lane_4k",       Color(0.00, 1.00, 0.20)],
	["l_left_lane_2k",       Color(0.00, 1.00, 0.20)],
	["l_shoot_again",        Color(1.00, 1.00, 1.00)],
	["l_match",              Color(1.00, 1.00, 1.00)],
	["l_standup_purple",     Color(0.60, 0.00, 1.00)],  # purple
	["l_drop_target_special",Color(1.00, 0.40, 0.00)],
	["l_right_spinner_purple",Color(0.60, 0.00, 1.00)],
	["l_right_outlane_special",Color(1.00, 0.10, 0.10)],  # red
	["l_left_spinner_purple",Color(0.60, 0.00, 1.00)],
	["l_extra_ball",         Color(1.00, 0.10, 0.10)],
	["l_ball_in_play",       Color(1.00, 1.00, 1.00)],
	["l_high_score_to_date", Color(1.00, 1.00, 0.00)],
	["l_game_over",          Color(1.00, 0.10, 0.10)],
	["l_tilt",               Color(1.00, 0.10, 0.10)],
	["l_player_1",           Color(1.00, 1.00, 1.00)],
	["l_player_2",           Color(1.00, 1.00, 1.00)],
	["l_player_3",           Color(1.00, 1.00, 1.00)],
	["l_player_4",           Color(1.00, 1.00, 1.00)],
	["l_player_1_up",        Color(1.00, 1.00, 1.00)],
	["l_player_2_up",        Color(1.00, 1.00, 1.00)],
	["l_player_3_up",        Color(1.00, 1.00, 1.00)],
	["l_player_4_up",        Color(1.00, 1.00, 1.00)],
]

# ---------------------------------------------------------------------------
# Runtime state
# ---------------------------------------------------------------------------
var _score_labels: Array = []
var _ball_label: Label
var _credits_label: Label
var _status_label: Label
# Maps lamp name → {"rect": ColorRect, "on_color": Color}
var _lamp_cells: Dictionary = {}

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
func _ready() -> void:
	MPF.server.listen()
	_build_ui()

	MPF.server.connect("status_changed", _on_status_changed)
	_on_status_changed(MPF.server.status)

	MPF.game.connect("player_update", _on_player_update)
	MPF.game.connect("machine_update", _on_machine_update)
	MPF.game.connect("game_started", _on_game_started)
	MPF.game.connect("player_added", _on_player_added)

	if MPF.server.has_signal("hardware_light_changed"):
		MPF.server.connect("hardware_light_changed", _on_light_changed)
		MPF.server.connect("hardware_switch_changed", _on_switch_changed)

# ---------------------------------------------------------------------------
# UI construction
# ---------------------------------------------------------------------------
func _build_ui() -> void:
	var bg = ColorRect.new()
	bg.color = Color(0.06, 0.06, 0.06)
	bg.set_anchors_preset(PRESET_FULL_RECT)
	add_child(bg)

	var root_vbox = VBoxContainer.new()
	root_vbox.set_anchors_preset(PRESET_FULL_RECT)
	root_vbox.add_theme_constant_override("separation", 6)
	add_child(root_vbox)

	root_vbox.add_child(_build_segment_row())
	root_vbox.add_child(_build_lamp_grid())

	_status_label = Label.new()
	_status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_status_label.add_theme_font_size_override("font_size", 11)
	_status_label.add_theme_color_override("font_color", Color(0.35, 0.35, 0.35))
	root_vbox.add_child(_status_label)


func _build_segment_row() -> Control:
	var outer = PanelContainer.new()
	outer.custom_minimum_size = Vector2(0, 100)

	var hbox = HBoxContainer.new()
	hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox.add_theme_constant_override("separation", 16)
	outer.add_child(hbox)

	_score_labels = []
	for i in range(4):
		var col = _make_segment_col("P%d" % (i + 1), "000000")
		hbox.add_child(col["container"])
		_score_labels.append(col["value"])

	hbox.add_child(VSeparator.new())

	var ball_col = _make_segment_col("BALL", "-")
	hbox.add_child(ball_col["container"])
	_ball_label = ball_col["value"]

	var cred_col = _make_segment_col("CRED", "0")
	hbox.add_child(cred_col["container"])
	_credits_label = cred_col["value"]

	return outer


func _make_segment_col(header: String, initial: String) -> Dictionary:
	var col = VBoxContainer.new()
	col.alignment = BoxContainer.ALIGNMENT_CENTER

	var hdr = Label.new()
	hdr.text = header
	hdr.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hdr.add_theme_font_size_override("font_size", 11)
	hdr.add_theme_color_override("font_color", Color(0.35, 0.35, 0.35))
	col.add_child(hdr)

	var val = Label.new()
	val.text = initial
	val.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	val.add_theme_font_size_override("font_size", 38)
	val.add_theme_color_override("font_color", Color(0.25, 0.18, 0.00))  # dim = inactive
	col.add_child(val)

	return {"container": col, "value": val}


func _build_lamp_grid() -> Control:
	var wrapper = Control.new()
	wrapper.size_flags_vertical = SIZE_EXPAND_FILL

	var grid = GridContainer.new()
	grid.columns = 10
	grid.add_theme_constant_override("h_separation", 3)
	grid.add_theme_constant_override("v_separation", 3)
	grid.set_anchors_preset(PRESET_FULL_RECT)
	wrapper.add_child(grid)

	for lamp in LAMPS:
		var lamp_name: String = lamp[0]
		var on_color: Color = lamp[1]
		var off_color: Color = on_color * 0.12

		var cell = VBoxContainer.new()
		cell.custom_minimum_size = Vector2(118, 48)

		var rect = ColorRect.new()
		rect.color = off_color
		rect.custom_minimum_size = Vector2(118, 32)
		cell.add_child(rect)

		var lbl = Label.new()
		# Strip the "l_" prefix for compactness
		lbl.text = lamp_name.substr(2)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.add_theme_font_size_override("font_size", 8)
		lbl.add_theme_color_override("font_color", Color(0.38, 0.38, 0.38))
		lbl.clip_text = true
		lbl.custom_minimum_size = Vector2(118, 0)
		cell.add_child(lbl)

		grid.add_child(cell)
		_lamp_cells[lamp_name] = {"rect": rect, "on_color": on_color, "off_color": off_color}

	return wrapper

# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------
func _on_status_changed(status) -> void:
	var msgs = {
		0: "Idle",
		1: "Listening on port 5050 — start MPF to connect",
		2: "Launching MPF...",
		3: "MPF Connected",
		4: "Connection Error",
	}
	if _status_label:
		_status_label.text = msgs.get(status, "")


func _on_game_started() -> void:
	for lbl in _score_labels:
		lbl.text = "000000"
		lbl.add_theme_color_override("font_color", Color(0.25, 0.18, 0.00))
	_ball_label.text = "-"


func _on_player_added(_total: int) -> void:
	_refresh_scores()


func _on_player_update(var_name: String, value) -> void:
	match var_name:
		"score": _refresh_scores()
		"ball":  _ball_label.text = str(value)


func _on_machine_update(var_name: String, value) -> void:
	if var_name == "credits":
		_credits_label.text = str(value)


func _on_light_changed(lamp_name: String, color: Color) -> void:
	if not lamp_name in _lamp_cells:
		return
	var cell = _lamp_cells[lamp_name]
	var is_on := color.r > 0.05 or color.g > 0.05 or color.b > 0.05
	cell["rect"].color = color if is_on else cell["off_color"]


func _on_switch_changed(_switch_name: String, _state: bool) -> void:
	pass  # Switch panel not yet implemented

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
func _refresh_scores() -> void:
	var current = MPF.game.player.get("number", 1) - 1
	for i in range(_score_labels.size()):
		if i < MPF.game.players.size():
			var score = MPF.game.players[i].get("score", 0)
			_score_labels[i].text = "%06d" % int(score)
			var active = i == current
			_score_labels[i].add_theme_color_override(
				"font_color",
				Color(1.00, 0.65, 0.00) if active else Color(0.35, 0.25, 0.00)
			)
		else:
			_score_labels[i].text = "------"
			_score_labels[i].add_theme_color_override("font_color", Color(0.15, 0.10, 0.00))
