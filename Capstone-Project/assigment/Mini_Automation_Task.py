import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)

BASE_URL = "https://the-internet.herokuapp.com"


def main():
    driver = webdriver.Firefox()
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    try:
        # -----------------------------
        # Verify main page
        # -----------------------------
        driver.get(BASE_URL)

        assert "The Internet" in driver.title, (
            f"Unexpected page title: {driver.title}"
        )

        print(f"Title verified: {driver.title}")

        time.sleep(1.5)

        # -----------------------------
        # Number input
        # -----------------------------
        driver.get(f"{BASE_URL}/inputs")
        print("Navigating to /inputs ...")

        number_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='number']")
            )
        )

        number_input.send_keys("42")

        print("Entered value into number input.")

        driver.save_screenshot("1_number_input.png")
        print("Screenshot saved as 1_number_input.png")

        time.sleep(1.5)

        # -----------------------------
        # Checkbox
        # -----------------------------
        driver.get(f"{BASE_URL}/checkboxes")
        print("Navigating to /checkboxes ...")

        checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//input[@type='checkbox'])[1]")
            )
        )

        was_checked_before = checkbox.is_selected()

        checkbox.click()

        assert checkbox.is_selected() != was_checked_before, (
            "Checkbox state did not change"
        )

        print("Checkbox toggled successfully.")

        driver.save_screenshot("2_checkbox.png")
        print("Screenshot saved as 2_checkbox.png")

        time.sleep(1.5)

        # -----------------------------
        # Dropdown
        # -----------------------------
        driver.get(f"{BASE_URL}/dropdown")
        print("Navigating to /dropdown ...")

        dropdown_el = wait.until(
            EC.presence_of_element_located(
                (By.ID, "dropdown")
            )
        )

        Select(dropdown_el).select_by_visible_text("Option 2")

        print("Dropdown option selected.")

        time.sleep(1.5)

        driver.save_screenshot("3_dropdown.png")
        print("Screenshot saved as 3_dropdown.png")

        time.sleep(1.5)

        # -----------------------------
        # Expected failure
        # -----------------------------
        try:
            wait_short = WebDriverWait(driver, 5)

            missing_el = wait_short.until(
                EC.presence_of_element_located(
                    (By.ID, "this-id-does-not-exist")
                )
            )

            missing_el.click()

        except (NoSuchElementException, TimeoutException) as e:
            print(
                "Expected failure handled: could not find element "
                "'#this-id-does-not-exist' on the Dropdown page. "
                f"Original error type: {type(e).__name__}"
            )

    finally:
        driver.quit()
        print("Browser session closed safely.")


if __name__ == "__main__":
    main()