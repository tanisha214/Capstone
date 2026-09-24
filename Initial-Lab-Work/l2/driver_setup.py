"""
Shared WebDriver factory (same idea as the other project's driver_setup.py).

Uses the system-installed firefox + geckodriver on PATH directly - no
webdriver_manager needed.
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_driver(headless: bool = False) -> webdriver.Firefox:
    options = FirefoxOptions()
    options.page_load_strategy = "eager"
    if headless:
        options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver
