"""
conftest.py — PyTest Configuration & Fixtures
Provides shared fixtures for all pytest tests.
Handles WebDriver setup/teardown and HTML report configuration.
"""
import pytest
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utilities.driver_factory import DriverFactory
from utilities.screenshot_util import ScreenshotUtil
from utilities.config_reader import ConfigReader
from utilities.csv_reader import CSVReader
from utilities.logger import get_logger

logger = get_logger(__name__)


# ────────────────── Command-line Options ──────────────────────

def pytest_addoption(parser):
    """Add custom CLI options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default=ConfigReader.get_browser(),
        help="Browser to use: chrome | firefox | edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=ConfigReader.get_headless(),
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=ConfigReader.get_base_url(),
        help="Base URL of the application"
    )


# ────────────────── Session Fixtures ──────────────────────────

@pytest.fixture(scope="session")
def base_url(request):
    """Returns the base URL for the test session"""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def browser_name(request):
    """Returns the browser name for the test session"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Returns headless mode setting for the test session"""
    return request.config.getoption("--headless")


# ────────────────── Function-Scope Driver Fixture ─────────────

@pytest.fixture(scope="function")
def driver(browser_name, headless_mode, base_url):
    """
    Pytest fixture: initializes WebDriver before each test
    and quits it after each test.
    """
    logger.info(f"Setting up driver for test | browser={browser_name} | headless={headless_mode}")
    drv = DriverFactory.get_driver(browser=browser_name, headless=headless_mode)
    drv.get(base_url)
    yield drv
    logger.info("Tearing down driver")
    drv.quit()


# ────────────────── Screenshot on Failure ─────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    Works with pytest-html to embed screenshots in the HTML report.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_name = item.nodeid.replace("/", "_").replace("::", "_").replace(".py", "")
            screenshot_path = ScreenshotUtil.capture_on_failure(driver, test_name)
            logger.info(f"Screenshot saved for failed test: {screenshot_path}")

            # Attach screenshot to pytest-html report
            try:
                from pytest_html import extras
                if hasattr(item, "_html_report_extras"):
                    if screenshot_path and os.path.exists(screenshot_path):
                        item._html_report_extras.append(
                            extras.image(screenshot_path)
                        )
            except ImportError:
                pass


# ────────────────── Test Data Fixtures ────────────────────────

@pytest.fixture(scope="session")
def login_test_data():
    """Provides login test data from CSV"""
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_data", "login_data.csv"
    )
    return CSVReader.read_csv(csv_path)


@pytest.fixture(scope="session")
def search_test_data():
    """Provides search test data from CSV"""
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_data", "search_data.csv"
    )
    return CSVReader.read_csv(csv_path)


# ────────────────── Parametrize Data ─────────────────────────

def get_login_params():
    """Returns login data for parametrize from CSV"""
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "test_data", "login_data.csv"
    )
    rows = CSVReader.read_csv(csv_path)
    return [(r["email"], r["password"], r["expected_result"]) for r in rows if "email" in r]


def get_search_params():
    """Returns search data for parametrize from CSV"""
    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "test_data", "search_data.csv"
    )
    rows = CSVReader.read_csv(csv_path)
    return [(r["search_term"], r["expected_result"]) for r in rows if "search_term" in r]
