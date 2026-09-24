
from driver_setup import get_driver


def run(headless: bool = False) -> None:
    driver = get_driver(headless=headless)
    try:
        driver.get("https://www.google.com")
        print("Page title:", driver.title)
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
