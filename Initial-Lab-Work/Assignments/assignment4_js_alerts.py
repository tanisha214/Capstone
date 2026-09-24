"""
Assignment 4: JavaScript Alerts and Confirms
Accept a plain alert, dismiss a confirm box, and send text into a prompt
box before submitting.

Delays added throughout purely for video demonstration pacing - so each
popup is clearly visible before the next action fires.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.selenium.dev/selenium/web/alerts.html")
    driver.maximize_window()
    time.sleep(2)  # let the page settle so viewers see it before anything happens

    # ---------- 1. Simple ALERT ----------
    print("About to trigger a simple Alert...")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#alert").click()

    wait.until(EC.alert_is_present())
    time.sleep(2)  # let the alert sit on screen so it's clearly visible

    alert = driver.switch_to.alert
    print(f"Alert text: {alert.text}")
    time.sleep(2)  # pause with alert still open, showing the text just printed

    alert.accept()  # ACCEPT the alert
    print("Alert accepted.\n")
    time.sleep(2)  # pause after alert closes before moving to the next popup

    # ---------- 2. CONFIRM box ----------
    print("About to trigger a Confirm box...")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#confirm").click()

    wait.until(EC.alert_is_present())
    time.sleep(2)  # let the confirm box sit on screen

    confirm_alert = driver.switch_to.alert
    print(f"Confirm text: {confirm_alert.text}")
    time.sleep(2)  # pause with confirm still open

    confirm_alert.dismiss()  # DISMISS (click Cancel)
    print("Confirm box dismissed.\n")
    time.sleep(2)  # pause after confirm closes

    # ---------- 3. PROMPT box ----------
    print("About to trigger a Prompt box...")
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#prompt").click()

    wait.until(EC.alert_is_present())
    time.sleep(2)  # let the prompt sit on screen, empty, before typing

    prompt_alert = driver.switch_to.alert
    print(f"Prompt text: {prompt_alert.text}")
    time.sleep(1)

    prompt_alert.send_keys("Yashraj Sharma")   # Enter text into the prompt
    time.sleep(2)  # pause so viewers can see the typed text inside the prompt

    prompt_alert.accept()                       # Submit it
    print("Prompt filled with text and submitted.\n")
    time.sleep(2)  # pause after prompt closes, before checking the page

    # Verify the result text on the page reflects our input
    result = driver.find_element(By.CSS_SELECTOR, "#text").text
    print(f"Result on page: {result}")
    assert "Yashraj Sharma" in result, "Prompt text was not reflected on page!"
    print("PASS: Prompt value verified on page.")

    time.sleep(3)  # final pause showing the verified result on the page

except Exception as e:
    print(f"ERROR: {e}")
finally:
    driver.quit()