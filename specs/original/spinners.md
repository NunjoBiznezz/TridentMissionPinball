# Spec: Spinners & Color Bonuses

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` pp. 5–6 (Spinner Feature, Stationary Targets).
Tests: `tests/test_spinners.py`

## Overview

Two spinners (left and right) score a base value per spin, optionally
augmented by color bonuses from standup targets and a moveable purple
bonus. All values reset on `ball_drain`.

## Base values

| Variable              | Initial value | Resets on  |
|-----------------------|---------------|------------|
| `left_spinner_value`  | 200           | ball_drain |
| `right_spinner_value` | 200           | ball_drain |
| `purple_bonus`        | 0             | ball_drain |
| `purple_on_left`      | 1             | ball_drain |

Score per spin = `spinner_value + (purple_bonus if side matches else 0)`.

## Color bonuses from standup targets

Each colored standup target advances one spinner's base value on its
**first hit per ball only** (enforced by `*_applied` player vars that
are cleared on `ball_drain`):

| Target  | Effect                             |
|---------|------------------------------------|
| White   | `left_spinner_value` +400          |
| Amber   | `left_spinner_value` +400          |
| Green   | `right_spinner_value` +400         |
| Yellow  | `right_spinner_value` +400         |
| Purple  | `purple_bonus` = 1,000; `purple_on_left` = 1 |

Both left targets (white + amber) can each add 400, bringing the left
spinner from 200 → 600 → 1,000. Likewise for the right.
A second hit of the same target does nothing to the spinner value.

## Purple bonus

The purple standup target creates a 1,000-point bonus that adds to
whichever spinner it is currently assigned to (`purple_on_left`
controls the side). The purple bonus starts on the left spinner.

**Upper slings flip the purple assignment** when `purple_bonus > 0`:
- `s_ul_sling` or `s_ur_sling` → if `purple_on_left == 1`, set to 0
  (move to right); if `purple_on_left == 0`, set to 1 (move to left).
- **When `purple_bonus == 0`, slings have no effect on `purple_on_left`.**

The lower slings, 10-point switch, and lower lane switches also trigger
the purple swap (via the same `purple_to_left` / `purple_to_right`
event dispatch in `event_player`), but only when `purple_bonus > 0`.

## Example: full setup

After hitting all 5 standup targets once:
- Left spinner: 200 + 400 (white) + 400 (amber) = **1,000**
- Right spinner: 200 + 400 (green) + 400 (yellow) = **1,000**
- Purple bonus: **1,000**, on left

Spinning left scores 1,000 + 1,000 = **2,000**.
Spinning right scores 1,000 + 0 = **1,000**.
After one upper sling hit: purple moves right.
Spinning left scores 1,000 + 0 = **1,000**.
Spinning right scores 1,000 + 1,000 = **2,000**.
