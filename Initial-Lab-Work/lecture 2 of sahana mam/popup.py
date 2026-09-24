"""
Triggers the JS alert on testautomationpractice.blogspot.com, reads its
text, and accepts it.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://testautomationpractice.blogspot.com/")

        alert_button = wait.until(EC.element_to_be_clickable((By.ID, "alertBtn")))
        alert_button.click()

        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
