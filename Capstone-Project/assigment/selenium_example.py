from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.binary_location = "/usr/bin/firefox"

service = Service("/usr/bin/geckodriver")

driver = webdriver.Firefox(
    service=service,
    options=options
)

try:
    driver.get("https://example.com")

    print("Page Title:", driver.title)
    print("Current URL:", driver.current_url)

finally:
    input("Press Enter to close...")
    driver.quit()
