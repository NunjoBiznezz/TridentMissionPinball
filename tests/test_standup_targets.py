import unittest

from tests.base import RulesetTestBase


class TestStandupTargets(RulesetTestBase):
    """Standup target behaviour for Trident Classic (ruleset_original).

    Each target scores 1000 pts on every hit.  Spinner values advance
    only on the FIRST hit per ball (guarded by *_applied player vars
    that reset on ball_drain).  Two full cycles are available per ball:

    Cycle 1 → standup_first_complete  → extra ball lit
    Cycle 2 → standup_second_complete → right outlane special lit

    The accrual uses disable_on_complete: false so it stays active
    for the second cycle after the first completes.
    """

    def setUp(self):
        super().setUp()
        for event in ('standup_first_complete', 'standup_second_complete',
                      'collect_standup_extra_ball', 'right_special_awarded',
                      'special_award_extra_ball'):
            self.mock_event(event)

    def test_standup_target_sequence(self):
        """Standup targets advance spinners, light extra ball, then right outlane special."""
        self._start_game_original()

        # Initial state
        self.assertPlayerVarEqual(200, 'left_spinner_value')
        self.assertPlayerVarEqual(200, 'right_spinner_value')
        self.assertPlayerVarEqual(0,   'purple_bonus')
        self.assertPlayerVarEqual(0,   'extra_ball_lit')
        self.assertPlayerVarEqual(0,   'right_special_lit')

        # ── First standup cycle ──────────────────────────────────────
        # white, amber → left_spinner +400 each (200 → 600 → 1000)
        # green, yellow → right_spinner +400 each (200 → 600 → 1000)
        # purple        → purple_bonus +1000, purple_on_left=1

        self.hit_and_release_switch('s_standup_white')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(600, 'left_spinner_value')

        self.hit_and_release_switch('s_standup_amber')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(1000, 'left_spinner_value')

        self.hit_and_release_switch('s_standup_green')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(600, 'right_spinner_value')

        self.hit_and_release_switch('s_standup_yellow')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(1000, 'right_spinner_value')

        self.hit_and_release_switch('s_standup_purple')
        self.advance_time_and_run(0.1)
        self.assertPlayerVarEqual(1000, 'purple_bonus')
        self.assertPlayerVarEqual(1,    'purple_on_left')

        # All 5 hit → standup_first_complete → extra ball lit
        self.assertEventCalled('standup_first_complete')
        self.assertPlayerVarEqual(1, 'extra_ball_lit')
        self.assertPlayerVarEqual(0, 'right_special_lit')

        # ── Extra ball collection ────────────────────────────────────
        # Right inlane with extra_ball_lit collects the extra ball and
        # clears the lamp.
        self.hit_switch_and_run('s_right_inlane', 0)
        self.advance_time_and_run(0.1)
        self.assertEventCalled('collect_standup_extra_ball')
        self.assertPlayerVarEqual(0, 'extra_ball_lit')

        # ── Second standup cycle ─────────────────────────────────────
        # Accrual resets automatically (reset_on_complete: true, disable_on_complete: false).
        # Spinner values do NOT advance further: *_applied vars are still
        # set and only reset on ball_drain.
        for sw in ('s_standup_white', 's_standup_amber', 's_standup_green',
                   's_standup_yellow', 's_standup_purple'):
            self.hit_and_release_switch(sw)
        self.advance_time_and_run(0.2)

        self.assertPlayerVarEqual(1000, 'left_spinner_value')
        self.assertPlayerVarEqual(1000, 'right_spinner_value')

        self.assertEventCalled('standup_second_complete')
        self.assertPlayerVarEqual(1, 'right_special_lit')

        # ── Right outlane special collection ────────────────────────
        # Default special_award_setting=2, adj_tournament_scoring=0
        # → dispatches special_award_extra_ball.
        self.hit_switch_and_run('s_right_outlane', 0)
        self.advance_time_and_run(0.1)
        self.assertEventCalled('right_special_awarded')
        self.assertEventCalled('special_award_extra_ball')
        self.assertPlayerVarEqual(0, 'right_special_lit')


if __name__ == '__main__':
    unittest.main()
