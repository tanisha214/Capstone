from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://rahulshettyacademy.com/AutomationPractice/")

        dropdown_elem = wait.until(
            EC.presence_of_element_located((By.ID, "dropdown-class-example"))
        )
        select = Select(dropdown_elem)

        for value in ("option1", "option2", "option3"):
            select.select_by_value(value)
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
