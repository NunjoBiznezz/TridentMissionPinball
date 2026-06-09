#!/usr/bin/env python3
"""
Convert pixel coordinates to normalized lamp_positions.json values.

Usage:
    python3 tools/px_to_norm.py <image_file> [--backbox]

Then type:  lamp_name  pixel_x  pixel_y
Example:    l_bonus_1  342 891

Type 'save' to write changes, 'quit' to exit without saving.
"""
import argparse, json, sys
from pathlib import Path
from PIL import Image

OUTPUT = Path(__file__).parent.parent / "gmc" / "assets" / "lamp_positions.json"

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("--backbox", action="store_true")
args = parser.parse_args()

if not Path(args.image).exists():
    print(__doc__); sys.exit(1)

location = "backbox" if args.backbox else "playfield"
w, h = Image.open(args.image).size
print(f"Image: {w} × {h} px  ({location})\n")

data = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {}

while True:
    try:
        line = input("lamp  px_x  px_y  (or 'save'/'quit'): ").strip()
    except EOFError:
        break
    if line in ("quit", "q"):
        break
    if line in ("save", "s"):
        OUTPUT.write_text(json.dumps(data, indent=2))
        print(f"Saved {len(data)} lamps → {OUTPUT}")
        continue
    parts = line.split()
    if len(parts) != 3:
        print("  need: lamp_name  x  y"); continue
    name, px, py = parts[0], int(parts[1]), int(parts[2])
    nx = round(px / w, 5)
    ny = round(py / h, 5)
    color = data.get(name, {}).get("color", "ffffff")
    data[name] = {"x": nx, "y": ny, "color": color, "image": location}
    print(f"  {name}: ({nx}, {ny})")

OUTPUT.write_text(json.dumps(data, indent=2))
print(f"Saved {len(data)} lamps → {OUTPUT}")
