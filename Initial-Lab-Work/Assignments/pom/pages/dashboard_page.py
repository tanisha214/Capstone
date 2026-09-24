"""
DashboardPage - Page Object for the SauceDemo inventory/dashboard screen.
Contains ONLY locators and UI interaction methods. No assertions here.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        return "/inventory.html" in self.driver.current_url

    def get_page_title_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        return element.text

    def get_item_count(self):
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(items)

    def logout(self):
        self.driver.find_element(*self.MENU_BUTTON).click()
        logout_link = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        logout_link.click()
        return self
