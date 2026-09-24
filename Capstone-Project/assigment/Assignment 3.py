from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://rahulshettyacademy.com/AutomationPractice/"


def main():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    # Starts with: [id^='...']
    checkboxes = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[id^='checkBoxOption']")
        )
    )

    print(
        "Found",
        len(checkboxes),
        "checkboxes via [id^='checkBoxOption']"
    )

    for cb in checkboxes:
        cb.click()
        print(
            "  Clicked",
            cb.get_attribute("id"),
            "-> checked =",
            cb.is_selected()
        )

    # Contains: [id*='...']
    contains_match = driver.find_elements(
        By.CSS_SELECTOR,
        "[id*='BoxOption']"
    )

    print(
        "Found",
        len(contains_match),
        "elements via [id*='BoxOption']"
    )

    # Ends with: [id$='...']
    ends_with_match = driver.find_element(
        By.CSS_SELECTOR,
        "[id$='Option3']"
    )

    print(
        "Ends-with match id:",
        ends_with_match.get_attribute("id")
    )

    # Starts with: [name^='...']
    radio_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "[name^='radioButton']"
    )

    print(
        "Found",
        len(radio_buttons),
        "radio buttons via [name^='radioButton']"
    )

    if radio_buttons:
        radio_buttons[0].click()

    driver.quit()


if __name__ == "__main__":
    main()
