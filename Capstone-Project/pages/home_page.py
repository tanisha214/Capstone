"""
Home Page Object
Represents the TutorialsNinja Demo Home Page
URL: https://tutorialsninja.com/demo/
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Page Object for the TutorialsNinja Home Page"""

    # ─────────────────────── Locators ───────────────────────
    SEARCH_BOX        = (By.NAME, "search")
    SEARCH_BUTTON     = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    MY_ACCOUNT_MENU   = (By.XPATH, "//span[text()='My Account']")
    LOGIN_LINK        = (By.LINK_TEXT, "Login")
    REGISTER_LINK     = (By.LINK_TEXT, "Register")
    LOGO              = (By.ID, "logo")
    CART_BUTTON       = (By.ID, "cart")
    NAV_MENU          = (By.CSS_SELECTOR, "nav#menu")

    # ─────────────────────── Actions ────────────────────────

    def search_for_product(self, product_name: str):
        """
        Enters a search term and clicks the search button.

        Args:
            product_name (str): Product to search for
        """
        logger.info(f"Searching for product: '{product_name}'")
        self.type_text(self.SEARCH_BOX, product_name)
        self.click(self.SEARCH_BUTTON)

    def navigate_to_login(self):
        """Navigates to the Login page via My Account dropdown"""
        logger.info("Navigating to Login page via My Account menu")
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.LOGIN_LINK)

    def navigate_to_register(self):
        """Navigates to the Register page via My Account dropdown"""
        logger.info("Navigating to Register page via My Account menu")
        self.click(self.MY_ACCOUNT_MENU)
        self.click(self.REGISTER_LINK)

    def is_logo_visible(self) -> bool:
        """Checks if the site logo is displayed"""
        return self.is_element_visible(self.LOGO)

    def get_search_box_placeholder(self) -> str:
        """Returns the placeholder text of the search box"""
        return self.get_attribute(self.SEARCH_BOX, "placeholder")
