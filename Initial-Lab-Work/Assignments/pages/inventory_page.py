"""
Assignment 7: Page Object Model

Inventory Page Object.
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DEMO_DELAY = 2


class InventoryPage:

    # =====================================================
    # LOCATORS
    # =====================================================

    INVENTORY_CONTAINER = (
        By.ID,
        "inventory_container"
    )

    PAGE_TITLE = (
        By.CLASS_NAME,
        "title"
    )

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # =====================================================
    # PAGE METHODS
    # =====================================================

    def is_inventory_page_displayed(self):

        try:

            inventory = self.wait.until(
                EC.visibility_of_element_located(
                    self.INVENTORY_CONTAINER
                )
            )

            time.sleep(DEMO_DELAY)

            return inventory.is_displayed()

        except Exception:

            return False

    def get_page_title(self):

        try:

            title = self.wait.until(
                EC.visibility_of_element_located(
                    self.PAGE_TITLE
                )
            )

            time.sleep(DEMO_DELAY)

            return title.text

        except Exception:

            return ""