"""
Test Suite Runner — Unittest
Discovers and runs all unittest tests.
Generates an HTML report using pytest-html (avoids HtmlTestRunner
which is broken on Python 3.14 due to missing _count_relevant_tb_levels).
"""
import sys
import os
import unittest
import subprocess
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_all_tests_via_pytest():
    """
    Runs the unittest test files via pytest.
    Pytest fully supports unittest.TestCase classes and generates
    a proper HTML report without the HtmlTestRunner Python 3.14 bug.
    """
    report_dir = ConfigReader.get_report_dir()
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(ConfigReader.get_screenshot_dir(), exist_ok=True)

    unittest_dir = os.path.join(_PROJECT_ROOT, "tests", "unittest_tests")
    report_path  = os.path.join(report_dir, "unittest_report.html")

    logger.info(f"{'='*60}")
    logger.info("Starting Unittest Test Suite Runner (via pytest)")
    logger.info(f"Test Directory : {unittest_dir}")
    logger.info(f"HTML Report    : {report_path}")
    logger.info(f"{'='*60}")

    cmd = [
        sys.executable, "-m", "pytest",
        unittest_dir,
        "-v",
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        "--no-header",
    ]

    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=_PROJECT_ROOT)

    logger.info(f"\n{'='*60}")
    logger.info(f"Exit code : {result.returncode}")
    logger.info(f"HTML report saved → {report_path}")
    logger.info(f"{'='*60}")

    return result.returncode


def run_all_tests_textrunner():
    """
    Fallback: runs unittest tests with plain TextTestRunner
    (no HTML report, but guaranteed to work on any Python version).
    """
    test_dir = os.path.join(_PROJECT_ROOT, "tests", "unittest_tests")
    loader   = unittest.TestLoader()
    suite    = loader.discover(start_dir=test_dir, pattern="test_*.py")

    logger.info("Running with TextTestRunner (fallback mode)")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    logger.info(f"Tests Run : {result.testsRun}")
    logger.info(f"Failures  : {len(result.failures)}")
    logger.info(f"Errors    : {len(result.errors)}")
    return result


if __name__ == "__main__":
    exit_code = run_all_tests_via_pytest()
    sys.exit(exit_code)
