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
        # 1 → 4 → 7 → 10  (3 chimes at 150ms intervals; need > 300ms to complete)
        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(4, 'bonus_steps')

        # Lamp display: exactly one units lamp lit (4), 10K lamp off
        self.assertLightColor('l_bonus_4', 'white')
        self.assertLightColor('l_bonus_1', 'off')
        self.assertLightColor('l_bonus_3', 'off')
        self.assertLightColor('l_bonus_10', 'off')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(7, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(10, 'bonus_steps')

        # At exactly 10: only the 10K lamp is lit
        self.assertLightColor('l_bonus_10', 'white')
        self.assertLightColor('l_bonus_4', 'off')
        self.assertLightColor('l_bonus_7', 'off')

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

        # 13,000 = units lamp 3 + the 10K lamp
        self.assertLightColor('l_bonus_3', 'white')
        self.assertLightColor('l_bonus_10', 'white')
        self.assertLightColor('l_bonus_2', 'off')

        # ── Right inlane: +3 again ───────────────────────────────────
        # 13 → 16 → 19  (max)
        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(16, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        # ── Cap: no source should advance past 19 ────────────────────
        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        self.hit_and_release_switch('s_right_return_lane')
        self.advance_time_and_run(0.5)
        self.assertPlayerVarEqual(19, 'bonus_steps')

        self.hit_and_release_switch('s_ul_sling')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(19, 'bonus_steps')

    def test_bonus_countdown_with_multiplier(self):
        """End-of-ball countdown scores 1,000 per step and repeats the
        full count once per earned multiplier level (2X = twice)."""
        self._start_game_original()
        # Let the serve confirm (3s eject timeout) before draining later
        self.advance_time_and_run(3.5)

        # Earn 2X: complete Phase A (targets 2 & 4, +500 each)
        self.hit_switch_and_run('s_drop_target_2', 0)
        self.advance_time_and_run(0.2)
        self.hit_switch_and_run('s_drop_target_4', 0)
        self.advance_time_and_run(1.5)
        self.assertPlayerVarEqual(2, 'bonus_multiplier')

        # Advance bonus to 3 steps (left return lane +1, twice)
        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.hit_and_release_switch('s_left_return_lane')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(3, 'bonus_steps')

        score_before = self.machine.game.player['score']

        # Drain: countdown = 3 steps x 1,000 x 2 passes = 6,000
        self.hit_switch_and_run('s_outhole', 1)
        self.advance_time_and_run(3)

        self.assertEqual(score_before + 6000, self.machine.game.player['score'])
        # Counter consumed and reset for the next ball
        self.assertPlayerVarEqual(1, 'bonus_steps')
        self.assertPlayerVarEqual(1, 'bonus_multiplier')


if __name__ == '__main__':
    unittest.main()
