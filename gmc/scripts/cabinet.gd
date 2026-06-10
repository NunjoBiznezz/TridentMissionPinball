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
var _attract_label: Label
var _attract_blink_timer: Timer
# Maps lamp name → {"style": StyleBoxFlat, "on_color": Color, "off_color": Color}
var _lamp_cells: Dictionary = {}
# Switch hit areas: Array of {name, nx, ny, radius, wrapper, style, latching}
var _switch_areas: Array = []
# Cabinet button hit areas: Array of {name, panel, style, label, off_color}
var _cabinet_buttons: Array = []
var _held_switch: String = ""
var _held_style: StyleBoxFlat = null
var _held_off_color: Color = Color(0, 0, 0, 0)
var _held_label: Label = null
# Latching switches (drop targets): stay active until MPF sends the inactive state
var _latched_switches: Dictionary = {}
# Quick-lookup for switch properties keyed by switch name
var _switch_area_map: Dictionary = {}

const POSITIONS_PATH    := "res://assets/lamp_positions.json"
const SWITCH_POSITIONS_PATH := "res://assets/switch_positions.json"
const LAMP_RADIUS       := 10
const LAMP_RADIUS_LARGE := 12
const SWITCH_RADIUS     := 14

func _find_asset_path(candidates: Array) -> String:
	for p in candidates:
		if FileAccess.file_exists(p):
			return p
	return ""

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
func _ready() -> void:
	MPF.server.listen()
	_build_ui()
	_init_assumed_switch_states()

	MPF.server.connect("status_changed", _on_status_changed)
	_on_status_changed(MPF.server.status)

	MPF.game.connect("player_update", _on_player_update)
	MPF.game.connect("machine_update", _on_machine_update)
	MPF.game.connect("game_started", _on_game_started)
	MPF.game.connect("player_added", _on_player_added)

	if MPF.server.has_signal("hardware_light_changed"):
		MPF.server.connect("hardware_light_changed", _on_light_changed)
		MPF.server.connect("hardware_switch_changed", _on_switch_changed)

	MPF.server.add_event_handler("start_attract_mode", _on_attract_start)
	MPF.server.add_event_handler("stop_attract_mode", _on_attract_stop)

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

	var _playfield_path := _find_asset_path(["res://assets/playfield.png",
		"res://assets/playfield.jpg", "res://assets/playfield.jpeg", "res://assets/playfield.webp"])
	var _backbox_path := _find_asset_path(["res://assets/backbox.png",
		"res://assets/backbox.jpg", "res://assets/backbox.jpeg", "res://assets/backbox.webp"])
	var _has_positions := FileAccess.file_exists(POSITIONS_PATH)

	if _has_positions and _playfield_path != "":
		if _backbox_path != "":
			# Side-by-side: playfield left, backbox right.
			# Displays are overlaid on the backbox; no separate header row.
			var hbox := HBoxContainer.new()
			hbox.size_flags_vertical = SIZE_EXPAND_FILL
			hbox.add_theme_constant_override("separation", 4)

			var pv := _build_image_view(_playfield_path, "playfield")
			pv.size_flags_stretch_ratio = 0.5
			hbox.add_child(pv)

			var bv := _build_image_view(_backbox_path, "backbox")
			bv.size_flags_stretch_ratio = 0.5
			hbox.add_child(bv)

			root_vbox.add_child(hbox)
		else:
			# No backbox: show traditional header row above playfield.
			root_vbox.add_child(_build_segment_row())
			root_vbox.add_child(_build_image_view(_playfield_path, "playfield"))
	else:
		root_vbox.add_child(_build_segment_row())
		root_vbox.add_child(_build_lamp_grid())

	if FileAccess.file_exists(SWITCH_POSITIONS_PATH):
		root_vbox.add_child(_build_cabinet_strip())

	_attract_label = Label.new()
	_attract_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_attract_label.add_theme_font_size_override("font_size", 20)
	_attract_label.add_theme_color_override("font_color", Color(1.0, 0.65, 0.0))
	_attract_label.visible = false
	root_vbox.add_child(_attract_label)

	_attract_blink_timer = Timer.new()
	_attract_blink_timer.wait_time = 0.6
	_attract_blink_timer.connect("timeout", _on_attract_blink)
	add_child(_attract_blink_timer)

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


func _build_image_view(image_path: String, location: String) -> Control:
	var wrapper := Control.new()
	wrapper.size_flags_vertical = SIZE_EXPAND_FILL
	wrapper.size_flags_horizontal = SIZE_EXPAND_FILL
	wrapper.clip_contents = true

	var img := Image.new()
	img.load(image_path)
	var tex := ImageTexture.create_from_image(img)
	var bg := TextureRect.new()
	bg.texture = tex
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	bg.set_anchors_preset(PRESET_FULL_RECT)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	wrapper.add_child(bg)

	var file := FileAccess.open(POSITIONS_PATH, FileAccess.READ)
	var positions: Dictionary = JSON.parse_string(file.get_as_text())
	file.close()

	for lamp_name in positions:
		var entry: Dictionary = positions[lamp_name]
		if entry.get("image", "playfield") != location:
			continue
		var r: int = entry.get("radius", LAMP_RADIUS)
		var hex: String = entry.get("color", "ffaa00")
		var on_color  := Color(hex.substr(0,2).hex_to_int()/255.0,
		                       hex.substr(2,2).hex_to_int()/255.0,
		                       hex.substr(4,2).hex_to_int()/255.0)
		var off_color := on_color * 0.12

		var style := StyleBoxFlat.new()
		style.bg_color = off_color
		style.corner_radius_top_left    = r
		style.corner_radius_top_right   = r
		style.corner_radius_bottom_left = r
		style.corner_radius_bottom_right = r
		style.border_width_left   = 1
		style.border_width_right  = 1
		style.border_width_top    = 1
		style.border_width_bottom = 1
		style.border_color = on_color * 0.35

		var bulb := Panel.new()
		bulb.add_theme_stylebox_override("panel", style)
		bulb.custom_minimum_size = Vector2(r * 2, r * 2)
		bulb.mouse_filter = Control.MOUSE_FILTER_IGNORE
		bulb.set_meta("nx", entry.get("x", 0.5))
		bulb.set_meta("ny", entry.get("y", 0.5))
		wrapper.add_child(bulb)

		_lamp_cells[lamp_name] = {"style": style, "on_color": on_color, "off_color": off_color}

	# Build switch hit areas for this image
	if FileAccess.file_exists(SWITCH_POSITIONS_PATH):
		var sf := FileAccess.open(SWITCH_POSITIONS_PATH, FileAccess.READ)
		var sw_data: Dictionary = JSON.parse_string(sf.get_as_text())
		sf.close()
		for sw_name in sw_data:
			var se: Dictionary = sw_data[sw_name]
			if se.get("image", "playfield") != location:
				continue
			var sr: int = se.get("radius", SWITCH_RADIUS)
			var sw_style := StyleBoxFlat.new()
			sw_style.bg_color            = Color(0, 0, 0, 0)
			sw_style.border_color        = Color(0.2, 0.8, 1.0, 0.65)
			sw_style.border_width_left   = 2
			sw_style.border_width_right  = 2
			sw_style.border_width_top    = 2
			sw_style.border_width_bottom = 2
			sw_style.corner_radius_top_left     = sr
			sw_style.corner_radius_top_right    = sr
			sw_style.corner_radius_bottom_left  = sr
			sw_style.corner_radius_bottom_right = sr
			var sw_panel := Panel.new()
			sw_panel.add_theme_stylebox_override("panel", sw_style)
			sw_panel.custom_minimum_size = Vector2(sr * 2, sr * 2)
			sw_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
			sw_panel.set_meta("nx", se.get("x", 0.5))
			sw_panel.set_meta("ny", se.get("y", 0.5))
			wrapper.add_child(sw_panel)
			var area_entry := {
				"name": sw_name, "nx": se.get("x", 0.5), "ny": se.get("y", 0.5),
				"radius": sr, "wrapper": wrapper, "style": sw_style,
				"img_size": tex.get_size(),
				"latching": se.get("latching", false),
				"ball_trap": se.get("ball_trap", false),
			}
			_switch_areas.append(area_entry)
			_switch_area_map[sw_name] = area_entry

	# Score / credits / ball display overlays (backbox only)
	if location == "backbox":
		_build_backbox_displays(wrapper)

	wrapper.connect("resized", func(): _reposition_lamps(wrapper, tex.get_size()))
	wrapper.call_deferred("emit_signal", "resized")
	return wrapper


func _build_backbox_displays(wrapper: Control) -> void:
	# Normalized positions on a 240×210 backbox image (pixel / image_dim).
	# Each entry: [key, nx, ny, initial_text, is_score, player_index]
	#   is_score=true → stored in _score_labels[player_index]
	#   is_score=false, key="credits" or "ball" → stored in _credits_label / _ball_label
	var displays := [
		["p1",      0.067, 0.142, "000000", true,  0],
		["p2",      0.725, 0.142, "------", true,  1],
		["p3",      0.067, 0.775, "------", true,  2],
		["p4",      0.725, 0.775, "------", true,  3],
		["credits",    0.104, 0.517, "-",      false, -1],
		["ball", 0.192, 0.517, "0",      false, -1],
	]

	_score_labels = []
	for _i in range(4):
		_score_labels.append(null)

	for d in displays:
		var lbl := Label.new()
		lbl.text = d[3]
		lbl.add_theme_font_size_override("font_size", 18)
		lbl.add_theme_color_override("font_color", Color(1.0, 0.65, 0.0))
		lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		lbl.set_meta("nx", float(d[1]))
		lbl.set_meta("ny", float(d[2]))
		lbl.set_meta("is_display", true)
		lbl.set_meta("base_font_size", 14.0)
		wrapper.add_child(lbl)

		if bool(d[4]):
			_score_labels[int(d[5])] = lbl
		elif d[0] == "credits":
			_credits_label = lbl
		else:
			_ball_label = lbl


func _reposition_lamps(wrapper: Control, img_size: Vector2) -> void:
	var ww := wrapper.size.x
	var wh := wrapper.size.y
	if ww == 0 or wh == 0:
		return

	# TextureRect KEEP_ASPECT_CENTERED: compute the actual drawn rect
	var iw := img_size.x
	var ih := img_size.y
	var scale := minf(ww / iw, wh / ih)
	var drawn_w := iw * scale
	var drawn_h := ih * scale
	var ox := (ww - drawn_w) * 0.5   # left offset of image inside wrapper
	var oy := (wh - drawn_h) * 0.5   # top offset

	for child in wrapper.get_children():
		if not child.has_meta("nx"):
			continue
		var nx: float = child.get_meta("nx")
		var ny: float = child.get_meta("ny")
		if child.has_meta("is_display"):
			# Display labels: top-left anchor, font scaled with image
			var font_size := int(child.get_meta("base_font_size") * scale)
			child.add_theme_font_size_override("font_size", max(font_size, 8))
			child.set_position(Vector2(ox + nx * drawn_w, oy + ny * drawn_h))
		elif child is Panel:
			# Lamp / switch circles: center anchor
			var r: float = child.custom_minimum_size.x * 0.5
			child.set_position(Vector2(
				ox + nx * drawn_w - r,
				oy + ny * drawn_h - r
			))


func _input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton):
		return
	var mbe := event as InputEventMouseButton
	if mbe.button_index != MOUSE_BUTTON_LEFT:
		return

	if mbe.pressed:
		# Cabinet strip buttons
		for btn in _cabinet_buttons:
			var panel: Panel = btn["panel"]
			if panel.get_global_rect().has_point(mbe.global_position):
				_held_switch    = btn["name"]
				_held_style     = btn["style"]
				_held_off_color = btn["off_color"]
				_held_label     = btn["label"]
				btn["style"].bg_color = Color(0.2, 0.8, 1.0, 0.5)
				btn["label"].add_theme_color_override("font_color", Color(1.0, 1.0, 1.0))
				MPF.server.send_switch(btn["name"], 1)
				return

		# Playfield / backbox switch circles
		for area in _switch_areas:
			var wrapper: Control = area["wrapper"]
			var img_size: Vector2 = area["img_size"]
			var wr := wrapper.get_global_rect()
			var lx := mbe.global_position.x - wr.position.x
			var ly := mbe.global_position.y - wr.position.y
			if lx < 0 or ly < 0 or lx > wr.size.x or ly > wr.size.y:
				continue
			var scale := minf(wr.size.x / img_size.x, wr.size.y / img_size.y)
			var drawn_w := img_size.x * scale
			var drawn_h := img_size.y * scale
			var ox := (wr.size.x - drawn_w) * 0.5
			var oy := (wr.size.y - drawn_h) * 0.5
			var ix := lx - ox
			var iy := ly - oy
			if ix < 0 or iy < 0 or ix > drawn_w or iy > drawn_h:
				continue
			var nx := ix / drawn_w
			var ny := iy / drawn_h
			var dpx := (nx - float(area["nx"])) * drawn_w
			var dpy := (ny - float(area["ny"])) * drawn_h
			if sqrt(dpx * dpx + dpy * dpy) <= float(area["radius"]):
				var sw_name: String = area["name"]
				if sw_name in _latched_switches:
					if area.get("ball_trap", false):
						# Ball is here — click to release without firing the solenoid
						MPF.server.send_switch(sw_name, 0)
						_latched_switches[sw_name].bg_color = Color(0, 0, 0, 0)
						_latched_switches.erase(sw_name)
					# Drop target while down: clicks are disabled
				else:
					MPF.server.send_switch(sw_name, 1)
					if area.get("latching", false) or area.get("ball_trap", false):
						area["style"].bg_color = Color(1.0, 0.15, 0.15, 0.7)
						_latched_switches[sw_name] = area["style"]
					else:
						area["style"].bg_color = Color(0.2, 0.8, 1.0, 0.5)
						_held_switch    = sw_name
						_held_style     = area["style"]
						_held_off_color = Color(0, 0, 0, 0)
						_held_label     = null
				break
	else:
		if _held_switch != "":
			MPF.server.send_switch(_held_switch, 0)
			if _held_style:
				_held_style.bg_color = _held_off_color
			if _held_label:
				_held_label.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
				_held_label = null
			_held_switch    = ""
			_held_style     = null
			_held_off_color = Color(0, 0, 0, 0)


func _build_cabinet_strip() -> Control:
	var outer := PanelContainer.new()
	outer.custom_minimum_size = Vector2(0, 52)

	var hbox := HBoxContainer.new()
	hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox.add_theme_constant_override("separation", 8)
	outer.add_child(hbox)

	var file := FileAccess.open(SWITCH_POSITIONS_PATH, FileAccess.READ)
	var sw_data: Dictionary = JSON.parse_string(file.get_as_text())
	file.close()

	for sw_name in sw_data:
		var se: Dictionary = sw_data[sw_name]
		if se.get("image", "playfield") != "cabinet":
			continue

		var label_text: String = sw_name.substr(2).replace("_", " ").to_upper()

		var sw_style := StyleBoxFlat.new()
		sw_style.bg_color            = Color(0.12, 0.12, 0.12)
		sw_style.border_color        = Color(0.2, 0.8, 1.0, 0.65)
		sw_style.border_width_left   = 2
		sw_style.border_width_right  = 2
		sw_style.border_width_top    = 2
		sw_style.border_width_bottom = 2
		sw_style.corner_radius_top_left     = 6
		sw_style.corner_radius_top_right    = 6
		sw_style.corner_radius_bottom_left  = 6
		sw_style.corner_radius_bottom_right = 6

		var btn := Panel.new()
		btn.add_theme_stylebox_override("panel", sw_style)
		btn.custom_minimum_size = Vector2(110, 36)

		var lbl := Label.new()
		lbl.text = label_text
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.vertical_alignment   = VERTICAL_ALIGNMENT_CENTER
		lbl.set_anchors_preset(PRESET_FULL_RECT)
		lbl.add_theme_font_size_override("font_size", 11)
		lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
		lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		btn.add_child(lbl)

		btn.mouse_filter = Control.MOUSE_FILTER_IGNORE
		hbox.add_child(btn)
		_cabinet_buttons.append({
			"name": sw_name, "panel": btn,
			"style": sw_style, "label": lbl,
			"off_color": Color(0.12, 0.12, 0.12)
		})

	return outer


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
		cell.custom_minimum_size = Vector2(100, 52)
		cell.alignment = BoxContainer.ALIGNMENT_CENTER

		var style := StyleBoxFlat.new()
		style.bg_color = off_color
		style.corner_radius_top_left    = 18
		style.corner_radius_top_right   = 18
		style.corner_radius_bottom_left = 18
		style.corner_radius_bottom_right = 18
		style.border_width_left   = 1
		style.border_width_right  = 1
		style.border_width_top    = 1
		style.border_width_bottom = 1
		style.border_color = on_color * 0.25

		var bulb := Panel.new()
		bulb.add_theme_stylebox_override("panel", style)
		bulb.custom_minimum_size = Vector2(36, 36)
		bulb.size_flags_horizontal = SIZE_SHRINK_CENTER
		cell.add_child(bulb)

		var lbl := Label.new()
		lbl.text = lamp_name.substr(2)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.add_theme_font_size_override("font_size", 7)
		lbl.add_theme_color_override("font_color", Color(0.38, 0.38, 0.38))
		lbl.clip_text = true
		lbl.custom_minimum_size = Vector2(100, 0)
		cell.add_child(lbl)

		grid.add_child(cell)
		_lamp_cells[lamp_name] = {"style": style, "on_color": on_color, "off_color": off_color}

	return wrapper

# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------
func _init_assumed_switch_states() -> void:
	var assumed := ["s_drop_target_1", "s_drop_target_2", "s_drop_target_3",
	                "s_drop_target_4", "s_drop_target_5", "s_outhole"]
	for sw_name in assumed:
		if sw_name in _switch_area_map and sw_name not in _latched_switches:
			var area = _switch_area_map[sw_name]
			area["style"].bg_color = Color(1.0, 0.15, 0.15, 0.7)
			_latched_switches[sw_name] = area["style"]


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
	if status == 3:
		call_deferred("_send_latched_switch_states")


func _send_latched_switch_states() -> void:
	for sw_name in _latched_switches:
		MPF.server.send_switch(sw_name, 1)


func _on_game_started() -> void:
	for lbl in _score_labels:
		if lbl:
			lbl.text = "000000"
			lbl.add_theme_color_override("font_color", Color(0.25, 0.18, 0.00))
	if _ball_label:
		_ball_label.text = "-"


func _on_player_added(_total: int) -> void:
	_refresh_scores()


func _on_player_update(var_name: String, value) -> void:
	match var_name:
		"score": _refresh_scores()
		"ball":
			if _ball_label:
				_ball_label.text = str(value)


func _on_machine_update(var_name: String, value) -> void:
	if var_name == "credits" and _credits_label:
		_credits_label.text = str(value)


func _on_light_changed(lamp_name: String, color: Color) -> void:
	if not lamp_name in _lamp_cells:
		return
	var cell = _lamp_cells[lamp_name]
	var is_on := color.r > 0.05 or color.g > 0.05 or color.b > 0.05
	cell["style"].bg_color = cell["on_color"] if is_on else cell["off_color"]


func _on_switch_changed(switch_name: String, state: bool) -> void:
	if state:
		if switch_name in _switch_area_map and switch_name not in _latched_switches:
			var area = _switch_area_map[switch_name]
			if area.get("latching", false) or area.get("ball_trap", false):
				area["style"].bg_color = Color(1.0, 0.15, 0.15, 0.7)
				_latched_switches[switch_name] = area["style"]
	else:
		if switch_name in _latched_switches:
			_latched_switches[switch_name].bg_color = Color(0, 0, 0, 0)
			_latched_switches.erase(switch_name)

func _on_attract_start(_payload = null) -> void:
	_attract_label.text = "GAME OVER"
	_attract_label.visible = true
	_attract_blink_timer.start()
	# Dim score labels during attract
	for lbl in _score_labels:
		lbl.add_theme_color_override("font_color", Color(0.15, 0.10, 0.00))

func _on_attract_stop(_payload = null) -> void:
	_attract_label.visible = false
	_attract_blink_timer.stop()

func _on_attract_blink() -> void:
	var credits = MPF.game.machine_vars.get("credits", 0)
	if int(credits) > 0:
		_attract_label.text = "PRESS START" if _attract_label.text != "PRESS START" else "GAME OVER"
	else:
		_attract_label.text = "INSERT COIN" if _attract_label.text != "INSERT COIN" else "GAME OVER"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
func _refresh_scores() -> void:
	var current = MPF.game.player.get("number", 1) - 1
	for i in range(_score_labels.size()):
		var lbl: Label = _score_labels[i]
		if not lbl:
			continue
		if i < MPF.game.players.size():
			var score = MPF.game.players[i].get("score", 0)
			lbl.text = "%06d" % int(score)
			var active = i == current
			lbl.add_theme_color_override(
				"font_color",
				Color(1.00, 0.65, 0.00) if active else Color(0.35, 0.25, 0.00)
			)
		else:
			lbl.text = "------"
			lbl.add_theme_color_override("font_color", Color(0.15, 0.10, 0.00))
