"""
Scrolls to the bottom of text-compare.com and clicks the "About" link.

Renamed from "scroll&click_About.py" - a filename with '&' can't be
imported as a Python module (`import scroll&click_About` is a syntax
error), which is exactly why this script was silently left out of main.py.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://text-compare.com/")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        about = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "About")))
        print("About link found:", about.text)
        about.click()
        print("About link clicked successfully!")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
