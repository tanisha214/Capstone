"""
Configuration Reader Utility
Reads configuration from config.ini file
"""
import configparser
import os


class ConfigReader:
    """Reads and provides access to configuration settings from config.ini"""

    _config = None
    _config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.ini")

    @classmethod
    def _load_config(cls):
        """Load configuration file if not already loaded"""
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            cls._config.read(cls._config_path)
        return cls._config

    @classmethod
    def get_browser(cls):
        return cls._load_config().get("browser", "browser", fallback="chrome")

    @classmethod
    def get_headless(cls):
        return cls._load_config().getboolean("browser", "headless", fallback=False)

    @classmethod
    def get_implicit_wait(cls):
        return cls._load_config().getint("browser", "implicit_wait", fallback=10)

    @classmethod
    def get_explicit_wait(cls):
        return cls._load_config().getint("browser", "explicit_wait", fallback=15)

    @classmethod
    def get_page_load_timeout(cls):
        return cls._load_config().getint("browser", "page_load_timeout", fallback=30)

    @classmethod
    def get_base_url(cls):
        return cls._load_config().get("application", "base_url", fallback="https://tutorialsninja.com/demo/")

    @classmethod
    def get_app_name(cls):
        return cls._load_config().get("application", "app_name", fallback="TutorialsNinja Demo")

    @classmethod
    def get_csv_path(cls):
        base = os.path.dirname(os.path.dirname(__file__))
        rel = cls._load_config().get("test_data", "csv_path", fallback="test_data/test_data.csv")
        return os.path.join(base, rel)

    @classmethod
    def get_report_dir(cls):
        base = os.path.dirname(os.path.dirname(__file__))
        rel = cls._load_config().get("reporting", "report_dir", fallback="reports/")
        return os.path.join(base, rel)

    @classmethod
    def get_screenshot_dir(cls):
        base = os.path.dirname(os.path.dirname(__file__))
        rel = cls._load_config().get("reporting", "screenshot_dir", fallback="reports/screenshots/")
        return os.path.join(base, rel)

    @classmethod
    def get_log_level(cls):
        return cls._load_config().get("logging", "log_level", fallback="INFO")

    @classmethod
    def get_log_file(cls):
        base = os.path.dirname(os.path.dirname(__file__))
        rel = cls._load_config().get("logging", "log_file", fallback="logs/automation.log")
        return os.path.join(base, rel)
