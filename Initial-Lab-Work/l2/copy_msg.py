"""
Types text into the left textarea on text-compare.com, selects it,
copies it (Ctrl+C), pastes it into the right textarea (Ctrl+V), and
verifies the paste actually landed.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://text-compare.com/")

        left_text = wait.until(EC.visibility_of_element_located((By.XPATH, "(//textarea)[1]")))
        left_text.send_keys("Selenium Keyboard Actions")

        right_text = wait.until(EC.visibility_of_element_located((By.XPATH, "(//textarea)[2]")))

        act = ActionChains(driver)
        act.click(left_text)
        act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
        act.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL)
        act.click(right_text)
        act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL)
        act.perform()

        # Poll instead of a flat sleep - waits only as long as actually needed
        wait.until(lambda d: right_text.get_attribute("value") != "")
        print("Right textbox now contains:", right_text.get_attribute("value"))
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
