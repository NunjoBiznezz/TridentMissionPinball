# Spec: Special Award — "Free Game"

Status: APPROVED — implementing.
Scope: ruleset_original (faithful-to-1979 bar). Not a house rule.

## Source of truth

`Stern_Trident_Man.pdf`, page 9, Adjustment 13 "SPECIAL AWARD":

| Award                 | Switch 31 | Switch 32 |
|-----------------------|-----------|-----------|
| Free Ball             | ON        | OFF       |
| Free Game             | OFF       | ON        |
| 100,000 Points        | OFF       | OFF       |
| Free Ball & Free Game | ON        | ON        |

The codebase already models this as `machine.special_award_setting` (1=points, 2=free ball, 3=free game, 4=free ball & free game), matching the four switch combinations.

## Current state (bug)

Three trigger points in `modes/ruleset_original/config/ruleset_original.yaml` post `special_award_free_game` when `special_award_setting` is 3 or 4:

- `dt_phase_e_complete` (drop target special) — line 139
- `standup_second_complete` (double standup special) — line 152
- `right_special_awarded` (right outlane special) — line 165

**Nothing in the codebase handles `special_award_free_game`.** No `variable_player`, `event_player`, or device config anywhere reacts to it. Compare to the sibling event `special_award_extra_ball`, which an `extra_balls` device (`drop_target_special`) actually consumes (`modes/ruleset_original/config/ruleset_original.yaml` line 45) and which works correctly.

Net effect: when an operator sets "Free Game" or "Free Ball & Free Game," the free-game half of that award currently does nothing — no credit is added, nothing is logged, nothing fires. (The free-ball half, when setting is 4, does work independently via the same `special_award_extra_ball` path.)

## Decisions (confirmed)

1. **Credit award.** Mirror the existing pattern from `modes/credits/config/credits.yaml`: increment `machine.credits` by 1, gated on `machine.credits < machine.max_credits` (no-op if already at the cap — same as coin insertion).
2. **Knocker.** Pulse `c_knocker` on award, matching the classic replay-award thunk.
3. **Sound.** Reuse `013_AddCredit` (the existing coin-insertion sound).

## Implementation

```yaml
event_player:
  special_award_free_game{machine.credits < machine.max_credits}: special_award_free_game_credited

sound_player:
  special_award_free_game_credited: 013_AddCredit

coil_player:
  special_award_free_game_credited:
    c_knocker: pulse

variable_player:
  special_award_free_game_credited:
    credits: {int: 1, action: add_machine}
```

An intermediate `special_award_free_game_credited` event is posted only when the cap check passes, so the knocker/sound/credit all fire together and stay silent if already maxed.
