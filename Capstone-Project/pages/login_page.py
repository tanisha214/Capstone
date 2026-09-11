"""
Login Page Object
Represents the TutorialsNinja Login Page
URL: https://tutorialsninja.com/demo/index.php?route=account/login
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Page Object for the TutorialsNinja Login Page"""

    # ─────────────────────── Locators ───────────────────────
    EMAIL_INPUT                  = (By.ID, "input-email")
    PASSWORD_INPUT               = (By.ID, "input-password")
    LOGIN_BUTTON                 = (By.CSS_SELECTOR, "input[value='Login']")
    FORGOTTEN_LINK               = (By.LINK_TEXT, "Forgotten Password")
    ERROR_ALERT                  = (By.CSS_SELECTOR, "div.alert.alert-danger")
    PAGE_HEADING                 = (By.CSS_SELECTOR, "div#content h2")
    RETURNING_CUSTOMER_HEADING   = (By.XPATH, "//div[@id='content']//h2[contains(text(),'Returning Customer')]")
    REGISTER_BUTTON              = (By.LINK_TEXT, "Continue")
    BREADCRUMB                   = (By.CSS_SELECTOR, "ul.breadcrumb")

    # ─────────────────────── Actions ────────────────────────

    def enter_email(self, email: str):
        """Enters email into the email input field"""
        logger.info(f"Entering email: {email}")
        self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        """Enters password into the password input field"""
        logger.info("Entering password: [HIDDEN]")
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Clicks the Login button"""
        logger.info("Clicking Login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """
        Performs complete login flow.

        Args:
            email (str): User email address
            password (str): User password
        """
        logger.info(f"Performing login for: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """Returns error alert text if login fails"""
        if self.is_element_visible(self.ERROR_ALERT, timeout=5):
            return self.get_text(self.ERROR_ALERT)
        return ""

    def is_login_error_displayed(self) -> bool:
        """Returns True if a login error alert is shown"""
        return self.is_element_visible(self.ERROR_ALERT, timeout=5)

    def get_page_heading(self) -> str:
        """
        Returns the 'Returning Customer' heading from the login page.
        Uses a direct XPath locator targeting the exact text,
        avoiding confusion with the 'New Customer' heading also on the page.
        """
        el = self.find_element_safe(self.RETURNING_CUSTOMER_HEADING)
        if el:
            return el.text
        # Fallback: scan all h2 elements
        elements = self.find_elements(self.PAGE_HEADING)
        for e in elements:
            if "returning" in e.text.lower():
                return e.text
        return " | ".join(e.text for e in elements) if elements else ""


    def click_forgotten_password(self):
        """Clicks the Forgotten Password link"""
        self.click(self.FORGOTTEN_LINK)
