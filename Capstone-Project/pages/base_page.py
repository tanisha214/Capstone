"""
Base Page
All Page Object classes inherit from this base class.
Provides common WebDriver interaction methods.
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException
)
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Base Page Object class.
    Encapsulates common Selenium interactions and provides
    reusable methods for all page objects.
    """

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get_explicit_wait())
        self.actions = ActionChains(driver)

    # ─────────────────────────── Navigation ───────────────────────────

    def open_url(self, url: str):
        """Navigate to a URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Return current page title"""
        title = self.driver.title
        logger.info(f"Page title: {title}")
        return title

    def get_current_url(self) -> str:
        """Return current URL"""
        return self.driver.current_url

    def go_back(self):
        """Click browser Back button"""
        self.driver.back()

    def refresh(self):
        """Refresh current page"""
        self.driver.refresh()

    # ─────────────────────────── Element Retrieval ────────────────────

    def wait_for_element(self, locator: tuple, timeout: int = None):
        """Wait for element to be visible and return it"""
        t = timeout or ConfigReader.get_explicit_wait()
        try:
            element = WebDriverWait(self.driver, t).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not visible after {t}s: {locator}")
            raise

    def wait_for_element_clickable(self, locator: tuple, timeout: int = None):
        """Wait for element to be clickable and return it"""
        t = timeout or ConfigReader.get_explicit_wait()
        try:
            element = WebDriverWait(self.driver, t).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable after {t}s: {locator}")
            raise

    def find_element(self, locator: tuple):
        """Find and return a single element"""
        return self.driver.find_element(*locator)

    def find_elements(self, locator: tuple):
        """Find and return all matching elements"""
        return self.driver.find_elements(*locator)

    def find_element_safe(self, locator: tuple):
        """
        Like find_element, but returns None instead of raising
        NoSuchElementException when the element is not found.
        """
        try:
            return self.driver.find_element(*locator)
        except Exception:
            return None

    # ─────────────────────────── Actions ──────────────────────────────

    def click(self, locator: tuple):
        """Click an element after waiting for it to be clickable"""
        element = self.wait_for_element_clickable(locator)
        logger.info(f"Clicking element: {locator}")
        element.click()

    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Type text into an input field"""
        element = self.wait_for_element(locator)
        if clear_first:
            element.clear()
        logger.info(f"Typing '{text}' into: {locator}")
        element.send_keys(text)

    def press_enter(self, locator: tuple):
        """Press Enter key on an element"""
        element = self.wait_for_element(locator)
        element.send_keys(Keys.ENTER)

    def get_text(self, locator: tuple) -> str:
        """Get text content of an element"""
        element = self.wait_for_element(locator)
        text = element.text
        logger.info(f"Element text: '{text}'")
        return text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Get attribute value of an element"""
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def scroll_to_element(self, locator: tuple):
        """Scroll element into view"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def hover_over(self, locator: tuple):
        """Hover mouse over an element"""
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()

    def js_click(self, locator: tuple):
        """Click element using JavaScript"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def wait_for_url_contains(self, partial_url: str, timeout: int = None):
        """Wait until URL contains a partial string"""
        t = timeout or ConfigReader.get_explicit_wait()
        WebDriverWait(self.driver, t).until(EC.url_contains(partial_url))

    def wait_for_text_in_element(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """Wait until element contains specific text"""
        t = timeout or ConfigReader.get_explicit_wait()
        try:
            WebDriverWait(self.driver, t).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False
