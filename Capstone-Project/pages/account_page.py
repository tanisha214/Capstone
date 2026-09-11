"""
Account Page Object
Represents the TutorialsNinja Account Dashboard Page (post-login)
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AccountPage(BasePage):
    """Page Object for the TutorialsNinja Account Dashboard"""

    # ─────────────────────── Locators ───────────────────────
    PAGE_HEADING       = (By.CSS_SELECTOR, "div#content h2")
    ACCOUNT_LINKS      = (By.CSS_SELECTOR, "div#content ul.list-unstyled a")
    LOGOUT_LINK        = (By.LINK_TEXT, "Logout")
    MY_ACCOUNT_MENU    = (By.XPATH, "//span[text()='My Account']")
    EDIT_ACCOUNT_LINK  = (By.LINK_TEXT, "Edit Account")
    CHANGE_PWD_LINK    = (By.LINK_TEXT, "Change Password")
    ORDER_HISTORY_LINK = (By.LINK_TEXT, "Order History")
    WELCOME_MESSAGE    = (By.CSS_SELECTOR, "div#content p")

    # ─────────────────────── Actions ────────────────────────

    def is_logged_in(self) -> bool:
        """Returns True if the user is successfully logged in (account page shown)"""
        title = self.get_title()
        url = self.get_current_url()
        logged_in = "account" in url.lower() and "login" not in url.lower()
        logger.info(f"Is logged in: {logged_in} | URL: {url}")
        return logged_in

    def get_page_heading(self) -> str:
        """Returns the page heading of the account dashboard"""
        elements = self.find_elements(self.PAGE_HEADING)
        if elements:
            return elements[0].text
        return ""

    def logout(self):
        """Logs out the current user via My Account dropdown"""
        logger.info("Logging out...")
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGOUT_LINK)

    def click_edit_account(self):
        """Clicks the Edit Account link"""
        self.click(self.EDIT_ACCOUNT_LINK)

    def click_order_history(self):
        """Clicks the Order History link"""
        self.click(self.ORDER_HISTORY_LINK)
