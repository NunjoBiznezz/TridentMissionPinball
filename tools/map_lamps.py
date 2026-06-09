#!/usr/bin/env python3
"""
map_lamps.py  —  Click each lamp on the playfield photo to record its
                 position and sample its natural color.

Usage:
    python3 tools/map_lamps.py <path/to/playfield.jpg>

Output:
    gmc/assets/lamp_positions.json   (normalized x/y 0-1, hex color)

Controls:
    Left-click   — place current lamp
    Backspace    — undo last placement
    S / Skip     — skip current lamp (leaves it unmapped)
    Q / Save     — save and quit
"""

import json
import sys
import os
from pathlib import Path

try:
    import tkinter as tk
    from PIL import Image, ImageTk
except ImportError:
    print("Install Pillow:  pip install Pillow")
    sys.exit(1)

# ── Lamp names in the order you will click them ──────────────────────────────
LAMPS = [
    "l_bonus_1",             "l_bonus_2",             "l_bonus_3",
    "l_bonus_4",             "l_bonus_5",             "l_bonus_6",
    "l_bonus_7",             "l_bonus_8",             "l_bonus_9",
    "l_bonus_10",
    "l_drop_target_5",       "l_standup_special",
    "l_left_spinner_amber",  "l_left_spinner_white",
    "l_standup_amber",       "l_standup_white",
    "l_right_spinner_yellow","l_right_spinner_green",
    "l_standup_yellow",      "l_standup_green",
    "l_drop_target_4",       "l_drop_target_3",
    "l_drop_target_2",       "l_drop_target_1",
    "l_top_eject_30k",       "l_top_eject_20k",
    "l_top_eject_10k",       "l_top_eject_5k",
    "l_bonus_5x_feature",    "l_bonus_4x_feature",
    "l_bonus_3x_feature",    "l_bonus_2x_feature",
    "l_bonus_5x",            "l_bonus_4x",
    "l_bonus_3x",            "l_bonus_2x",
    "l_left_lane_8k",        "l_left_lane_6k",
    "l_left_lane_4k",        "l_left_lane_2k",
    "l_shoot_again",         "l_match",
    "l_standup_purple",      "l_drop_target_special",
    "l_right_spinner_purple","l_right_outlane_special",
    "l_left_spinner_purple", "l_extra_ball",
    "l_ball_in_play",        "l_high_score_to_date",
    "l_game_over",           "l_tilt",
    "l_player_1",            "l_player_2",
    "l_player_3",            "l_player_4",
    "l_player_1_up",         "l_player_2_up",
    "l_player_3_up",         "l_player_4_up",
]

OUTPUT_PATH = Path(__file__).parent.parent / "gmc" / "assets" / "lamp_positions.json"
SAMPLE_RADIUS = 6   # pixels around click point to average for color
DOT_RADIUS    = 7   # display dot size on canvas


class LampMapper:
    def __init__(self, image_path: str):
        self.orig = Image.open(image_path).convert("RGB")
        self.iw, self.ih = self.orig.size

        # Load any existing progress
        self.data: dict = {}
        if OUTPUT_PATH.exists():
            with open(OUTPUT_PATH) as f:
                self.data = json.load(f)

        # Resume after already-mapped lamps
        self.idx = 0
        while self.idx < len(LAMPS) and LAMPS[self.idx] in self.data:
            self.idx += 1

        self._build_ui()
        self._scale_image()
        self._refresh()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.root = tk.Tk()
        self.root.title("Trident Lamp Mapper")
        self.root.configure(bg="#111")

        # Scale image to 90 % of screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        scale = min(sw * 0.90 / self.iw, sh * 0.85 / self.ih, 1.0)
        self.dw = int(self.iw * scale)
        self.dh = int(self.ih * scale)
        self.scale = scale

        # Header
        hdr = tk.Frame(self.root, bg="#111")
        hdr.pack(fill=tk.X, padx=6, pady=4)

        self.v_lamp     = tk.StringVar()
        self.v_progress = tk.StringVar()
        tk.Label(hdr, textvariable=self.v_lamp, bg="#111", fg="#ffcc00",
                 font=("monospace", 13, "bold")).pack(side=tk.LEFT)
        tk.Label(hdr, textvariable=self.v_progress, bg="#111", fg="#666",
                 font=("monospace", 11)).pack(side=tk.RIGHT)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.dw, height=self.dh,
                                bg="#000", cursor="crosshair",
                                highlightthickness=0)
        self.canvas.pack(padx=6, pady=2)
        self.canvas.bind("<Button-1>", self._click)

        # Footer
        ftr = tk.Frame(self.root, bg="#111")
        ftr.pack(fill=tk.X, padx=6, pady=4)
        btn = lambda t, cmd, c="#333": tk.Button(
            ftr, text=t, command=cmd, bg=c, fg="white",
            relief=tk.FLAT, padx=10, pady=4)
        btn("← Undo (Backspace)", self._undo).pack(side=tk.LEFT, padx=4)
        btn("Skip →",             self._skip).pack(side=tk.LEFT, padx=4)
        btn("Save & Quit",        self._save_quit, "#1a7a3a").pack(side=tk.RIGHT, padx=4)

        self.root.bind("<BackSpace>", lambda e: self._undo())
        self.root.bind("<s>",         lambda e: self._save_quit())
        self.root.bind("<q>",         lambda e: self._save_quit())

    # ── Image helpers ─────────────────────────────────────────────────────────

    def _scale_image(self):
        scaled = self.orig.resize((self.dw, self.dh), Image.LANCZOS)
        # Slightly darken so dots pop
        from PIL import ImageEnhance
        scaled = ImageEnhance.Brightness(scaled).enhance(0.75)
        self.tk_img = ImageTk.PhotoImage(scaled)

    def _sample_color(self, img_x: int, img_y: int) -> str:
        x0 = max(0, img_x - SAMPLE_RADIUS)
        y0 = max(0, img_y - SAMPLE_RADIUS)
        x1 = min(self.iw, img_x + SAMPLE_RADIUS + 1)
        y1 = min(self.ih, img_y + SAMPLE_RADIUS + 1)
        region = self.orig.crop((x0, y0, x1, y1))
        pixels = list(region.getdata())
        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)
        # Boost saturation so dim insert colors read as vivid on-colors
        import colorsys
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        s = min(1.0, s * 2.5)
        v = min(1.0, v * 1.6)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
        return f"{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}"

    # ── Event handlers ────────────────────────────────────────────────────────

    def _click(self, event):
        if self.idx >= len(LAMPS):
            return
        img_x = int(event.x / self.scale)
        img_y = int(event.y / self.scale)
        lamp  = LAMPS[self.idx]
        color = self._sample_color(img_x, img_y)
        self.data[lamp] = {
            "x":     round(event.x / self.dw, 5),
            "y":     round(event.y / self.dh, 5),
            "color": color,
        }
        self.idx += 1
        self._autosave()
        self._refresh()

    def _undo(self):
        if self.idx == 0:
            return
        self.idx -= 1
        self.data.pop(LAMPS[self.idx], None)
        self._autosave()
        self._refresh()

    def _skip(self):
        if self.idx < len(LAMPS):
            self.idx += 1
            self._refresh()

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _refresh(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

        for i, lamp in enumerate(LAMPS):
            if lamp not in self.data:
                continue
            d   = self.data[lamp]
            cx  = d["x"] * self.dw
            cy  = d["y"] * self.dh
            col = "#" + d["color"]
            r   = DOT_RADIUS
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                    fill=col, outline="white", width=1)
            self.canvas.create_text(cx, cy - r - 6, text=str(i+1),
                                    fill="white", font=("monospace", 7))

        if self.idx < len(LAMPS):
            self.v_lamp.set(f"▶  {LAMPS[self.idx]}")
            self.v_progress.set(f"{self.idx + 1} / {len(LAMPS)}")
        else:
            self.v_lamp.set("✓  All lamps mapped — Save & Quit")
            self.v_progress.set(f"{len(LAMPS)} / {len(LAMPS)}")

    # ── Persistence ───────────────────────────────────────────────────────────

    def _autosave(self):
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(self.data, f, indent=2)

    def _save_quit(self):
        self._autosave()
        print(f"Saved {len(self.data)} lamps → {OUTPUT_PATH}")
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    img = sys.argv[1]
    if not Path(img).exists():
        print(f"File not found: {img}")
        sys.exit(1)
    LampMapper(img).run()
