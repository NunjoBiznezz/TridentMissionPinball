import unittest

from tests.base import RulesetTestBase


class TestBonusAdvancement(RulesetTestBase):
    """Bonus score advancement for Trident Classic (ruleset_original).

    Three sources advance the bonus counter:
        Left inlane   → +1 step
        Upper slings  → +1 step
        Right inlane  → +3 steps

    The counter runs from 1 (1,000 starting bonus) to a maximum of 19
    (19,000).  At step 10, the 10K lamp lights and the 1K–9K lamps clear
    so they can represent 11K–19K in the second pass.  No handler exists
    for step 19, so further hits are silently ignored.

    Ball-drain formula: bonus_steps × 1,000 × bonus_multiplier.
    """

    def setUp(self):
        super().setUp()

    def test_bonus_advances_to_max_and_caps(self):
        """Advance bonus to 19,000 via all three sources; verify cap holds."""
        self._start_game_original()

        # Game starts at 1 step (1,000 bonus)
        self.assertPlayerVarEqual(1, 'bonus_steps')

        # ── Right inlane: +3 each time ───────────────────────────────
        # 1 → 4 → 7 → 10
        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(4, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(7, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(10, 'bonus_steps')

        # ── Left inlane: +1 step ─────────────────────────────────────
        # 10 → 11 → 12
        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(11, 'bonus_steps')

        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(12, 'bonus_steps')

        # ── Upper sling: +1 step ─────────────────────────────────────
        # 12 → 13
        self.hit_and_release_switch('s_ul_sling')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(13, 'bonus_steps')

        # ── Right inlane: +3 again ───────────────────────────────────
        # 13 → 16 → 19  (max)
        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(16, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        # ── Cap: no source should advance past 19 ────────────────────
        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        self.hit_and_release_switch('s_ul_sling')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')


if __name__ == '__main__':
    unittest.main()
