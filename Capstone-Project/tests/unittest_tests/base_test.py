"""
Base Test Class (Unittest)
All unittest test classes inherit from this base class.
Handles WebDriver lifecycle and screenshot on failure.
"""
import unittest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.driver_factory import DriverFactory
from utilities.screenshot_util import ScreenshotUtil
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)


class BaseTest(unittest.TestCase):
    """
    Base test class for all Unittest-based tests.
    Provides setUp and tearDown with automatic screenshot on failure.

    Compatible with both:
      - Standard `python -m unittest` runner
      - Pytest runner (which wraps unittest.TestCase differently)
    """

    driver = None

    @classmethod
    def setUpClass(cls):
        """Called once before all tests in the class"""
        logger.info(f"{'='*60}")
        logger.info(f"Starting Test Class: {cls.__name__}")
        logger.info(f"{'='*60}")

    @classmethod
    def tearDownClass(cls):
        """Called once after all tests in the class"""
        logger.info(f"{'='*60}")
        logger.info(f"Finished Test Class: {cls.__name__}")
        logger.info(f"{'='*60}")

    def setUp(self):
        """Called before each test method — initializes driver"""
        logger.info(f"\n--- Starting Test: {self._testMethodName} ---")
        self.driver = DriverFactory.get_driver()
        self.driver.get(ConfigReader.get_base_url())

    def tearDown(self):
        """
        Called after each test method.
        - Detects failures/errors in a way that works under both
          the standard unittest runner AND pytest's unittest wrapper.
        - Captures a screenshot if the test failed.
        - Always quits the driver.
        """
        test_failed = self._detect_failure()

        if test_failed:
            logger.warning(f"Test FAILED: {self._testMethodName}")
            if self.driver:
                ScreenshotUtil.capture_on_failure(self.driver, self._testMethodName)
        else:
            logger.info(f"Test PASSED: {self._testMethodName}")

        if self.driver:
            self.driver.quit()
            logger.info("Driver closed.")

    # ─────────────────────── Helpers ──────────────────────────

    def _detect_failure(self) -> bool:
        """
        Returns True if the current test has failed or errored.

        Handles two execution contexts:
        1. Standard unittest runner  → result has .errors / .failures lists
        2. Pytest runner             → result is a TestCaseFunction;
                                       use self._outcome.success instead
        """
        try:
            outcome = self._outcome          # available in Python 3.4+

            # ── Pytest path: outcome.result is a pytest TestCaseFunction ──
            # pytest sets outcome.success = False when the test fails.
            if hasattr(outcome, 'success'):
                return not outcome.success

            # ── Standard unittest path ────────────────────────────────────
            result = outcome.result
            if hasattr(result, 'errors') and hasattr(result, 'failures'):
                errors   = [e for e in result.errors   if e[0] is self]
                failures = [f for f in result.failures if f[0] is self]
                return bool(errors or failures)

        except AttributeError:
            pass  # Unexpected runner — assume passed to avoid noise

        return False
