"""
Search Results Page Object
Represents the TutorialsNinja Search Results Page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger
from typing import List

logger = get_logger(__name__)


class SearchResultsPage(BasePage):
    """Page Object for the TutorialsNinja Search Results Page"""

    # ─────────────────────── Locators ───────────────────────
    SEARCH_HEADING       = (By.CSS_SELECTOR, "div#content h1")
    PRODUCT_ITEMS        = (By.CSS_SELECTOR, "div.product-thumb")
    PRODUCT_NAMES        = (By.CSS_SELECTOR, "div.caption h4 a")
    NO_RESULT_MESSAGE    = (By.CSS_SELECTOR, "div#content p")
    PRODUCT_PRICES       = (By.CSS_SELECTOR, ".price")       # site uses <p class="price">
    LIST_VIEW_BUTTON     = (By.ID, "list-view")
    GRID_VIEW_BUTTON     = (By.ID, "grid-view")
    SORT_DROPDOWN        = (By.ID, "input-sort")
    LIMIT_DROPDOWN       = (By.ID, "input-limit")
    PAGINATION_LINKS     = (By.CSS_SELECTOR, "ul.pagination li a")
    ADD_TO_CART_BUTTONS  = (By.CSS_SELECTOR, "button[onclick*='cart.add']")

    # ─────────────────────── Actions ────────────────────────

    def get_search_heading(self) -> str:
        """Returns the search results heading text"""
        return self.get_text(self.SEARCH_HEADING)

    def get_product_count(self) -> int:
        """Returns the number of products displayed"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        count = len(products)
        logger.info(f"Found {count} products in results")
        return count

    def get_product_names(self) -> List[str]:
        """Returns list of all product names on the results page"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        names = [el.text for el in elements]
        logger.info(f"Product names: {names}")
        return names

    def is_no_result_message_displayed(self) -> bool:
        """Returns True if the 'no results' message is shown"""
        paragraphs = self.find_elements(self.NO_RESULT_MESSAGE)
        for p in paragraphs:
            if "no product" in p.text.lower() or "not found" in p.text.lower():
                return True
        return False

    def are_results_displayed(self) -> bool:
        """Returns True if at least one product result is shown"""
        return self.get_product_count() > 0

    def click_first_product(self):
        """Clicks the first product in results"""
        products = self.find_elements(self.PRODUCT_NAMES)
        if products:
            logger.info(f"Clicking first product: {products[0].text}")
            products[0].click()
        else:
            logger.warning("No products found to click")

    def product_names_contain_keyword(self, keyword: str) -> bool:
        """
        Checks if all product names contain the given keyword (case-insensitive).

        Args:
            keyword (str): Keyword to check

        Returns:
            bool: True if all names contain the keyword
        """
        names = self.get_product_names()
        if not names:
            return False
        result = all(keyword.lower() in name.lower() for name in names)
        logger.info(f"Products contain keyword '{keyword}': {result}")
        return result

    def get_prices(self) -> List[str]:
        """Returns list of all product prices"""
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [el.text for el in elements]

    def switch_to_list_view(self):
        """Switches results to list view"""
        self.click(self.LIST_VIEW_BUTTON)

    def switch_to_grid_view(self):
        """Switches results to grid view"""
        self.click(self.GRID_VIEW_BUTTON)
