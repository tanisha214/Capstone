import os
import sys
import time
import json
import shutil
import logging
from typing import List, Dict, Any, Tuple
import requests

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
logger = logging.getLogger("BDD_Assignment2")


def get_firefox_driver(headless: bool = False) -> webdriver.Firefox:

    gecko_path = os.getenv("GECKODRIVER_PATH", "/usr/bin/geckodriver")

    if not os.path.exists(gecko_path):
        gecko_path = shutil.which("geckodriver")

    if not gecko_path:
        logger.error(
            "geckodriver not found! On Arch Linux, install via: sudo pacman -S geckodriver"
        )
        sys.exit(1)

    logger.info(f"Using geckodriver at: {gecko_path}")

    firefox_options = Options()
    if headless or os.getenv("HEADLESS", "0") == "1":
        logger.info("Running Firefox in headless mode...")
        firefox_options.add_argument("-headless")

    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.implicitly_wait(5)
    return driver


class DataDrivenLoginSuite:

    LOGIN_URL = "https://the-internet.herokuapp.com/login"

    def __init__(self, driver: webdriver.Firefox, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to_login(self):
        logger.info(f"[GIVEN] Navigating to login portal: {self.LOGIN_URL}")
        self.driver.get(self.LOGIN_URL)

    def execute_login(self, username: str, password: str):
        logger.info(f"[WHEN] Entering credentials: username='{username}'")
        username_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        submit_button.click()

    def verify_login_outcome(self, expected_status: str) -> bool:
        logger.info(f"[THEN] Verifying expected outcome: '{expected_status}'")
        flash_element = self.wait.until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        flash_text = flash_element.text

        if expected_status == "success":
            assert "You logged into a secure area!" in flash_text, (
                f"Expected success message not found. Got: {flash_text}"
            )
            logout_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.secondary.radius"))
            )
            logger.info("       Successfully authenticated to secure dashboard.")
            logout_btn.click()
            return True
        else:
            assert "Your username is invalid!" in flash_text or "invalid" in flash_text.lower(), (
                f"Expected error message not found. Got: {flash_text}"
            )
            logger.info("       Properly rejected invalid credentials with banner alert.")
            return True


class RestApiTestSuite:

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.response = None

    def given_get_endpoint(self, endpoint: str):
        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"[API GIVEN] Sending GET request to: {url}")
        self.response = requests.get(url, timeout=self.timeout)

    def given_post_endpoint(self, endpoint: str, payload: Dict[str, Any]):
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        logger.info(f"[API GIVEN] Sending POST request to: {url}")
        logger.info(f"            Payload: {json.dumps(payload)}")
        self.response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=self.timeout
        )

    def then_status_code_should_be(self, expected_status: int):
        logger.info(f"[API THEN] Verifying status code is {expected_status}")
        actual_status = self.response.status_code
        assert actual_status == expected_status, (
            f"Expected status {expected_status}, but received {actual_status}"
        )
        logger.info(f"           HTTP Status {actual_status} confirmed.")

    def then_json_field_equals(self, field_key: str, expected_val: Any):
        logger.info(f"[API AND] Checking JSON['{field_key}'] == {expected_val}")
        data = self.response.json()
        actual_val = data.get(field_key)
        assert actual_val == expected_val, (
            f"Expected {field_key} == {expected_val}, got: {actual_val}"
        )
        logger.info(f"          Field '{field_key}' matches expected value: {actual_val}")

    def then_json_contains_keys(self, required_keys: List[str]):
        logger.info(f"[API AND] Checking response contains keys: {required_keys}")
        data = self.response.json()
        for key in required_keys:
            assert key in data, f"Required key '{key}' was not returned in response: {data}"
        logger.info("          All expected JSON keys are present.")


def run_ui_data_driven_tests(driver: webdriver.Firefox):
    logger.info("==================================================")
    logger.info("Starting Assignment 2: Data-Driven UI Automation")
    logger.info("==================================================")

    test_dataset: List[Tuple[str, str, str, str]] = [
        ("tomsmith", "SuperSecretPassword!", "success", "Valid Credentials"),
        ("invalidUser", "SuperSecretPassword!", "failure", "Invalid Username"),
        ("tomsmith", "WrongPassword123!", "failure", "Invalid Password"),
        ("qa_tester", "empty_password", "failure", "Non-existent Account"),
    ]

    suite = DataDrivenLoginSuite(driver=driver, timeout=10)
    screenshot_dir = "reports/assignment2_screenshots"

    for index, (user, pwd, expected_outcome, desc) in enumerate(test_dataset, start=1):
        logger.info(f"\n--- [Iteration {index}/{len(test_dataset)}] {desc} ---")
        try:
            suite.navigate_to_login()
            suite.execute_login(username=user, password=pwd)
            suite.verify_login_outcome(expected_status=expected_outcome)
            logger.info(f"[PASS] Iteration {index} passed successfully.")
        except (AssertionError, TimeoutException, WebDriverException) as exc:
            logger.error(f"[FAIL] Iteration {index} encountered an error: {exc}")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(
                screenshot_dir, f"failure_iteration_{index}_{int(time.time())}.png"
            )
            driver.save_screenshot(screenshot_path)
            logger.error(f"[DEBUG] Captured failure screenshot: {screenshot_path}")
            raise exc


def run_api_tests():
    logger.info("\n==================================================")
    logger.info("Starting Assignment 2: REST API BDD Validations")
    logger.info("==================================================")

    api_suite = RestApiTestSuite(timeout=10)

    logger.info("\n--- [API Scenario 1] Validate GET /posts/1 ---")
    api_suite.given_get_endpoint("/posts/1")
    api_suite.then_status_code_should_be(200)
    api_suite.then_json_field_equals("id", 1)
    api_suite.then_json_field_equals("userId", 1)
    api_suite.then_json_contains_keys(["title", "body"])

    logger.info("\n--- [API Scenario 2] Validate POST /posts ---")
    new_post = {
        "title": "Arch Linux QA Automation",
        "body": "Testing Python Behave & Selenium framework",
        "userId": 99
    }
    api_suite.given_post_endpoint("/posts", payload=new_post)
    api_suite.then_status_code_should_be(201)
    api_suite.then_json_field_equals("title", "Arch Linux QA Automation")
    api_suite.then_json_field_equals("userId", 99)
    api_suite.then_json_contains_keys(["id"])


def main():
    driver = None
    try:
        driver = get_firefox_driver(headless=False)
        run_ui_data_driven_tests(driver)

        run_api_tests()

        logger.info("\n==================================================")
        logger.info("ASSIGNMENT 2 COMPLETED: All UI & API tests PASSED!")
        logger.info("==================================================")

    finally:
        if driver:
            logger.info("Cleaning up and closing Firefox session...")
            driver.quit()


if __name__ == "__main__":
    main()
