"""
LoginPage - Page Object for the SauceDemo login screen.
Contains ONLY locators and UI interaction methods. No assertions here.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # ---------- Locators ----------
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- Actions ----------
    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username):
        field = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password):
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)
        return self

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        return self

    def login(self, username, password):
        """Convenience method combining the full login flow."""
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text
        except Exception:
            return None
