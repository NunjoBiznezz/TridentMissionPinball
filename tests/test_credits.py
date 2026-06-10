import unittest

from tests.base import RulesetTestBase


class TestCredits(RulesetTestBase):
    """Coins must be accepted at any time (attract or mid-game),
    up to machine.max_credits."""

    def _insert_coin(self):
        self.hit_and_release_switch('s_coin_1')
        self.advance_time_and_run(0.1)

    def _credits(self):
        return self.machine.variables.get_machine_var('credits')

    def test_credits_in_attract(self):
        self.assertEqual(0, self._credits())
        self._insert_coin()
        self.assertEqual(1, self._credits())
        self._insert_coin()
        self.assertEqual(2, self._credits())

    def test_credits_during_game(self):
        self._insert_coin()
        self._insert_coin()
        self.assertEqual(2, self._credits())

        self._start_game_original()
        # game start consumed one credit
        self.assertEqual(1, self._credits())

        self._insert_coin()
        self.assertEqual(2, self._credits(),
                         'coin during an active game must add a credit')

    def test_credits_capped_at_max(self):
        max_credits = self.machine.variables.get_machine_var('max_credits')
        for _ in range(max_credits + 3):
            self._insert_coin()
        self.assertEqual(max_credits, self._credits())


if __name__ == '__main__':
    unittest.main()
