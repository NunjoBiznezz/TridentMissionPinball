import unittest

from tests.base import RulesetTestBase


class TestTilt(RulesetTestBase):
    """Tilt behaviour (original ruleset).

    With adj_tilt_warnings = 1 (default): the first plumb bob closure is a
    warning, the second tilts. A tilted ball awards no end-of-ball bonus;
    warnings reset between balls and a clean drain pays bonus normally.
    """

    def setUp(self):
        super().setUp()
        self.mock_event('tilt_warning')
        self.mock_event('tilt')

    def _bob(self):
        self.hit_and_release_switch('s_tilt')
        # multiple_hit_window is 300ms — space the closures apart
        self.advance_time_and_run(0.5)

    def _drain(self):
        self.hit_switch_and_run('s_outhole', 1)
        self.advance_time_and_run(2)

    def test_warning_then_tilt_no_bonus(self):
        self._start_game_original()

        self._bob()
        self.assertEventCalled('tilt_warning')
        self.assertEventNotCalled('tilt')
        self.assertFalse(self.machine.game.tilted)

        self._bob()
        self.assertEventCalled('tilt')
        self.assertTrue(self.machine.game.tilted)

        score_at_tilt = self.machine.game.player['score']
        self._drain()
        # No end-of-ball bonus on a tilted ball (a clean drain would have
        # paid bonus_steps * 1000 * multiplier = 1000 minimum).
        self.assertEqual(score_at_tilt, self.machine.game.player['score'])

        # Next ball: warnings are reset and the game is no longer tilted
        self.assertEqual(2, self.machine.game.player['ball'])
        self.assertFalse(self.machine.game.tilted)
        self.assertEqual(0, self.machine.game.player['tilt_warnings'])

    def test_clean_drain_pays_bonus(self):
        self._start_game_original()
        score_before = self.machine.game.player['score']
        self._drain()
        # bonus_steps starts at 1, multiplier 1 → 1000 points of bonus
        self.assertEqual(score_before + 1000, self.machine.game.player['score'])


if __name__ == '__main__':
    unittest.main()
