import unittest

from tests.base import RulesetTestBase


class TestTournamentScoring(RulesetTestBase):
    """adj_tournament_scoring (Adjustment 22) substitutes point awards for
    real prizes (extra balls, free game credits) during tournament play.

    adj_extra_ball_award (default 25,000) replaces extra balls.
    adj_special_award  (default 50,000) replaces free game credits.

    See specs/house-rules/tournament_scoring.md.
    """

    def _score(self):
        return self.machine.game.player.score

    def _tournament_on(self):
        self.machine.variables.set_machine_var('adj_tournament_scoring', 1)

    # ── Extra ball substitution (pre-existing behaviour, regression guard) ──

    def test_extra_ball_tournament_scores_points(self):
        """Setting 2 + tournament on: dt_phase_e_complete scores adj_extra_ball_award."""
        self.machine.variables.set_machine_var('special_award_setting', 2)
        self._tournament_on()
        self._start_game_original()
        before = self._score()

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 25000, self._score())

    def test_extra_ball_no_tournament_awards_extra_ball(self):
        """Setting 2, tournament off: dt_phase_e_complete posts special_award_extra_ball."""
        self.machine.variables.set_machine_var('special_award_setting', 2)
        self.mock_event('special_award_extra_ball')
        self._start_game_original()

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEventCalled('special_award_extra_ball')

    # ── Free game substitution (new behaviour) ──────────────────────────────

    def test_free_game_tournament_scores_points(self):
        """Setting 3 + tournament on: dt_phase_e_complete scores adj_special_award."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._tournament_on()
        self._start_game_original()
        before = self._score()

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 50000, self._score())

    def test_free_game_tournament_no_credit_awarded(self):
        """Setting 3 + tournament on: no credit is added."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._tournament_on()
        self._start_game_original()
        self.mock_event('special_award_free_game_credited')

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEventNotCalled('special_award_free_game_credited')

    def test_free_game_no_tournament_awards_credit(self):
        """Setting 3, tournament off: dt_phase_e_complete awards a credit."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._start_game_original()
        credits_before = self.machine.variables.get_machine_var('credits')

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(credits_before + 1,
                         self.machine.variables.get_machine_var('credits'))

    # ── Setting 4 (Free Ball & Free Game): both halves substitute independently

    def test_setting4_tournament_scores_both(self):
        """Setting 4 + tournament on: dt_phase_e_complete scores both
        adj_extra_ball_award and adj_special_award."""
        self.machine.variables.set_machine_var('special_award_setting', 4)
        self._tournament_on()
        self._start_game_original()
        before = self._score()

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 25000 + 50000, self._score())

    # ── Other trigger sources (standup, right outlane) ──────────────────────

    def test_standup_second_scores_points_in_tournament(self):
        """Setting 3 + tournament on: standup_second_complete also substitutes."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._tournament_on()
        self._start_game_original()
        before = self._score()

        self.post_event('standup_second_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 50000, self._score())

    def test_right_special_scores_points_in_tournament(self):
        """Setting 3 + tournament on: right_special_awarded also substitutes."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._tournament_on()
        self._start_game_original()
        before = self._score()

        self.post_event('right_special_awarded')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 50000, self._score())


if __name__ == '__main__':
    unittest.main()
