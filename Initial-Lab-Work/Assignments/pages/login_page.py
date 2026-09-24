"""
Assignment 7: Page Object Model

Login Page Object.

Contains:
- Locators
- UI interaction methods

Does not contain test assertions.
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Delay used only so the automation can be visually observed
DEMO_DELAY = 1.5


class LoginPage:

    # =====================================================
    # LOCATORS
    # =====================================================

    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # =====================================================
    # UI METHODS
    # =====================================================

    def enter_username(self, username):

        username_field = self.wait.until(
            EC.visibility_of_element_located(
                self.USERNAME_FIELD
            )
        )

        username_field.clear()

        time.sleep(DEMO_DELAY)

        if username:
            username_field.send_keys(username)

        time.sleep(DEMO_DELAY)

    def enter_password(self, password):

        password_field = self.wait.until(
            EC.visibility_of_element_located(
                self.PASSWORD_FIELD
            )
        )

        password_field.clear()

        time.sleep(DEMO_DELAY)

        if password:
            password_field.send_keys(password)

        time.sleep(DEMO_DELAY)

    def click_login(self):

        login_button = self.wait.until(
            EC.element_to_be_clickable(
                self.LOGIN_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            login_button
        )

        time.sleep(DEMO_DELAY)

        login_button.click()

        time.sleep(DEMO_DELAY)

    def login(self, username, password):

        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):

        try:

            error = self.wait.until(
                EC.visibility_of_element_located(
                    self.ERROR_MESSAGE
                )
            )

            time.sleep(DEMO_DELAY)

            return error.text

        except Exception:

            return ""

    def is_login_page_displayed(self):

        try:

            return self.wait.until(
                EC.visibility_of_element_located(
                    self.LOGIN_BUTTON
                )
            ).is_displayed()

        except Exception:

            return False