import os
import sys
import time
import shutil
import logging
from typing import Tuple, List, Optional
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("POM_Assignment3")


def get_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    gecko_path = os.getenv("GECKODRIVER_PATH", "/usr/bin/geckodriver")

    if not os.path.exists(gecko_path):
        gecko_path = shutil.which("geckodriver")

    if not gecko_path:
        logger.error("geckodriver not found! Run on Arch: sudo pacman -S geckodriver")
        sys.exit(1)

    logger.info(f"Resolved geckodriver at: {gecko_path}")

    firefox_options = Options()
    if headless or os.getenv("HEADLESS", "0") == "1":
        logger.info("Running Firefox in headless mode...")
        firefox_options.add_argument("-headless")

    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.implicitly_wait(0)
    return driver


class BasePage:

    def __init__(self, driver: webdriver.Firefox, default_timeout: int = 10):
        self.driver = driver
        self.timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)

    def open(self, url: str) -> None:
        start_time = time.time()
        logger.info(f"[PAGE NAVIGATE] Loading target URL: {url}")
        self.driver.get(url)
        elapsed = (time.time() - start_time) * 1000
        logger.info(f"[PAGE OPTIMIZATION] Page initial load finished in {elapsed:.2f}ms")

    def find(self, locator: Tuple[By, str]):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element with locator {locator} was not visible after {self.timeout}s"
        )

    def click(self, locator: Tuple[By, str]) -> None:
        element = self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element {locator} was not clickable after {self.timeout}s"
        )
        element.click()

    def type_text(self, locator: Tuple[By, str], text: str, clear_first: bool = True) -> None:
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        return self.find(locator).text.strip()

    def is_visible(self, locator: Tuple[By, str], custom_timeout: Optional[int] = None) -> bool:
        timeout = custom_timeout if custom_timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_current_url(self) -> str:
        return self.driver.current_url


class LoginPage(BasePage):
    PAGE_URL = "https://the-internet.herokuapp.com/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_ALERT    = (By.ID, "flash")
    PAGE_HEADING   = (By.TAG_NAME, "h2")

    def __init__(self, driver: webdriver.Firefox, default_timeout: int = 10):
        super().__init__(driver, default_timeout)

    def load(self) -> "LoginPage":
        self.open(self.PAGE_URL)
        self.wait.until(EC.text_to_be_present_in_element(self.PAGE_HEADING, "Login Page"))
        return self

    def enter_username(self, username: str) -> "LoginPage":
        logger.info(f"  [ACTION] Typing username: '{username}'")
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        logger.info("  [ACTION] Typing password: '***'")
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        logger.info("  [ACTION] Submitting login form")
        self.click(self.LOGIN_BUTTON)

    def login_with(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_flash_message(self) -> str:
        raw_text = self.get_text(self.FLASH_ALERT)
        clean_text = raw_text.replace("×", "").strip()
        return clean_text


class SecureAreaPage(BasePage):
    PAGE_HEADING   = (By.TAG_NAME, "h2")
    SUB_HEADER     = (By.CSS_SELECTOR, "h4.subheader")
    LOGOUT_BUTTON  = (By.CSS_SELECTOR, "a.button.secondary.radius")
    FLASH_ALERT    = (By.ID, "flash")

    def __init__(self, driver: webdriver.Firefox, default_timeout: int = 10):
        super().__init__(driver, default_timeout)

    def is_dashboard_loaded(self) -> bool:
        heading_ok = self.is_visible(self.PAGE_HEADING)
        logout_ok = self.is_visible(self.LOGOUT_BUTTON)
        return heading_ok and logout_ok

    def get_welcome_text(self) -> str:
        return self.get_text(self.SUB_HEADER)

    def get_flash_message(self) -> str:
        return self.get_text(self.FLASH_ALERT).replace("×", "").strip()

    def click_logout(self) -> LoginPage:
        logger.info("  [ACTION] Clicking Logout button to terminate session")
        self.click(self.LOGOUT_BUTTON)
        return LoginPage(self.driver, self.timeout)


@dataclass
class DiagnosticArtifacts:
    output_dir: str = "reports/assignment3_diagnostics"

    def capture_failure(self, driver: webdriver.Firefox, test_name: str, error: Exception):
        os.makedirs(self.output_dir, exist_ok=True)
        timestamp = int(time.time())
        screenshot_file = os.path.join(self.output_dir, f"{test_name}_{timestamp}.png")
        html_file = os.path.join(self.output_dir, f"{test_name}_{timestamp}.html")

        driver.save_screenshot(screenshot_file)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        logger.error(f"[DEBUG ARTIFACT] Screenshot saved to: {screenshot_file}")
        logger.error(f"[DEBUG ARTIFACT] DOM Source dump saved to: {html_file}")
        logger.error(f"[DEBUG ROOT CAUSE] Reason: {error}")


def test_valid_login_pom(driver: webdriver.Firefox, diagnostics: DiagnosticArtifacts):
    test_id = "test_valid_login_pom"
    logger.info("--------------------------------------------------")
    logger.info("[SCENARIO 1] Positive Login Flow via Page Object Model")
    logger.info("--------------------------------------------------")

    try:
        login_page = LoginPage(driver).load()
        login_page.login_with("tomsmith", "SuperSecretPassword!")

        secure_page = SecureAreaPage(driver)
        assert secure_page.is_dashboard_loaded(), "Secure dashboard elements not visible!"

        flash_msg = secure_page.get_flash_message()
        assert "You logged into a secure area!" in flash_msg, f"Unexpected flash: '{flash_msg}'"
        logger.info(f"  [VERIFY] Confirmation message verified: '{flash_msg}'")

        login_page_after_logout = secure_page.click_logout()
        assert login_page_after_logout.is_visible(LoginPage.USERNAME_INPUT), "Logout failed to return to login form!"
        logger.info("  [VERIFY] Successfully logged out back to LoginPage.")
        logger.info("[RESULT] Scenario 1 PASSED.\n")

    except Exception as exc:
        diagnostics.capture_failure(driver, test_id, exc)
        raise exc


def test_data_driven_invalid_login_pom(driver: webdriver.Firefox, diagnostics: DiagnosticArtifacts):
    test_id = "test_data_driven_invalid_login_pom"
    logger.info("--------------------------------------------------")
    logger.info("[SCENARIO 2] Data-Driven Negative Validations via POM")
    logger.info("--------------------------------------------------")

    test_matrix: List[Tuple[str, str, str]] = [
        ("invalidUser", "SuperSecretPassword!", "Your username is invalid!"),
        ("tomsmith", "WrongPassword456!", "Your password is invalid!"),
        ("", "EmptyUsernameTest!", "Your username is invalid!"),
    ]

    login_page = LoginPage(driver)

    for idx, (username, password, expected_alert) in enumerate(test_matrix, start=1):
        logger.info(f"-> Sub-test {idx}/{len(test_matrix)}: User='{username}'")
        try:
            login_page.load()
            login_page.login_with(username, password)

            actual_alert = login_page.get_flash_message()
            assert expected_alert in actual_alert, (
                f"Expected alert containing '{expected_alert}', but received '{actual_alert}'"
            )
            logger.info(f"   [VERIFY] Error Banner matched expected pattern: '{actual_alert}'")

        except Exception as exc:
            sub_id = f"{test_id}_case_{idx}"
            diagnostics.capture_failure(driver, sub_id, exc)
            raise exc

    logger.info("[RESULT] Scenario 2 PASSED.\n")


def test_sync_optimization_benchmark(driver: webdriver.Firefox):
    logger.info("--------------------------------------------------")
    logger.info("[SCENARIO 3] Explicit Wait Synchronization & Optimization Demo")
    logger.info("--------------------------------------------------")

    login_page = LoginPage(driver).load()

    start_bench = time.perf_counter()
    login_page.enter_username("tomsmith")
    login_page.enter_password("SuperSecretPassword!")
    login_page.click_login()

    secure_page = SecureAreaPage(driver)
    secure_page.wait.until(EC.visibility_of_element_located(SecureAreaPage.LOGOUT_BUTTON))
    optimized_elapsed = time.perf_counter() - start_bench

    logger.info(f"  [OPTIMIZATION METRIC] State transition completed in {optimized_elapsed:.3f}s")
    logger.info("  [INSIGHT] Explicit synchronization avoided wasteful static pauses.")
    logger.info("[RESULT] Scenario 3 PASSED.\n")


def main():
    driver = None
    diagnostics = DiagnosticArtifacts()

    logger.info("==================================================")
    logger.info("STARTING ASSIGNMENT 3: POM & OPTIMIZATION SUITE")
    logger.info("==================================================")

    try:
        driver = get_firefox_driver(headless=False)

        test_valid_login_pom(driver, diagnostics)
        test_data_driven_invalid_login_pom(driver, diagnostics)
        test_sync_optimization_benchmark(driver)

        logger.info("==================================================")
        logger.info("ASSIGNMENT 3 COMPLETED: ALL POM SCENARIOS PASSED")
        logger.info("==================================================")

    except Exception as exc:
        logger.critical(f"Suite execution aborted due to unhandled failure: {exc}")
        sys.exit(1)

    finally:
        if driver:
            logger.info("Terminating Firefox driver session cleanly...")
            driver.quit()


if __name__ == "__main__":
    main()
