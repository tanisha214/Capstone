"""
Screenshot Utility
Captures screenshots on test failure and saves them to the reports directory
"""
import os
import time
from selenium import webdriver
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)


class ScreenshotUtil:
    """Utility class for capturing and managing screenshots"""

    @staticmethod
    def capture_screenshot(driver: webdriver.Remote, test_name: str) -> str:
        """
        Captures a screenshot and saves it to the screenshots directory.

        Args:
            driver (webdriver.Remote): Active WebDriver instance
            test_name (str): Name of the test (used in filename)

        Returns:
            str: Absolute path to the saved screenshot file
        """
        screenshot_dir = ConfigReader.get_screenshot_dir()
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # Sanitize test name for file system
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        filename = f"{safe_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)

        try:
            driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to capture screenshot for '{test_name}': {e}")
            return ""

    @staticmethod
    def capture_on_failure(driver: webdriver.Remote, test_name: str) -> str:
        """
        Wrapper to capture screenshot specifically on test failure.

        Args:
            driver (webdriver.Remote): Active WebDriver instance
            test_name (str): Test name for filename

        Returns:
            str: Path to saved screenshot
        """
        logger.warning(f"Test FAILED: {test_name} — capturing screenshot.")
        return ScreenshotUtil.capture_screenshot(driver, f"FAIL_{test_name}")
