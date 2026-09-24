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

        driver.execute_script("window.scrollTo({top: 800, left: 0, behavior: 'smooth'});")

        parent_menu = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point Me')]"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", parent_menu
        )

        sub_option = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Mobiles')]"))
        )

        ActionChains(driver).move_to_element(parent_menu).pause(1).move_to_element(
            sub_option
        ).pause(1).click().perform()

        print("Hovered over menu and selected Mobiles successfully.")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
