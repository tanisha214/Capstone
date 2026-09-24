"""
Assignment 9: PyTest Integration

Contains:
1. Selenium WebDriver fixture
2. Browser setup and teardown
3. Automatic screenshot capture on failure
"""

import time

import pytest
import pytest_html

from selenium import webdriver


DEMO_DELAY = 2


# =========================================================
# WEB DRIVER FIXTURE
# =========================================================

@pytest.fixture
def driver():

    # -----------------------------------------------------
    # SETUP
    # -----------------------------------------------------

    driver = webdriver.Chrome()

    driver.maximize_window()

    time.sleep(DEMO_DELAY)

    driver.get(
        "https://www.saucedemo.com/"
    )

    time.sleep(DEMO_DELAY)

    # Give driver to test
    yield driver

    # -----------------------------------------------------
    # TEARDOWN
    # -----------------------------------------------------

    # Keep browser open briefly so the final state
    # can be observed during training/demo execution.
    time.sleep(DEMO_DELAY)

    driver.quit()


# =========================================================
# SCREENSHOT ON FAILURE
# =========================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when != "call":
        return

    if not report.failed:
        return

    driver = item.funcargs.get("driver")

    if driver is None:
        return

    try:

        screenshot = driver.get_screenshot_as_base64()

        pytest_html_plugin = (
            item.config.pluginmanager.getplugin("html")
        )

        if pytest_html_plugin is None:
            return

        extras = getattr(report, "extras", [])

        extras.append(
            pytest_html_plugin.extras.image(
                screenshot,
                mime_type="image/png",
                extension="png",
                name="Failure Screenshot"
            )
        )

        report.extras = extras

    except Exception as e:

        print(
            f"\nScreenshot capture failed: {e}"
        )


# =========================================================
# HTML REPORT TITLE
# =========================================================

def pytest_html_report_title(report):

    report.title = "Selenium Automation Test Report"