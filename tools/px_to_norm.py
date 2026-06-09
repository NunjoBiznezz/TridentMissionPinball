#!/usr/bin/env python3
"""
Convert pixel coordinates to normalized position JSON values.

Usage:
    python3 tools/px_to_norm.py <image_file>              # lamp positions (playfield)
    python3 tools/px_to_norm.py <image_file> --backbox    # lamp positions (backbox)
    python3 tools/px_to_norm.py <image_file> --switches   # switch positions (playfield)
    python3 tools/px_to_norm.py <image_file> --switches --backbox  # switch positions (backbox)

Then type:  name  pixel_x  pixel_y
Example:    l_bonus_1  342 891
            s_left_flipper  210 1740

Type 'save' to write changes, 'quit' to exit without saving.
"""
import argparse, json, sys
from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).parent.parent / "gmc" / "assets"

parser = argparse.ArgumentParser()
parser.add_argument("image")
parser.add_argument("--backbox", action="store_true", help="Use backbox image location")
parser.add_argument("--switches", action="store_true", help="Write to switch_positions.json")
args = parser.parse_args()

if not Path(args.image).exists():
    print(__doc__); sys.exit(1)

location = "backbox" if args.backbox else "playfield"
output   = ASSETS / ("switch_positions.json" if args.switches else "lamp_positions.json")
kind     = "switch" if args.switches else "lamp"

w, h = Image.open(args.image).size
print(f"Image: {w} × {h} px  |  {kind} positions  |  location: {location}")
print(f"Output: {output}\n")

data = json.loads(output.read_text()) if output.exists() else {}

while True:
    try:
        line = input(f"{kind}  px_x  px_y  (or 'save'/'quit'): ").strip()
    except EOFError:
        break
    if line in ("quit", "q"):
        break
    if line in ("save", "s"):
        output.write_text(json.dumps(data, indent=2))
        print(f"Saved {len(data)} entries → {output}")
        continue
    parts = line.split()
    if len(parts) != 3:
        print(f"  need: {kind}_name  x  y"); continue
    name, px, py = parts[0], int(parts[1]), int(parts[2])
    nx = round(px / w, 5)
    ny = round(py / h, 5)
    existing = data.get(name, {})
    if args.switches:
        data[name] = {"x": nx, "y": ny,
                      "radius": existing.get("radius", 14),
                      "image": location}
    else:
        data[name] = {"x": nx, "y": ny,
                      "color": existing.get("color", "ffffff"),
                      "image": location}
    print(f"  {name}: ({nx}, {ny})")

output.write_text(json.dumps(data, indent=2))
print(f"Saved {len(data)} entries → {output}")
