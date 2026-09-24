"""
Clicks the three checkboxes on rahulshettyacademy.com/AutomationPractice/
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        for value in ("option1", "option2", "option3"):
            wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//input[@value='{value}']"))
            ).click()
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
