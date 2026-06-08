import os

from mpf.tests.MpfGameTestCase import MpfGameTestCase


class RulesetTestBase(MpfGameTestCase):
    """Shared setup for all ruleset_original tests."""

    def get_config_file(self):
        return 'config_dev.yaml'

    def get_absolute_machine_path(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def get_platform(self):
        return 'smart_virtual'

    def _start_game_original(self):
        """Start a one-player game and confirm ruleset_original is active."""
        self.fill_troughs()
        self.start_game()
        self.advance_time_and_run(1)
        self.assertTrue(
            self.machine.mode_controller.is_active('ruleset_original'),
            'ruleset_original should be active (current_ruleset defaults to 1)',
        )
