import unittest

from tests.base import RulesetTestBase


class TestSpecialAwardFreeGame(RulesetTestBase):
    """Special award setting 3 ('Free Game'): special_award_free_game must
    add a credit (capped at max_credits), pulse the knocker, and play the
    coin-insertion chime — mirroring a real coin insertion.

    See specs/original/special_award_free_game.md.
    """

    def _credits(self):
        return self.machine.variables.get_machine_var('credits')

    def test_free_game_awards_a_credit(self):
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._start_game_original()
        before = self._credits()

        self.post_event('special_award_free_game')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 1, self._credits())

    def test_free_game_credited_event_fires(self):
        self._start_game_original()
        self.mock_event('special_award_free_game_credited')

        self.post_event('special_award_free_game')
        self.advance_time_and_run(0.1)

        self.assertEventCalled('special_award_free_game_credited')

    def test_free_game_capped_at_max_credits(self):
        self._start_game_original()
        max_credits = self.machine.variables.get_machine_var('max_credits')
        self.machine.variables.set_machine_var('credits', max_credits)
        self.mock_event('special_award_free_game_credited')

        self.post_event('special_award_free_game')
        self.advance_time_and_run(0.1)

        self.assertEventNotCalled('special_award_free_game_credited')
        self.assertEqual(max_credits, self._credits())

    def test_dt_phase_e_complete_awards_free_game(self):
        """End-to-end: drop target Phase E special with setting=3 awards a credit."""
        self.machine.variables.set_machine_var('special_award_setting', 3)
        self._start_game_original()
        before = self._credits()

        self.post_event('dt_phase_e_complete')
        self.advance_time_and_run(0.1)

        self.assertEqual(before + 1, self._credits())


if __name__ == '__main__':
    unittest.main()
