"""
Driver Factory
Responsible for creating and configuring WebDriver instances
"""
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    WEBDRIVER_MANAGER = True
except ImportError:
    WEBDRIVER_MANAGER = False

from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)

# Project root (one level up from utilities/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
        """
        Creates and returns a WebDriver instance.

        Firefox geckodriver discovery order (important for Arch Linux):
          1. System PATH    — sudo pacman -S geckodriver
          2. Local drivers/ — place binary at  drivers/geckodriver
          3. webdriver-manager — auto-downloads from GitHub (slow on poor networks)

        Args:
            browser (str): 'chrome' | 'firefox' | 'edge'
            headless (bool): Run in headless mode if True

        Returns:
            webdriver.Remote: Configured WebDriver instance
        """
        browser = (browser or ConfigReader.get_browser()).lower()
        headless = headless if headless is not None else ConfigReader.get_headless()

        logger.info(f"Initializing {browser} driver | headless={headless}")

        driver = None

        # ──────────────────────────────────────────── CHROME ──────
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            if headless:
                options.add_argument("--headless=new")

            system_chromedriver = shutil.which("chromedriver")
            local_chromedriver = os.path.join(_PROJECT_ROOT, "drivers", "chromedriver")
            local_chrome_exists = os.path.isfile(local_chromedriver) and os.access(local_chromedriver, os.X_OK)

            if system_chromedriver:
                logger.info(f"[1/3] Using system chromedriver: {system_chromedriver}")
                driver = webdriver.Chrome(
                    service=ChromeService(executable_path=system_chromedriver),
                    options=options
                )
            elif local_chrome_exists:
                logger.info(f"[2/3] Using local chromedriver: {local_chromedriver}")
                driver = webdriver.Chrome(
                    service=ChromeService(executable_path=local_chromedriver),
                    options=options
                )
            elif WEBDRIVER_MANAGER:
                logger.info("[3/3] Downloading chromedriver via webdriver-manager...")
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            else:
                driver = webdriver.Chrome(options=options)

        # ──────────────────────────────────────────── FIREFOX ─────
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            # Geckodriver discovery: PATH → drivers/ folder → webdriver-manager
            system_gecko = shutil.which("geckodriver")
            local_gecko = os.path.join(_PROJECT_ROOT, "drivers", "geckodriver")
            local_gecko_exists = os.path.isfile(local_gecko) and os.access(local_gecko, os.X_OK)

            if system_gecko:
                gecko_path = system_gecko
                logger.info(f"[1/3] Using system geckodriver from PATH: {gecko_path}")
            elif local_gecko_exists:
                gecko_path = local_gecko
                logger.info(f"[2/3] Using local geckodriver from drivers/ folder: {gecko_path}")
            elif WEBDRIVER_MANAGER:
                logger.info("[3/3] geckodriver not found locally — downloading via webdriver-manager (may take a while)...")
                gecko_path = GeckoDriverManager().install()
            else:
                raise RuntimeError(
                    "\n\nGeckodriver not found! To fix this, run ONE of:\n"
                    "  Option A: sudo pacman -S geckodriver\n"
                    "  Option B: Download from https://github.com/mozilla/geckodriver/releases\n"
                    "            and place the binary at: drivers/geckodriver\n"
                )

            driver = webdriver.Firefox(
                service=FirefoxService(executable_path=gecko_path),
                options=options
            )

        # ──────────────────────────────────────────── EDGE ────────
        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            if headless:
                options.add_argument("--headless")
            if WEBDRIVER_MANAGER:
                driver = webdriver.Edge(
                    service=EdgeService(EdgeChromiumDriverManager().install()),
                    options=options
                )
            else:
                driver = webdriver.Edge(options=options)

        else:
            raise ValueError(
                f"Unsupported browser: '{browser}'. "
                "Supported values: chrome | firefox | edge"
            )

        driver.implicitly_wait(ConfigReader.get_implicit_wait())
        driver.set_page_load_timeout(ConfigReader.get_page_load_timeout())
        driver.maximize_window()

        logger.info(f"{browser.capitalize()} driver initialized successfully.")
        return driver
