import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch Firefox
driver = webdriver.Firefox()
driver.maximize_window()

# 1. Navigate to the live testing URL
driver.get("https://demo.automationtesting.in/Frames.html")
wait = WebDriverWait(driver, 10)

# 2. Click the tab: "Iframe with in an Iframe"
nested_tab = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(text(), 'Iframe with in an Iframe')]")
))
nested_tab.click()

# 3. Switch to the outer iframe
outerframe = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//div[@id='Multiple']/iframe")
))
driver.switch_to.frame(outerframe)

# 4. Switch to the inner iframe (searched from inside the outer iframe)
innerframe = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//div[@class='iframe-container']/iframe")
))
driver.switch_to.frame(innerframe)

# 5. Locate the text box inside the nested iframe and type text
text_box = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//input[@type='text']")
))
text_box.clear()
text_box.send_keys("Automation inside nested iframe successful!")

time.sleep(3)

# 6. Exit back to the main document
# - Use driver.switch_to.parent_frame() to step back out one level
# - Use driver.switch_to.default_content() to return straight to the root page
driver.switch_to.default_content()

driver.quit()
