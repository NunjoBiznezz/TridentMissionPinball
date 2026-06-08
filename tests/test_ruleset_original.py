import os
import unittest

from mpf.tests.MpfGameTestCase import MpfGameTestCase


class TestDropTargetPhases(MpfGameTestCase):
    """Drop target phase progression for Trident Classic (ruleset_original).

    The original Stern Trident advances through five phases by knocking
    down specific target combinations.  Each completion raises the bonus
    multiplier, advances the saucer value, and re-raises targets for the
    next phase via coil_player.  smart_virtual automatically releases a
    drop target switch when its reset_coil fires, so we don't need to
    manage switch state manually between phases.

    Phase layout
    ------------
    Phase 1 → A (start): targets 2, 4 raised
    Phase 2 → B:         targets 1, 3, 5 raised;  2 & 4 stay down
    Phase 3 → C:         targets 1, 2, 4, 5 raised; 3 stays down
    Phase 4 → D:         all 5 raised
    Phase 5 → E:         all 5 raised (special award territory)
    """

    def get_config_file(self):
        return 'config_dev.yaml'

    def get_absolute_machine_path(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def get_platform(self):
        # smart_virtual auto-releases a drop target switch when its reset
        # coil fires, which mirrors the real coil behaviour between phases.
        return 'smart_virtual'

    def setUp(self):
        super().setUp()
        for event in ('dt_phase_a_complete', 'dt_phase_b_complete',
                      'dt_phase_c_complete', 'dt_phase_d_complete'):
            self.mock_event(event)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _start_game_original(self):
        """Start a one-player game and confirm ruleset_original is active."""
        self.fill_troughs()
        self.start_game()
        self.advance_time_and_run(1)
        self.assertTrue(
            self.machine.mode_controller.is_active('ruleset_original'),
            'ruleset_original should be active (current_ruleset defaults to 1)',
        )

    def _hit(self, *target_nums):
        """Knock down one or more drop targets by number."""
        for n in target_nums:
            self.hit_switch_and_run(f's_drop_target_{n}', 0)
        self.advance_time_and_run(0.2)

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def test_drop_target_phase_sequence(self):
        """Completing phases A → B → C → D raises drop_phase and bonus_multiplier."""
        self._start_game_original()

        # Phase 1 initial state
        self.assertPlayerVarEqual(1, 'drop_phase')
        self.assertPlayerVarEqual(1, 'bonus_multiplier')
        self.assertPlayerVarEqual(5000, 'saucer_value')

        # ── Phase A ──────────────────────────────────────────────────
        # Targets 2 and 4 start raised; knock them both down.
        # Completing the bank fires dt_phase_a_complete which raises
        # targets 1, 3, 5 via coil (smart_virtual auto-releases those
        # switches).
        self._hit(2, 4)

        self.assertEventCalled('dt_phase_a_complete')
        self.assertPlayerVarEqual(2, 'drop_phase')
        self.assertPlayerVarEqual(2, 'bonus_multiplier')
        self.assertPlayerVarEqual(10000, 'saucer_value')

        # ── Phase B ──────────────────────────────────────────────────
        # Targets 1, 3, 5 are now raised.  Knock them all down.
        # Completing the bank fires dt_phase_b_complete which raises
        # targets 1, 2, 4, 5 (target 3 stays down per rules).
        self._hit(1, 3, 5)

        self.assertEventCalled('dt_phase_b_complete')
        self.assertPlayerVarEqual(3, 'drop_phase')
        self.assertPlayerVarEqual(3, 'bonus_multiplier')
        self.assertPlayerVarEqual(20000, 'saucer_value')

        # ── Phase C ──────────────────────────────────────────────────
        # Targets 1, 2, 4, 5 are raised; target 3 is still down.
        # Knock down the four raised targets.
        # Completing the bank fires dt_phase_c_complete which raises
        # all five targets.
        self._hit(1, 2, 4, 5)

        self.assertEventCalled('dt_phase_c_complete')
        self.assertPlayerVarEqual(4, 'drop_phase')
        self.assertPlayerVarEqual(4, 'bonus_multiplier')
        self.assertPlayerVarEqual(30000, 'saucer_value')

        # ── Phase D ──────────────────────────────────────────────────
        # All five targets are raised.  Knock them all down.
        # Completing the bank fires dt_phase_d_complete and earns 5×.
        self._hit(1, 2, 3, 4, 5)

        self.assertEventCalled('dt_phase_d_complete')
        self.assertPlayerVarEqual(5, 'drop_phase')
        self.assertPlayerVarEqual(5, 'bonus_multiplier')


if __name__ == '__main__':
    unittest.main()
