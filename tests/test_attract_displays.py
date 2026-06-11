import unittest

from tests.base import RulesetTestBase


class TestAttractDisplays(RulesetTestBase):
    """Attract-mode score display cycle.

    All four player displays alternate: high score to date → blank → 00,
    2 seconds per step, repeating until a game starts.
    """

    def _texts(self):
        return [
            self.machine.segment_displays[f'player{n}_score'].hw_display.text.strip()
            for n in range(1, 5)
        ]

    def test_attract_score_cycle(self):
        self.assertTrue(self.machine.mode_controller.is_active('attract'))
        high_score = str(self.machine.variables.get_machine_var('high_game_to_date'))

        # Sample the displays across one full 6s cycle (steps are 2s each).
        seen = set()
        for _ in range(7):
            self.advance_time_and_run(1)
            texts = self._texts()
            # all four displays always show the same thing
            self.assertEqual(1, len(set(texts)), texts)
            seen.add(texts[0])

        self.assertIn(high_score, seen, 'high score step missing')
        self.assertIn('', seen, 'blank step missing')
        self.assertIn('00', seen, '00 step missing')


if __name__ == '__main__':
    unittest.main()
