# Spec: Top Eject Pocket (Saucer)

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` p. 5 (Top Eject Pockets).
Tests: `tests/test_saucer.py`

## Scoring

The saucer (`s_saucer`) scores `current_player.saucer_value` on every
hit. The value is tied to the drop target phase and advances as phases
complete:

| drop_phase | After event             | saucer_value |
|-----------|-------------------------|--------------|
| 1 (Phase A) | game/ball start       | 5,000        |
| 2 (Phase B) | dt_phase_a_complete   | 10,000       |
| 3 (Phase C) | dt_phase_b_complete   | 20,000       |
| 4 (Phase D) | dt_phase_c_complete   | 30,000 (max) |
| 5 (Phase E) | dt_phase_d_complete   | 30,000 (unchanged) |

The saucer value never exceeds 30,000. Phase D and Phase E both score
30,000.

## Skill shot

On each ball launch the `skill_shot` mode is active and monitors the
saucer. A first-ball-launch saucer hit before any other playfield switch
scores an enhanced bonus (5K / 10K / 20K / 30K depending on a rotating
index). The skill shot mode deactivates on `skill_shot_awarded` or
`ball_drain`. This is separate from the regular saucer scoring above.

## Phase E reset

When the saucer is hit while `drop_phase == 5` (i.e. during Phase E),
it triggers a full reset in addition to scoring:

1. Posts `phase_e_saucer_reset`
2. Fires the drop target reset coil (raises the bank)
3. After 400ms fires the repositioning coils to present Phase A
4. Resets `drop_phase` to 1 and `saucer_value` to 5,000
5. **Preserves** `bonus_multiplier` — the 5× earned through Phase D
   remains active for the rest of the ball

`drop_phase` stays at 5 between Phase E completion and the saucer hit;
the saucer hit is what triggers the reset, not the phase completion itself.
