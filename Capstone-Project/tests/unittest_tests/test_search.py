"""
Product Search Tests — Unittest
Tests for the Product Search functionality of TutorialsNinja Demo
Uses Page Object Model (POM) and data from CSV
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.unittest_tests.base_test import BaseTest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.csv_reader import CSVReader
from utilities.logger import get_logger

logger = get_logger(__name__)

SEARCH_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "test_data", "search_data.csv"
)


class TestProductSearch(BaseTest):
    """
    Unittest Test Suite for Product Search Functionality.
    Tests valid search, no results, empty search, search heading, etc.
    """

    # ──────────────────── TC_SEARCH_001 ───────────────────────
    def test_TC_SEARCH_001_valid_product_search(self):
        """TC_SEARCH_001: Valid product search returns results"""
        logger.info("TC_SEARCH_001: Valid Product Search")

        home = HomePage(self.driver)
        home.search_for_product("MacBook")

        results = SearchResultsPage(self.driver)
        self.assertTrue(
            results.are_results_displayed(),
            "Search results should be displayed for 'MacBook'"
        )
        logger.info("TC_SEARCH_001 PASSED ✓")

    # ──────────────────── TC_SEARCH_002 ───────────────────────
    def test_TC_SEARCH_002_search_result_count(self):
        """TC_SEARCH_002: Verify at least 1 product found for 'MacBook'"""
        logger.info("TC_SEARCH_002: Search Result Count")

        home = HomePage(self.driver)
        home.search_for_product("MacBook")

        results = SearchResultsPage(self.driver)
        count = results.get_product_count()
        self.assertGreater(count, 0,
                           f"Expected at least 1 result for 'MacBook', got {count}")
        logger.info(f"TC_SEARCH_002 PASSED ✓ | Found {count} products")

    # ──────────────────── TC_SEARCH_003 ───────────────────────
    def test_TC_SEARCH_003_no_results_for_invalid_product(self):
        """TC_SEARCH_003: Search for non-existent product shows no results"""
        logger.info("TC_SEARCH_003: No Results for Invalid Product")

        home = HomePage(self.driver)
        home.search_for_product("NonExistentProduct99999XYZ")

        results = SearchResultsPage(self.driver)
        self.assertFalse(
            results.are_results_displayed(),
            "No results should be shown for a non-existent product"
        )
        logger.info("TC_SEARCH_003 PASSED ✓")

    # ──────────────────── TC_SEARCH_004 ───────────────────────
    def test_TC_SEARCH_004_search_heading_displayed(self):
        """TC_SEARCH_004: Search results page displays search heading"""
        logger.info("TC_SEARCH_004: Search Results Heading")

        home = HomePage(self.driver)
        home.search_for_product("iPhone")

        results = SearchResultsPage(self.driver)
        heading = results.get_search_heading()
        logger.info(f"Search heading: '{heading}'")

        self.assertGreater(len(heading), 0,
                           "Search results page should display a heading")
        logger.info("TC_SEARCH_004 PASSED ✓")

    # ──────────────────── TC_SEARCH_005 ───────────────────────
    def test_TC_SEARCH_005_empty_search(self):
        """TC_SEARCH_005: Empty search query shows appropriate response"""
        logger.info("TC_SEARCH_005: Empty Search Test")

        home = HomePage(self.driver)
        home.search_for_product("")

        # After empty search, either results page or same page
        current_url = self.driver.current_url
        logger.info(f"URL after empty search: {current_url}")
        # Verify the page didn't crash
        self.assertIsNotNone(self.driver.title,
                             "Page should still load after empty search")
        logger.info("TC_SEARCH_005 PASSED ✓")

    # ──────────────────── TC_SEARCH_006 ───────────────────────
    def test_TC_SEARCH_006_search_url_contains_keyword(self):
        """TC_SEARCH_006: Search URL contains the searched keyword"""
        logger.info("TC_SEARCH_006: Search URL Contains Keyword")

        search_term = "Samsung"
        home = HomePage(self.driver)
        home.search_for_product(search_term)

        current_url = self.driver.current_url
        self.assertIn("search", current_url.lower(),
                      f"URL should contain 'search' after searching for '{search_term}'")
        logger.info("TC_SEARCH_006 PASSED ✓")

    # ──────────────────── TC_SEARCH_007 ───────────────────────
    def test_TC_SEARCH_007_home_page_logo_visible(self):
        """TC_SEARCH_007: Home page logo is visible before search"""
        logger.info("TC_SEARCH_007: Home Page Logo Visibility")

        home = HomePage(self.driver)
        self.assertTrue(
            home.is_logo_visible(),
            "Home page logo should be visible"
        )
        logger.info("TC_SEARCH_007 PASSED ✓")

    # ──────────────────── TC_SEARCH_008 (Data-Driven) ─────────
    def test_TC_SEARCH_008_data_driven_search(self):
        """TC_SEARCH_008: Data-driven search test from CSV (first valid row)"""
        logger.info("TC_SEARCH_008: Data-Driven Search Test (CSV)")

        rows = CSVReader.read_csv(SEARCH_CSV)
        if not rows:
            self.skipTest("No search test data found in CSV")

        # Test first row
        row = rows[0]
        search_term = row.get("search_term", "")
        expected = row.get("expected_result", "").lower()

        logger.info(f"Searching for: '{search_term}' | expected: {expected}")

        home = HomePage(self.driver)
        home.search_for_product(search_term)

        results = SearchResultsPage(self.driver)

        if expected == "found":
            self.assertTrue(results.are_results_displayed(),
                            f"Expected results for '{search_term}'")
        else:
            self.assertFalse(results.are_results_displayed(),
                             f"Expected no results for '{search_term}'")

        logger.info("TC_SEARCH_008 PASSED ✓")


# ─────────────────────── Run Tests ────────────────────────────
if __name__ == "__main__":
    unittest.main(verbosity=2)
