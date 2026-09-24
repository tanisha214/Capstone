# 1. send_keys()
# 2. key_down()
# 3. key_up()
# 4. perform()
# 5. release()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://text-compare.com/")

        # Some sites show a cookie-consent banner that silently eats the
        # first interaction. Try to dismiss anything obvious before
        # proceeding, but don't fail the script if there isn't one.
        try:
            consent_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(translate(text(),'ACEPT','acept'),'accept') "
                    "or contains(text(),'Accept') or contains(text(),'Agree')]",
                ))
            )
            consent_btn.click()
            print("Dismissed a consent banner.")
        except Exception:
            print("No consent banner found (or it wasn't blocking) - continuing.")

        left_textbox = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[@id='inputText1']"))
        )

        left_textbox.clear()
        left_textbox.send_keys("Welcome to Selennium")

        actual_value = left_textbox.get_attribute("value")
        print("Textbox now contains:", repr(actual_value))
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
