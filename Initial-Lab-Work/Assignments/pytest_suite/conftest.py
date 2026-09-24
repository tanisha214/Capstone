"""
Assignment 9: PyTest Integration with HTML Reporting
conftest.py provides shared fixtures for all test files:
 - `driver` fixture handles browser setup/teardown
 - a hook automatically attaches a screenshot to the HTML report
   whenever a test fails
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest_html


@pytest.fixture()
def driver():
    """Fixture: creates the WebDriver before each test, quits it after."""
    drv = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    drv.maximize_window()
    yield drv          # <-- test runs here
    drv.quit()          # <-- teardown, runs even if test fails


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that runs after each test step. If the test failed, capture a
    screenshot and embed it directly into the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            screenshot = driver_fixture.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, mime_type="image/png"))
    report.extra = extra
