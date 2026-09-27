import os
import sys
import time
import shutil
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("BDD_Assignment1")



def get_firefox_driver(headless: bool = False) -> webdriver.Firefox:

    gecko_path = os.getenv("GECKODRIVER_PATH", "/usr/bin/geckodriver")

    if not os.path.exists(gecko_path):
        gecko_path = shutil.which("geckodriver")

    if not gecko_path:
        logger.error(
            "geckodriver not found! On Arch Linux, install it using: sudo pacman -S geckodriver"
        )
        sys.exit(1)

    logger.info(f"Using geckodriver at: {gecko_path}")

    firefox_options = Options()
    if headless or os.getenv("HEADLESS", "0") == "1":
        logger.info("Running in headless mode...")
        firefox_options.add_argument("-headless")

    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.implicitly_wait(5)
    return driver

class Assignment1BDDScenario:


    def __init__(self, driver: webdriver.Firefox, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def given_i_open_url(self, url: str):
        logger.info(f"[GIVEN] Navigating to URL: {url}")
        self.driver.get(url)

    def when_page_title_contains(self, expected_title_substring: str):
        logger.info(f"[WHEN] Verifying page title contains: '{expected_title_substring}'")
        self.wait.until(EC.title_contains(expected_title_substring))
        actual_title = self.driver.title
        assert expected_title_substring in actual_title, (
            f"Expected '{expected_title_substring}' in title, got: '{actual_title}'"
        )
        logger.info(f"       Page title verified: '{actual_title}'")

    def then_page_header_equals(self, expected_header: str):
        logger.info(f"[THEN] Checking header element text equals: '{expected_header}'")
        header_el = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert header_el.text == expected_header, (
            f"Expected header '{expected_header}', but found '{header_el.text}'"
        )
        logger.info(f"       Header verified: '{header_el.text}'")

    def and_i_click_link_by_text(self, link_text: str):
        logger.info(f"[AND] Clicking link with text: '{link_text}'")
        link_el = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )
        link_el.click()

    def then_current_url_contains(self, expected_slug: str):
        logger.info(f"[THEN] Verifying current URL contains: '{expected_slug}'")
        self.wait.until(EC.url_contains(expected_slug))
        current_url = self.driver.current_url
        assert expected_slug in current_url, (
            f"Expected '{expected_slug}' in current URL: '{current_url}'"
        )
        logger.info(f"       URL verified: '{current_url}'")


def run_scenario():
    driver = None
    target_url = "https://the-internet.herokuapp.com"
    screenshot_dir = "debug_screenshots"

    try:
        driver = get_firefox_driver(headless=False)
        scenario = Assignment1BDDScenario(driver=driver, timeout=10)

        logger.info("==================================================")
        logger.info("Starting Assignment 1: Selenium BDD Scenario")
        logger.info("==================================================")

        # Execute Scenario Steps
        scenario.given_i_open_url(target_url)
        scenario.when_page_title_contains("The Internet")
        scenario.then_page_header_equals("Welcome to the-internet")
        scenario.and_i_click_link_by_text("Checkboxes")
        scenario.then_current_url_contains("/checkboxes")

        logger.info("==================================================")
        logger.info("Scenario PASSED: All BDD steps executed cleanly!")
        logger.info("==================================================")

    except (AssertionError, TimeoutException, WebDriverException) as err:
        logger.error(f"[FAILURE] Test failed: {err}")
        if driver:
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_file = os.path.join(
                screenshot_dir, f"assignment1_failure_{int(time.time())}.png"
            )
            driver.save_screenshot(screenshot_file)
            logger.error(f"[DEBUG] Failure screenshot captured at: {screenshot_file}")
        sys.exit(1)

    finally:
        if driver:
            logger.info("Tearing down Firefox session...")
            driver.quit()


if __name__ == "__main__":
    run_scenario()
