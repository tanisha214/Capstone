"""
Uses the Wikipedia search gadget on testautomationpractice.blogspot.com
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://testautomationpractice.blogspot.com")

        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "Wikipedia1_wikipedia-search-input"))
        )
        search_box.send_keys("English")

        search_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "wikipedia-search-button"))
        )
        search_button.click()
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
