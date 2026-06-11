import unittest

from tests.base import RulesetTestBase


class TestDropTargetPhases(RulesetTestBase):
    """Drop target phase progression for Trident Classic (ruleset_original).

    Phase layout (standing targets; the game raises the bank with
    c_drop_target_reset and knocks the rest down with the individual
    knockdown coils)
    ------------
    Phase 1 → A (start): targets 2, 4 standing
    Phase 2 → B:         targets 1, 3, 5 standing
    Phase 3 → C:         targets 1, 2, 4, 5 standing
    Phase 4 → D:         all 5 standing
    Phase 5 → E:         all 5 standing; special award, then saucer
                         resets to Phase A
    """

    def setUp(self):
        super().setUp()
        for event in ('dt_phase_a_complete', 'dt_phase_b_complete',
                      'dt_phase_c_complete', 'dt_phase_d_complete',
                      'dt_phase_e_complete', 'special_award_extra_ball',
                      'phase_e_saucer_reset'):
            self.mock_event(event)

    def _hit(self, *target_nums):
        """Knock down one or more drop targets by number.

        First waits out any repositioning in progress (reset bar at +0ms,
        knockdown coils at +400ms, switch mute windows up to +900ms) so the
        hits land on settled, standing targets — like a real ball would.
        """
        self.advance_time_and_run(1)
        for n in target_nums:
            self.hit_switch_and_run(f's_drop_target_{n}', 0)
        self.advance_time_and_run(0.2)

    def test_power_on_presents_phase_a(self):
        """At power-on (attract), the bank is raised and targets 1, 3, 5
        are knocked back down — the same Phase A setup a ball starts with."""
        self.advance_time_and_run(2)
        dt = self.machine.drop_targets
        self.assertFalse(dt['dt_2'].complete, 'target 2 should be standing')
        self.assertFalse(dt['dt_4'].complete, 'target 4 should be standing')
        self.assertTrue(dt['dt_1'].complete, 'target 1 should be down')
        self.assertTrue(dt['dt_3'].complete, 'target 3 should be down')
        self.assertTrue(dt['dt_5'].complete, 'target 5 should be down')

    def test_drop_target_phase_sequence(self):
        """Completing phases A → E raises drop_phase and bonus_multiplier;
        saucer hit during Phase E resets to Phase A with 5× preserved."""
        self._start_game_original()

        # Phase 1 initial state
        self.assertPlayerVarEqual(1, 'drop_phase')
        self.assertPlayerVarEqual(1, 'bonus_multiplier')
        self.assertPlayerVarEqual(5000, 'saucer_value')

        # Lamps show the Phase A combination: 2 & 4 standing
        self.advance_time_and_run(1)
        self.assertLightColor('l_drop_target_2', 'white')
        self.assertLightColor('l_drop_target_4', 'white')
        self.assertLightColor('l_drop_target_1', 'off')
        self.assertLightColor('l_drop_target_3', 'off')
        self.assertLightColor('l_drop_target_5', 'off')

        # ── Phase A ──────────────────────────────────────────────────
        self._hit(2, 4)

        self.assertEventCalled('dt_phase_a_complete')
        self.assertPlayerVarEqual(2, 'drop_phase')
        self.assertPlayerVarEqual(2, 'bonus_multiplier')
        self.assertPlayerVarEqual(10000, 'saucer_value')

        # Lamps show the Phase B combination: 1, 3, 5 standing
        self.advance_time_and_run(1)
        self.assertLightColor('l_drop_target_1', 'white')
        self.assertLightColor('l_drop_target_3', 'white')
        self.assertLightColor('l_drop_target_5', 'white')
        self.assertLightColor('l_drop_target_2', 'off')
        self.assertLightColor('l_drop_target_4', 'off')

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
