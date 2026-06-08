import unittest

from tests.base import RulesetTestBase


class TestDropTargetPhases(RulesetTestBase):
    """Drop target phase progression for Trident Classic (ruleset_original).

    Phase layout
    ------------
    Phase 1 → A (start): targets 2, 4 raised
    Phase 2 → B:         all 5 raised after completion
    Phase 3 → C:         all 5 raised after completion
    Phase 4 → D:         all 5 raised after completion
    Phase 5 → E:         special award, then saucer resets to Phase A
    """

    def setUp(self):
        super().setUp()
        for event in ('dt_phase_a_complete', 'dt_phase_b_complete',
                      'dt_phase_c_complete', 'dt_phase_d_complete',
                      'dt_phase_e_complete', 'special_award_extra_ball',
                      'phase_e_saucer_reset'):
            self.mock_event(event)

    def _hit(self, *target_nums):
        """Knock down one or more drop targets by number."""
        for n in target_nums:
            self.hit_switch_and_run(f's_drop_target_{n}', 0)
        self.advance_time_and_run(0.2)

    def test_drop_target_phase_sequence(self):
        """Completing phases A → E raises drop_phase and bonus_multiplier;
        saucer hit during Phase E resets to Phase A with 5× preserved."""
        self._start_game_original()

        # Phase 1 initial state
        self.assertPlayerVarEqual(1, 'drop_phase')
        self.assertPlayerVarEqual(1, 'bonus_multiplier')
        self.assertPlayerVarEqual(5000, 'saucer_value')

        # ── Phase A ──────────────────────────────────────────────────
        self._hit(2, 4)

        self.assertEventCalled('dt_phase_a_complete')
        self.assertPlayerVarEqual(2, 'drop_phase')
        self.assertPlayerVarEqual(2, 'bonus_multiplier')
        self.assertPlayerVarEqual(10000, 'saucer_value')

        # ── Phase B ──────────────────────────────────────────────────
        self._hit(1, 3, 5)

        self.assertEventCalled('dt_phase_b_complete')
        self.assertPlayerVarEqual(3, 'drop_phase')
        self.assertPlayerVarEqual(3, 'bonus_multiplier')
        self.assertPlayerVarEqual(20000, 'saucer_value')

        # ── Phase C ──────────────────────────────────────────────────
        self._hit(1, 2, 4, 5)

        self.assertEventCalled('dt_phase_c_complete')
        self.assertPlayerVarEqual(4, 'drop_phase')
        self.assertPlayerVarEqual(4, 'bonus_multiplier')
        self.assertPlayerVarEqual(30000, 'saucer_value')

        # ── Phase D ──────────────────────────────────────────────────
        self._hit(1, 2, 3, 4, 5)

        self.assertEventCalled('dt_phase_d_complete')
        self.assertPlayerVarEqual(5, 'drop_phase')
        self.assertPlayerVarEqual(5, 'bonus_multiplier')

        # ── Phase E ──────────────────────────────────────────────────
        # Default special_award_setting=2, adj_tournament_scoring=0
        # → special_award_extra_ball dispatched.
        self._hit(1, 2, 3, 4, 5)

        self.assertEventCalled('dt_phase_e_complete')
        self.assertEventCalled('special_award_extra_ball')
        self.assertPlayerVarEqual(5, 'drop_phase')  # stays at 5 until saucer

        # ── Saucer hit resets progression ────────────────────────────
        # drop_phase → 1, saucer_value → 5K; earned 5× bonus preserved.
        self.hit_switch_and_run('s_saucer', 0)
        self.advance_time_and_run(0.2)

        self.assertEventCalled('phase_e_saucer_reset')
        self.assertPlayerVarEqual(1, 'drop_phase')
        self.assertPlayerVarEqual(5000, 'saucer_value')
        self.assertPlayerVarEqual(5, 'bonus_multiplier')


if __name__ == '__main__':
    unittest.main()
