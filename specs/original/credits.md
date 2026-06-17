# Spec: Credits & Coin Insertion

Status: APPROVED — implemented and tested.
Source: `Stern_Trident_Man.pdf` p. 3 (Installation — coin mechanism);
  Adjustments 1–11 (chute coin-per-credit ratios).
Tests: `tests/test_credits.py`

## Machine variables

| Variable       | Default | Description                        |
|----------------|---------|------------------------------------|
| `credits`      | 0       | Current credit count               |
| `max_credits`  | 40      | Maximum storable credits           |
| `adj_free_play`| 0       | 1 = no credits deducted on game start |

## Coin insertion

Three coin chutes (`s_coin_1`, `s_coin_2`, `s_coin_3`). Each chute
insertion fires a `coin_inserted_chute_N` event. When
`machine.credits < machine.max_credits`:
- `credits` increments by 1
- `013_AddCredit` sound plays

Insertions above `max_credits` are silently ignored (no sound, no
increment).

## Game start

When a game starts, 1 credit is deducted:
```
game_started{machine.adj_free_play == 0 and machine.credits > 0}:
  credits: {int: -1, action: add_machine}
```
In free-play mode (`adj_free_play == 1`) no credit is deducted.

## Coin-per-credit ratios

Adjustments 1–11 control how many coins from each chute equal one
credit (e.g. 1-coin, 2-coin, or multi-coin-per-credit). These are
set via the service menu and stored as machine vars. The credits mode
wires the ratio logic; this spec covers only the basic 1-coin-1-credit
default behavior exercised by the tests.

## Related

The Free Game special award also increments `credits` — see
[special_award_free_game.md](special_award_free_game.md).
