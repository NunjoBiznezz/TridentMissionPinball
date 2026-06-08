"""
Ruleset Original (Trident Classic) — top-level test suite.

Running this file executes all tests for the original ruleset:
    python -m unittest tests.test_ruleset_original

Individual sub-suites can also be run directly:
    python -m unittest tests.test_drop_targets
    python -m unittest tests.test_standup_targets
"""
import unittest

from tests import (test_bonus_advancement, test_drop_targets,
                   test_saucer, test_spinners, test_standup_targets)


def load_tests(loader, _tests, _pattern):
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(test_drop_targets))
    suite.addTests(loader.loadTestsFromModule(test_standup_targets))
    suite.addTests(loader.loadTestsFromModule(test_bonus_advancement))
    suite.addTests(loader.loadTestsFromModule(test_saucer))
    suite.addTests(loader.loadTestsFromModule(test_spinners))
    return suite


if __name__ == '__main__':
    unittest.main()
