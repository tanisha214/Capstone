"""
Drags the #draggable element onto #droppable on
testautomationpractice.blogspot.com
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://testautomationpractice.blogspot.com/")

        source = wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
        target = wait.until(EC.visibility_of_element_located((By.ID, "droppable")))

        ActionChains(driver).drag_and_drop(source, target).perform()

        print("Dragged and Dropped Successfully")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
