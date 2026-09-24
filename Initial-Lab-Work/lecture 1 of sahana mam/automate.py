"""
Fills out the contact form on testautomationpractice.blogspot.com
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://testautomationpractice.blogspot.com/")

        wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Yashraj Sharma")
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("yashrajs118@gmail.com")
        wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys("8100129357")

        # Address textarea's id can vary between page revisions, so fall
        # back to a plain CSS "textarea" selector if the id lookup fails.
        try:
            wait.until(EC.presence_of_element_located((By.ID, "textarea"))).send_keys("Dum Dum")
        except Exception:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))).send_keys("Dum Dum")

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='male']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='sunday']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='monday']"))).click()

        country_dropdown = wait.until(EC.presence_of_element_located((By.ID, "country")))
        Select(country_dropdown).select_by_value("india")

        wait.until(EC.presence_of_element_located((By.ID, "datepicker"))).send_keys("12/15/2026")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
