"""
Shared WebDriver factory.

This machine already has firefox + geckodriver installed system-wide and on
PATH (confirmed via `which firefox` / `which geckodriver`), so there is no
need for webdriver_manager at all. webdriver_manager tries to detect your OS
and download a matching geckodriver binary from GitHub every run, which is
exactly what was failing on Arch (network/arch-detection issues, and it's
redundant work when the driver is already installed).

Selenium 4.6+ can find `firefox`/`geckodriver` on PATH by itself, so
`webdriver.Firefox()` with no service/executable_path is all that's needed.
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_driver(headless: bool = False) -> webdriver.Firefox:
    """Create a Firefox WebDriver using the system firefox + geckodriver.

    Args:
        headless: run without a visible window (useful for CI / running
            many scripts back-to-back without a bunch of windows popping up).
    """
    options = FirefoxOptions()
    # 'eager' returns control once the DOM is ready, without waiting on
    # every image/ad/script to finish loading -> much faster on heavy pages.
    options.page_load_strategy = "eager"
    if headless:
        options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver
