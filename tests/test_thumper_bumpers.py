import unittest

from tests.base import RulesetTestBase


class TestThumperBumpers(RulesetTestBase):
    """Slingshot, pop bumper and 10-point switch scoring for Trident
    Classic (ruleset_original).

        Lower slings  → 10 pts flat (s_ll_sling / s_lr_sling)
        Pop bumpers   → 1,000 pts on a 3-ball game, 100 on 5-ball
        s_10_pts      → 10 pts per closure
    """

    def setUp(self):
        super().setUp()
        self._start_game_original()
        self.post_event('skill_shot_awarded')
        self.advance_time_and_run(0.1)

    def _score(self):
        return self.machine.game.player.score

    def _hit(self, switch):
        before = self._score()
        self.hit_and_release_switch(switch)
        self.advance_time_and_run(0.1)
        return self._score() - before

    def test_lower_slings_score_10(self):
        """Both lower slings score a flat 10 points."""
        self.assertEqual(10, self._hit('s_ll_sling'))
        self.assertEqual(10, self._hit('s_lr_sling'))

        # Independent of the balls-per-game setting
        self.machine.variables.set_machine_var('balls_per_game_setting', 5)
        self.advance_time_and_run(0.1)
        self.assertEqual(10, self._hit('s_ll_sling'))
        self.assertEqual(10, self._hit('s_lr_sling'))

    def test_pop_bumpers_score(self):
        """Both pop bumpers score 1,000 on a 3-ball game, 100 on 5-ball."""
        self.assertMachineVarEqual(3, 'balls_per_game_setting')
        self.assertEqual(1000, self._hit('s_top_bumper'))
        self.assertEqual(1000, self._hit('s_bottom_bumper'))

        self.machine.variables.set_machine_var('balls_per_game_setting', 5)
        self.advance_time_and_run(0.1)
        self.assertEqual(100, self._hit('s_top_bumper'))
        self.assertEqual(100, self._hit('s_bottom_bumper'))

    def test_10_point_switch_scores(self):
        """The 10 point switch awards 10 points per closure."""
        self.assertEqual(10, self._hit('s_10_pts'))
        self.assertEqual(10, self._hit('s_10_pts'))


if __name__ == '__main__':
    unittest.main()
