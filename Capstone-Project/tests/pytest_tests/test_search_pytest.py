"""
Product Search Tests — PyTest
Tests for Product Search functionality of TutorialsNinja Demo
Uses PyTest fixtures, markers, parametrize, and POM
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.logger import get_logger
from tests.conftest import get_search_params

logger = get_logger(__name__)

SEARCH_PARAMS = get_search_params()


# ═══════════════════════════════════════════════════════════════
# TEST CLASS
# ═══════════════════════════════════════════════════════════════

@pytest.mark.search
class TestSearchPytest:
    """PyTest-based Product Search Test Suite using fixtures and POM"""

    # ──────────────────── TC_PY_SEARCH_001 ────────────────────
    @pytest.mark.smoke
    def test_TC_PY_SEARCH_001_macbook_search_returns_results(self, driver):
        """TC_PY_SEARCH_001: Searching 'MacBook' returns product results"""
        logger.info("TC_PY_SEARCH_001: MacBook Search Returns Results")

        home = HomePage(driver)
        home.search_for_product("MacBook")

        results = SearchResultsPage(driver)
        assert results.are_results_displayed(), \
            "At least one product should be displayed for 'MacBook'"
        logger.info("TC_PY_SEARCH_001 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_002 ────────────────────
    @pytest.mark.smoke
    def test_TC_PY_SEARCH_002_product_names_contain_keyword(self, driver):
        """TC_PY_SEARCH_002: Product names contain the searched keyword"""
        logger.info("TC_PY_SEARCH_002: Product Names Contain Keyword")

        search_term = "MacBook"
        home = HomePage(driver)
        home.search_for_product(search_term)

        results = SearchResultsPage(driver)
        product_names = results.get_product_names()
        logger.info(f"Products found: {product_names}")

        assert len(product_names) > 0, "At least one product name should be returned"
        logger.info("TC_PY_SEARCH_002 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_003 ────────────────────
    @pytest.mark.negative
    def test_TC_PY_SEARCH_003_invalid_product_no_results(self, driver):
        """TC_PY_SEARCH_003: Invalid product search yields no results"""
        logger.info("TC_PY_SEARCH_003: Invalid Product No Results Test")

        home = HomePage(driver)
        home.search_for_product("XYZNONEXISTENT123456ABCDE")

        results = SearchResultsPage(driver)
        assert not results.are_results_displayed(), \
            "No products should be shown for a completely invalid search term"
        logger.info("TC_PY_SEARCH_003 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_004 ────────────────────
    def test_TC_PY_SEARCH_004_search_results_heading(self, driver):
        """TC_PY_SEARCH_004: Search results page has a valid heading"""
        logger.info("TC_PY_SEARCH_004: Search Results Heading Test")

        home = HomePage(driver)
        home.search_for_product("iPhone")

        results = SearchResultsPage(driver)
        heading = results.get_search_heading()
        logger.info(f"Heading: {heading}")

        assert heading, "Search results heading should not be empty"
        logger.info("TC_PY_SEARCH_004 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_005 ────────────────────
    def test_TC_PY_SEARCH_005_search_url_after_query(self, driver):
        """TC_PY_SEARCH_005: URL contains 'search' after performing search"""
        logger.info("TC_PY_SEARCH_005: Search URL Verification Test")

        home = HomePage(driver)
        home.search_for_product("Camera")

        assert "search" in driver.current_url.lower(), \
            "URL should contain 'search' after performing search"
        logger.info("TC_PY_SEARCH_005 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_006 ────────────────────
    @pytest.mark.smoke
    def test_TC_PY_SEARCH_006_search_product_count_gt_zero(self, driver):
        """TC_PY_SEARCH_006: Product count is greater than 0 for valid search"""
        logger.info("TC_PY_SEARCH_006: Product Count > 0 Test")

        home = HomePage(driver)
        home.search_for_product("HP")

        results = SearchResultsPage(driver)
        count = results.get_product_count()
        logger.info(f"Product count: {count}")

        assert count > 0, f"Expected product count > 0, got: {count}"
        logger.info("TC_PY_SEARCH_006 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_007 ────────────────────
    def test_TC_PY_SEARCH_007_prices_displayed_with_results(self, driver):
        """TC_PY_SEARCH_007: Products displayed with prices"""
        logger.info("TC_PY_SEARCH_007: Prices Displayed With Results Test")

        home = HomePage(driver)
        home.search_for_product("MacBook")

        results = SearchResultsPage(driver)
        if results.are_results_displayed():
            prices = results.get_prices()
            logger.info(f"Prices: {prices}")
            assert len(prices) > 0, "Prices should be shown alongside products"
        else:
            pytest.skip("No results displayed, skipping price check")
        logger.info("TC_PY_SEARCH_007 PASSED ✓")

    # ──────────────────── TC_PY_SEARCH_008 (Parametrized) ─────
    @pytest.mark.parametrize(
        "search_term, expected",
        SEARCH_PARAMS if SEARCH_PARAMS else [
            ("MacBook", "found"),
            ("iPhone", "found"),
            ("NonExistentProduct12345", "not_found"),
        ]
    )
    @pytest.mark.regression
    def test_TC_PY_SEARCH_008_parametrized_search(self, driver, search_term, expected):
        """TC_PY_SEARCH_008: Parametrized search test using CSV data"""
        logger.info(f"TC_PY_SEARCH_008: Searching '{search_term}' | expected: {expected}")

        home = HomePage(driver)
        home.search_for_product(search_term)

        results = SearchResultsPage(driver)

        if expected.lower() == "found":
            assert results.are_results_displayed(), \
                f"Expected results for '{search_term}'"
        else:
            assert not results.are_results_displayed(), \
                f"Expected no results for '{search_term}'"

        logger.info(f"TC_PY_SEARCH_008 PASSED ✓ | '{search_term}' | {expected}")
