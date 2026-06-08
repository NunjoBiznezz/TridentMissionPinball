import unittest

from tests.base import RulesetTestBase


class TestSpinners(RulesetTestBase):
    """Spinner scoring for Trident Classic (ruleset_original).

    Each spin scores the spinner's base value plus the purple bonus when
    the purple side matches.

    Base values (reset on ball drain):
        left_spinner_value  = 200
        right_spinner_value = 200
        purple_bonus        = 0

    Color bonuses (first standup hit per ball only):
        white, amber → left_spinner_value  +400 each  (max 1,000)
        green, yellow → right_spinner_value +400 each  (max 1,000)
        purple        → purple_bonus +1,000, purple_on_left = 1

    Purple alternation:
        upper slings flip purple_on_left when purple_bonus > 0
        → purple adds to whichever spinner it is currently assigned to
        → slings do NOT flip when purple_bonus == 0
    """

    def setUp(self):
        super().setUp()
        self._start_game_original()
        # End skill shot to prevent its 10K left-spinner bonus distorting
        # score delta assertions.
        self.post_event('skill_shot_awarded')
        self.advance_time_and_run(0.1)

    def _score(self):
        return self.machine.game.player.score

    def _spin_left(self):
        before = self._score()
        self.hit_and_release_switch('s_left_spinner')
        self.advance_time_and_run(0.1)
        return self._score() - before

    def _spin_right(self):
        before = self._score()
        self.hit_and_release_switch('s_right_spinner')
        self.advance_time_and_run(0.1)
        return self._score() - before

    def _hit_standup(self, colour):
        self.hit_and_release_switch(f's_standup_{colour}')
        self.advance_time_and_run(0.1)

    def _hit_ul_sling(self):
        self.hit_and_release_switch('s_ul_sling')
        self.advance_time_and_run(0.1)

    def _hit_ur_sling(self):
        self.hit_and_release_switch('s_ur_sling')
        self.advance_time_and_run(0.1)

    # ── Base scoring ─────────────────────────────────────────────────

    def test_base_spinner_scoring(self):
        """Without any standup bonuses, spinners score their initial 200 each."""
        self.assertPlayerVarEqual(200, 'left_spinner_value')
        self.assertPlayerVarEqual(200, 'right_spinner_value')
        self.assertPlayerVarEqual(0,   'purple_bonus')

        self.assertEqual(200, self._spin_left())
        self.assertEqual(200, self._spin_right())

    # ── Color bonus advancement ───────────────────────────────────────

    def test_left_spinner_color_bonuses(self):
        """White and amber standups each add 400 to the left spinner (first hit only)."""
        self.assertEqual(200, self._spin_left())

        self._hit_standup('white')
        self.assertPlayerVarEqual(600, 'left_spinner_value')
        self.assertEqual(600, self._spin_left())

        self._hit_standup('amber')
        self.assertPlayerVarEqual(1000, 'left_spinner_value')
        self.assertEqual(1000, self._spin_left())

        # Hitting the same target again does NOT re-advance the spinner value
        self._hit_standup('white')
        self.assertPlayerVarEqual(1000, 'left_spinner_value')

    def test_right_spinner_color_bonuses(self):
        """Green and yellow standups each add 400 to the right spinner (first hit only)."""
        self.assertEqual(200, self._spin_right())

        self._hit_standup('green')
        self.assertPlayerVarEqual(600, 'right_spinner_value')
        self.assertEqual(600, self._spin_right())

        self._hit_standup('yellow')
        self.assertPlayerVarEqual(1000, 'right_spinner_value')
        self.assertEqual(1000, self._spin_right())

        # Hitting the same target again does NOT re-advance the spinner value
        self._hit_standup('green')
        self.assertPlayerVarEqual(1000, 'right_spinner_value')

    # ── Purple bonus ─────────────────────────────────────────────────

    def test_purple_bonus_scores_on_assigned_spinner(self):
        """Purple standup adds purple_bonus to whichever spinner it is assigned to."""
        # Build up both spinners and add purple
        self._hit_standup('white')
        self._hit_standup('amber')
        self._hit_standup('green')
        self._hit_standup('yellow')
        self._hit_standup('purple')

        self.assertPlayerVarEqual(1000, 'left_spinner_value')
        self.assertPlayerVarEqual(1000, 'right_spinner_value')
        self.assertPlayerVarEqual(1000, 'purple_bonus')
        self.assertPlayerVarEqual(1,    'purple_on_left')

        # Purple is on the left: left spin = base + purple, right = base only
        self.assertEqual(2000, self._spin_left())
        self.assertEqual(1000, self._spin_right())

    # ── Purple alternation ────────────────────────────────────────────

    def test_purple_alternates_via_upper_slings(self):
        """Upper slings move the purple bonus to the opposite spinner."""
        self._hit_standup('white')
        self._hit_standup('amber')
        self._hit_standup('green')
        self._hit_standup('yellow')
        self._hit_standup('purple')

        # Purple starts on left
        self.assertPlayerVarEqual(1, 'purple_on_left')
        self.assertEqual(2000, self._spin_left())
        self.assertEqual(1000, self._spin_right())

        # Upper left sling → purple moves to right
        self._hit_ul_sling()
        self.assertPlayerVarEqual(0, 'purple_on_left')
        self.assertEqual(1000, self._spin_left())
        self.assertEqual(2000, self._spin_right())

        # Upper right sling → purple moves back to left
        self._hit_ur_sling()
        self.assertPlayerVarEqual(1, 'purple_on_left')
        self.assertEqual(2000, self._spin_left())
        self.assertEqual(1000, self._spin_right())

    def test_slings_do_not_alternate_without_purple_bonus(self):
        """Upper slings leave purple_on_left unchanged when purple_bonus is 0."""
        self.assertPlayerVarEqual(0, 'purple_bonus')
        self.assertPlayerVarEqual(1, 'purple_on_left')

        self._hit_ul_sling()
        self.assertPlayerVarEqual(1, 'purple_on_left')

        self._hit_ur_sling()
        self.assertPlayerVarEqual(1, 'purple_on_left')


if __name__ == '__main__':
    unittest.main()
