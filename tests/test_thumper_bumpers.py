import unittest

from tests.base import RulesetTestBase


class TestThumperBumpers(RulesetTestBase):
    """Lower slingshot (thumper bumper) scoring for Trident Classic.

    Scoring depends on the balls_per_game_setting machine variable:
        3-ball game → 1,000 pts per hit
        5-ball game →   100 pts per hit

    Both left (s_ll_sling) and right (s_lr_sling) lower slings share
    the same scoring rule via the lower_sling_hit event.
    """

    def setUp(self):
        super().setUp()
        self._start_game_original()
        self.post_event('skill_shot_awarded')
        self.advance_time_and_run(0.1)

    def _score(self):
        return self.machine.game.player.score

    def _hit_ll(self):
        before = self._score()
        self.hit_and_release_switch('s_ll_sling')
        self.advance_time_and_run(0.1)
        return self._score() - before

    def _hit_lr(self):
        before = self._score()
        self.hit_and_release_switch('s_lr_sling')
        self.advance_time_and_run(0.1)
        return self._score() - before

    def _hit(self, switch):
        before = self._score()
        self.hit_and_release_switch(switch)
        self.advance_time_and_run(0.1)
        return self._score() - before

    def test_three_ball_game_scores_1000(self):
        """Both lower slings score 1,000 when balls_per_game_setting is 3."""
        self.assertMachineVarEqual(3, 'balls_per_game_setting')
        self.assertEqual(1000, self._hit_ll())
        self.assertEqual(1000, self._hit_lr())

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

    def test_five_ball_game_scores_100(self):
        """Both lower slings score 100 when balls_per_game_setting is 5."""
        self.machine.variables.set_machine_var('balls_per_game_setting', 5)
        self.advance_time_and_run(0.1)
        self.assertEqual(100, self._hit_ll())
        self.assertEqual(100, self._hit_lr())

    def test_switching_setting_mid_game_takes_effect_immediately(self):
        """Changing balls_per_game_setting during a game is reflected instantly."""
        self.assertMachineVarEqual(3, 'balls_per_game_setting')
        self.assertEqual(1000, self._hit_ll())

        self.machine.variables.set_machine_var('balls_per_game_setting', 5)
        self.advance_time_and_run(0.1)
        self.assertEqual(100, self._hit_ll())

        self.machine.variables.set_machine_var('balls_per_game_setting', 3)
        self.advance_time_and_run(0.1)
        self.assertEqual(1000, self._hit_ll())


if __name__ == '__main__':
    unittest.main()
