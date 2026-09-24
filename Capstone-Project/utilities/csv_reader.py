"""
CSV Data Reader Utility
Reads test data from CSV files for data-driven testing
"""
import csv
import os
from typing import List, Dict, Any
from utilities.config_reader import ConfigReader
from utilities.logger import get_logger

logger = get_logger(__name__)


class CSVReader:
    """Utility class for reading test data from CSV files"""

    @staticmethod
    def read_csv(file_path: str = None) -> List[Dict[str, Any]]:
        """
        Reads all rows from a CSV file and returns as list of dicts.

        Args:
            file_path (str): Path to CSV file. Defaults to config csv_path.

        Returns:
            List[Dict]: List of row dictionaries
        """
        if file_path is None:
            file_path = ConfigReader.get_csv_path()

        if not os.path.exists(file_path):
            logger.error(f"CSV file not found: {file_path}")
            return []

        records = []
        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    records.append(dict(row))
            logger.info(f"Loaded {len(records)} records from CSV: {file_path}")
        except Exception as e:
            logger.error(f"Error reading CSV '{file_path}': {e}")

        return records

    @staticmethod
    def get_login_data(file_path: str = None) -> List[tuple]:
        """
        Returns login test data as list of (email, password, expected_result) tuples.

        Args:
            file_path (str): Optional path to CSV file.

        Returns:
            List[tuple]: Login data tuples
        """
        rows = CSVReader.read_csv(file_path)
        login_data = []
        for row in rows:
            if "email" in row and "password" in row:
                expected = row.get("expected_result", "success")
                login_data.append((row["email"], row["password"], expected))
        return login_data

    @staticmethod
    def get_search_data(file_path: str = None) -> List[tuple]:
        """
        Returns search test data as list of (search_term, expected_result) tuples.

        Args:
            file_path (str): Optional path to CSV file.

        Returns:
            List[tuple]: Search data tuples
        """
        rows = CSVReader.read_csv(file_path)
        search_data = []
        for row in rows:
            if "search_term" in row:
                expected = row.get("expected_result", "found")
                search_data.append((row["search_term"], expected))
        return search_data
