import unittest

from tests.base import RulesetTestBase


class TestSaucer(RulesetTestBase):
    """Top eject pocket (saucer) behaviour for Trident Classic (ruleset_original).

    The saucer always scores its current saucer_value.  That value
    advances with each phase completion:

        Start (Phase A) :  5,000
        Phase A complete: 10,000
        Phase B complete: 20,000
        Phase C complete: 30,000  ← maximum; stays here through Phase D/E
        Phase E saucer  :  5,000  ← scoring reset (drop_phase → 1)

    Phase events are posted directly so this test focuses on saucer
    logic without depending on the drop-target mechanism.
    """

    def _score(self):
        return self.machine.game.player.score

    def _hit_saucer(self):
        self.hit_and_release_switch('s_saucer')
        self.advance_time_and_run(0.1)

    def test_saucer_value_advances_and_caps(self):
        """Saucer scores 5K→10K→20K→30K as phases complete; stays at 30K through Phase D."""
        self._start_game_original()

        # End the skill shot mode so its scoring doesn't interfere with
        # saucer delta assertions below.
        self.post_event('skill_shot_awarded')
        self.advance_time_and_run(0.1)

        # ── Initial: Phase A, 5K ─────────────────────────────────────
        self.assertPlayerVarEqual(5000, 'saucer_value')
        before = self._score()
        self._hit_saucer()
        self.assertEqual(before + 5000, self._score())

        # ── Phase A complete → 10K ───────────────────────────────────
        self.post_event('dt_phase_a_complete')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(10000, 'saucer_value')
        before = self._score()
        self._hit_saucer()
        self.assertEqual(before + 10000, self._score())

        # ── Phase B complete → 20K ───────────────────────────────────
        self.post_event('dt_phase_b_complete')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(20000, 'saucer_value')
        before = self._score()
        self._hit_saucer()
        self.assertEqual(before + 20000, self._score())

        # ── Phase C complete → 30K (maximum) ────────────────────────
        self.post_event('dt_phase_c_complete')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(30000, 'saucer_value')
        before = self._score()
        self._hit_saucer()
        self.assertEqual(before + 30000, self._score())

        # ── Phase D complete → saucer stays at 30K ───────────────────
        self.post_event('dt_phase_d_complete')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(30000, 'saucer_value')
        before = self._score()
        self._hit_saucer()
        self.assertEqual(before + 30000, self._score())

    def test_saucer_phase_e_reset(self):
        """During Phase E (drop_phase=5) saucer scores 30K then resets to Phase A."""
        self._start_game_original()
        self.post_event('skill_shot_awarded')
        self.advance_time_and_run(0.1)

        # Advance to Phase E via posted events
        for event in ('dt_phase_a_complete', 'dt_phase_b_complete',
                      'dt_phase_c_complete', 'dt_phase_d_complete'):
            self.post_event(event)
            self.advance_time_and_run(0.1)

        self.assertPlayerVarEqual(5, 'drop_phase')
        self.assertPlayerVarEqual(30000, 'saucer_value')

        # Saucer hit during Phase E: scores 30K, then resets to Phase A
        before = self._score()
        self._hit_saucer()

        self.assertEqual(before + 30000, self._score())
        self.assertPlayerVarEqual(1, 'drop_phase')
        self.assertPlayerVarEqual(5000, 'saucer_value')


if __name__ == '__main__':
    unittest.main()
