"""
Fills the name/email/phone fields on testautomationpractice.blogspot.com

(Kept as its own file/name since main.py imports it, but note it no longer
needs the webdriver_manager package - see driver_setup.py for why.)
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

        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("test@example.com")
        wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys("8100129357")
        wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Yashraj Sharma")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
