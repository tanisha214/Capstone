# 📘 Capstone Assignment 2
## Selenium Python Automation Framework
### Unittest + PyTest + Page Object Model (POM)

---

## 🎯 Objective

Design and develop a **robust Selenium Python Automation Framework** that automates the **Login** and **Product Search** functionality of the TutorialsNinja Demo E-Commerce application.

**Application Under Test:** [https://tutorialsninja.com/demo/](https://tutorialsninja.com/demo/)

---

## 🏗️ Framework Architecture

```
Capstone-Project/
│
├── config/                         # Configuration Management
│   ├── __init__.py
│   └── config.ini                  # Central config (browser, URLs, paths)
│
├── pages/                          # Page Object Model (POM)
│   ├── __init__.py
│   ├── base_page.py                # Base page with common Selenium methods
│   ├── home_page.py                # Home Page Object
│   ├── login_page.py               # Login Page Object
│   ├── account_page.py             # Account/Dashboard Page Object
│   └── search_results_page.py      # Search Results Page Object
│
├── utilities/                      # Utility Classes
│   ├── __init__.py
│   ├── config_reader.py            # Reads config.ini
│   ├── driver_factory.py           # WebDriver initialization (Chrome/FF/Edge)
│   ├── logger.py                   # Centralized logging
│   ├── screenshot_util.py          # Screenshot capture on failure
│   └── csv_reader.py               # CSV test data reader
│
├── test_data/                      # Test Data (CSV)
│   ├── test_data.csv               # Default combined test data
│   ├── login_data.csv              # Login test data (email, password, expected)
│   └── search_data.csv             # Search test data (search_term, expected)
│
├── tests/                          # All Test Files
│   ├── __init__.py
│   ├── conftest.py                 # PyTest fixtures & hooks
│   ├── test_suite_runner.py        # Unittest HTML suite runner
│   │
│   ├── unittest_tests/             # Unittest-based Tests
│   │   ├── __init__.py
│   │   ├── base_test.py            # Base test class (setUp/tearDown)
│   │   ├── test_login.py           # Login tests (TC_LOGIN_001–008)
│   │   └── test_search.py          # Search tests (TC_SEARCH_001–008)
│   │
│   └── pytest_tests/               # PyTest-based Tests
│       ├── __init__.py
│       ├── test_login_pytest.py    # Login tests (TC_PY_LOGIN_001–008)
│       └── test_search_pytest.py   # Search tests (TC_PY_SEARCH_001–008)
│
├── reports/                        # Generated Reports (auto-created)
│   └── screenshots/                # Screenshots on failure
│
├── logs/                           # Log files (auto-created)
│
├── pytest.ini                      # PyTest configuration & markers
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🛠️ Framework Components

### 1. Configuration Management
- **`config/config.ini`** — Central configuration file
- **`utilities/config_reader.py`** — ConfigParser-based reader
- Controls: browser type, headless mode, waits, URLs, paths

### 2. Page Object Model (POM)
| Page Class | Description |
|---|---|
| `BasePage` | Common Selenium methods (click, type, wait, find) |
| `HomePage` | Search box, My Account menu navigation |
| `LoginPage` | Email/password fields, login button, error alerts |
| `AccountPage` | Post-login dashboard, logout |
| `SearchResultsPage` | Product listings, counts, names, prices |

### 3. Utility Classes
| Utility | Purpose |
|---|---|
| `DriverFactory` | Creates Chrome/Firefox/Edge WebDriver |
| `ConfigReader` | Reads `config.ini` settings |
| `ScreenshotUtil` | Captures PNG screenshots on failure |
| `CSVReader` | Reads CSV test data into dicts/tuples |
| `logger` | File + console logging with timestamps |

### 4. Test Data Handling (CSV)
```csv
# login_data.csv
email,password,expected_result
test@example.com,Test@1234,success
invalid@user.com,wrongpassword,failure

# search_data.csv
search_term,expected_result
MacBook,found
NonExistentProduct12345,not_found
```

### 5. Screenshots on Failure
- **Unittest**: `tearDown()` detects failures and calls `ScreenshotUtil.capture_on_failure()`
- **PyTest**: `pytest_runtest_makereport` hook triggers screenshots automatically
- Saved in: `reports/screenshots/FAIL_<test_name>_<timestamp>.png`

### 6. HTML Reporting
- **Unittest**: Uses `HtmlTestRunner` → `reports/TestReport_<timestamp>.html`
- **PyTest**: Uses `pytest-html` → `reports/pytest_report.html`

---

## 📋 Test Cases

### Login Tests (16 total: 8 Unittest + 8 PyTest)

| TC ID | Framework | Description |
|---|---|---|
| TC_LOGIN_001 | Unittest | Valid login redirects to account page |
| TC_LOGIN_002 | Unittest | Invalid credentials show error alert |
| TC_LOGIN_003 | Unittest | Empty email shows validation error |
| TC_LOGIN_004 | Unittest | Empty password shows validation error |
| TC_LOGIN_005 | Unittest | Login page has correct title |
| TC_LOGIN_006 | Unittest | "Returning Customer" heading visible |
| TC_LOGIN_007 | Unittest | Forgotten Password link works |
| TC_LOGIN_008 | Unittest | Data-driven login test from CSV |
| TC_PY_LOGIN_001 | PyTest | Login page loads with correct title |
| TC_PY_LOGIN_002 | PyTest | Valid login redirects to account |
| TC_PY_LOGIN_003 | PyTest | Invalid login shows error |
| TC_PY_LOGIN_004 | PyTest | Error message content verified |
| TC_PY_LOGIN_005 | PyTest | Empty credentials trigger error |
| TC_PY_LOGIN_006 | PyTest | Returning Customer heading |
| TC_PY_LOGIN_007 | PyTest | Forgotten Password navigation |
| TC_PY_LOGIN_008 | PyTest | **Parametrized** — CSV data-driven |

### Search Tests (16 total: 8 Unittest + 8 PyTest)

| TC ID | Framework | Description |
|---|---|---|
| TC_SEARCH_001 | Unittest | MacBook search returns results |
| TC_SEARCH_002 | Unittest | Result count > 0 for MacBook |
| TC_SEARCH_003 | Unittest | Non-existent product = no results |
| TC_SEARCH_004 | Unittest | Search heading displayed |
| TC_SEARCH_005 | Unittest | Empty search handled gracefully |
| TC_SEARCH_006 | Unittest | URL contains 'search' after query |
| TC_SEARCH_007 | Unittest | Home page logo visible |
| TC_SEARCH_008 | Unittest | Data-driven search from CSV |
| TC_PY_SEARCH_001 | PyTest | MacBook returns results |
| TC_PY_SEARCH_002 | PyTest | Product names returned |
| TC_PY_SEARCH_003 | PyTest | Invalid product = no results |
| TC_PY_SEARCH_004 | PyTest | Search results heading verified |
| TC_PY_SEARCH_005 | PyTest | URL contains 'search' |
| TC_PY_SEARCH_006 | PyTest | Product count > 0 for HP |
| TC_PY_SEARCH_007 | PyTest | Prices displayed with results |
| TC_PY_SEARCH_008 | PyTest | **Parametrized** — CSV data-driven |

---

## 🚀 Setup & Execution

### Step 1 — Install Dependencies
```bash
cd Capstone-Project
pip install -r requirements.txt
```

### Step 2 — Configure Settings
Edit `config/config.ini`:
```ini
[browser]
browser = chrome       # chrome | firefox | edge
headless = False       # True for headless mode

[application]
base_url = https://tutorialsninja.com/demo/
```

### Step 3 — Update Test Credentials
Edit `test_data/login_data.csv` with a **valid registered account**:
```csv
email,password,expected_result
your_email@example.com,YourPassword,success
```

> ⚠️ **Important**: Register an account at https://tutorialsninja.com/demo/ first.

### Step 4 — Run Tests

#### 🔷 Run ALL PyTest Tests (with HTML Report):
```bash
pytest tests/pytest_tests/ -v --html=reports/pytest_report.html --self-contained-html
```

#### 🔷 Run PyTest Smoke Tests Only:
```bash
pytest tests/pytest_tests/ -m smoke -v
```

#### 🔷 Run PyTest Login Tests Only:
```bash
pytest tests/pytest_tests/ -m login -v
```

#### 🔷 Run PyTest Search Tests Only:
```bash
pytest tests/pytest_tests/ -m search -v
```

#### 🔷 Run ALL Unittest Tests (with HTML Report):
```bash
python tests/test_suite_runner.py
```

#### 🔷 Run Specific Unittest File:
```bash
python -m pytest tests/unittest_tests/test_login.py -v
```

#### 🔷 Run with Different Browser:
```bash
pytest tests/pytest_tests/ --browser=firefox -v
pytest tests/pytest_tests/ --browser=edge -v
```

#### 🔷 Run in Headless Mode:
```bash
pytest tests/pytest_tests/ --headless -v
```

---

## 📊 PyTest Markers

| Marker | Description | Run Command |
|---|---|---|
| `smoke` | Quick sanity tests | `pytest -m smoke` |
| `regression` | Full test run | `pytest -m regression` |
| `login` | Login feature tests | `pytest -m login` |
| `search` | Search feature tests | `pytest -m search` |
| `negative` | Negative scenarios | `pytest -m negative` |

---

## 📂 Output Files

| Output | Location |
|---|---|
| PyTest HTML Report | `reports/pytest_report.html` |
| Unittest HTML Report | `reports/TestReport_<timestamp>.html` |
| Failure Screenshots | `reports/screenshots/FAIL_*.png` |
| Framework Logs | `logs/automation.log` |
| PyTest Logs | `logs/pytest.log` |

---

## 🔧 Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.9+ | Primary language |
| Selenium | 4.18+ | Browser automation |
| PyTest | 8.0+ | Test framework |
| Unittest | Built-in | Test framework |
| webdriver-manager | 4.0+ | Auto ChromeDriver management |
| pytest-html | 4.1+ | HTML test reports |
| HtmlTestRunner | 1.2+ | Unittest HTML reports |
| ConfigParser | Built-in | Configuration management |

---

## 🌟 Framework Features

- ✅ **Page Object Model (POM)** — Clean separation of test logic and UI elements
- ✅ **Unittest** — Traditional Python test framework with setUp/tearDown
- ✅ **PyTest** — Modern test framework with fixtures, markers, parametrize
- ✅ **Data-Driven Testing** — CSV-based test data for both frameworks
- ✅ **Cross-Browser** — Chrome, Firefox, Edge support
- ✅ **Headless Mode** — CI/CD compatible
- ✅ **Screenshots on Failure** — Automatic PNG capture
- ✅ **HTML Reports** — Both Unittest and PyTest generate reports
- ✅ **Centralized Logging** — File + console with timestamps
- ✅ **Configuration Management** — Single `config.ini` controls everything
- ✅ **WebDriver Manager** — No manual driver downloads needed

---

*Submitted by: Tanisha | Capstone Assignment 2*
