"""
Types "Germany" into the autocomplete field on
rahulshettyacademy.com/AutomationPractice/ and clicks the matching suggestion.
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

        autocomplete = wait.until(EC.presence_of_element_located((By.ID, "autocomplete")))
        autocomplete.send_keys("Germany")

        suggestion = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Germany')]"))
        )
        suggestion.click()
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
