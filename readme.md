# 🧪 Software QA, Test Automation & Framework Architecture Portfolio

A comprehensive software quality assurance and test automation portfolio demonstrating end-to-end framework engineering, browser control engines, dynamic DOM locator strategies, and enterprise test architecture.

---

## 📌 Table of Contents
1. [Curriculum & Certification Summary](#-curriculum--certification-summary)
2. [Core Technical Competencies](#-core-technical-competencies)
3. [Lab Modules & Research Experiments (Assignments 1–4)](#-lab-modules--research-experiments-assignments-14)
   - [Assignment 1: W3C Web Element Identification Strategies](#assignment-1-w3c-web-element-identification-strategies)
   - [Assignment 2: Batch DOM Traversal & State Manipulation](#assignment-2-batch-dom-traversal--state-manipulation)
   - [Assignment 3: Dynamic Attribute Resolution via CSS3 Wildcards](#assignment-3-dynamic-attribute-resolution-via-css3-wildcards)
   - [Assignment 4: Direct Child Combinators & Structural Pseudo-Classes](#assignment-4-direct-child-combinators--structural-pseudo-classes)
4. [Capstone Automation Framework (Assignment 2)](#-capstone-automation-framework-assignment-2)
   - [Framework Architecture & Directory Tree](#framework-architecture--directory-tree)
   - [Key Architectural Features](#key-architectural-features)
   - [Test Suite Matrix (32 Scenarios)](#test-suite-matrix-32-scenarios)
   - [Installation & Quick Start](#installation--quick-start)
   - [Execution Commands & PyTest Markers](#execution-commands--pytest-markers)
5. [Host Environment & POSIX Engineering Standards](#-host-environment--posix-engineering-standards)
6. [Author & Acknowledgments](#-author--acknowledgments)

---

## 🎓 Curriculum & Certification Summary

This portfolio encompasses 5 rigorous technical specializations (30 total instructional and applied hours) completed in September 2026, covering automated browser engines, object-oriented design patterns, data-driven pipelines, and continuous integration.

| # | Course Title | Provider / Instructor | Core Focus | Key Technologies |
|---|---|---|---|---|
| **1** | **Python for Automation** | Madecraft | Scripting, automated file management, structured/unstructured parsing, API integration | Python, REST APIs, JSON, XML, HTML, CSS |
| **2** | **Introduction to Selenium** | Karlis Zars | Core web automation concepts, DOM querying, debugging workflows, web scraping | Selenium WebDriver, CSS Selectors, Browser Automation |
| **3** | **Selenium WebDriver with Python** | Whizlabs | WebDriver architecture, multi-window/alert/frame handling, test organization | Python, Selenium WebDriver, `pytest`, `unittest` |
| **4** | **Selenium Automation & Frameworks** | Packt | Page Object Model (POM), data-driven testing (CSV/Excel), Selenium Grid, headless tests | Java, Selenium WebDriver, Selenium Grid, POM, Apache POI |
| **5** | **Playwright (Python) & Robot Framework** | Industry Professionals | Next-gen browser automation, keyword-driven testing, trace analysis, CI/CD tagging | Playwright, Robot Framework, CI/CD, Trace/Log Analyzers |

---

## 🛠️ Core Technical Competencies

- **Languages & Runtimes:** Python 3.9+, Java, Bash / POSIX Shell.
- **Automation Engines:** Selenium WebDriver 4.x, Playwright, Robot Framework.
- **Test Frameworks:** PyTest (Fixtures, Markers, Parameterization), Unittest (Test Suites, Test Runners).
- **Architecture & Design Patterns:** Page Object Model (POM), Driver Factory Pattern, Singleton Logger, Data-Driven Testing (DDT).
- **DOM Traversal & Locator Engineering:** W3C Locators (`By.ID`, `By.NAME`, `By.CLASS_NAME`, `By.TAG_NAME`, `By.LINK_TEXT`), CSS3 Wildcard Selectors (`^=`, `*=`, `$=`), Direct Child Combinators (`>`), Structural Pseudo-Classes (`:nth-child()`).
- **Test Reporting & Telemetry:** `pytest-html`, `HtmlTestRunner`, automated failure screenshot hooks, real-time unbuffered log streaming (`flush=True`).
- **Operating Environment:** Arch Linux x86_64, Mozilla Firefox (GeckoDriver), Google Chrome, Microsoft Edge, Headless CI execution.

---

## 🔬 Lab Modules & Research Experiments (Assignments 1–4)

Before architecting enterprise test suites, four targeted research experiments were conducted on Arch Linux with Mozilla Firefox (GeckoDriver) to evaluate DOM interrogation resilience, collection handling, and CSS selector performance.

```
                          DOM LOCATOR RESEARCH PIPELINE
  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
  │  Assignment 1   │    │  Assignment 2   │    │  Assignment 3   │    │  Assignment 4   │
  │ W3C Core 5      │───▶│ find_elements() │───▶│ CSS Wildcards   │───▶│ Direct Child (>)│
  │ Locators & Waits│    │ Batch Queries   │    │ Dynamic Nodes   │    │ & :nth-child()  │
  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

### Assignment 1: W3C Web Element Identification Strategies
- **Target Fixture:** `https://the-internet.herokuapp.com/login`
- **Objective:** Evaluate and empirically benchmark the 5 primary W3C locator strategies within an authentication workflow under dynamic synchronization.
- **Locator Verification Matrix:**
  - `By.ID` (`#username`): Document-wide unique identifier; typed test credential.
  - `By.NAME` (`password`): Payload identification; cleared and injected password.
  - `By.TAG_NAME` (`h2`): Typography structure; verified heading string `"Login Page"`.
  - `By.CLASS_NAME` (`.subheader`, `.radius`): Stylistic tokens; parsed contextual description and triggered the submission button.
  - `By.LINK_TEXT` (`"Elemental Selenium"`): Text node anchor evaluation; validated persistent footer destination URL.
- **Key Takeaways:**
  - `By.ID` provides the highest reliability across browser builds.
  - Replaced arbitrary sleeps with explicit `WebDriverWait` and `expected_conditions.visibility_of_element_located` to eliminate dynamic timing flakiness.
  - Strict lifecycle teardown in `try...finally` blocks guarantees daemon termination.

---

### Assignment 2: Batch DOM Traversal & State Manipulation
- **Target Fixture:** `https://the-internet.herokuapp.com` & `/checkboxes`
- **Objective:** Analyze behavioral differences between singleton discovery (`find_element`) and collection interrogation (`find_elements`), validating bulk attribute extraction and state toggling.
- **Methodology & Results:**
  - **Bulk Link Enumeration:** Collected all 46 anchor tags (`<a>`) on the root directory. Sanitized text and `href` attributes, categorized graphical/icon nodes, and performed prefix filtering (filtered 3 sub-routes beginning with letter `"C"`).
  - **Collection State Manipulation:** Interrogated an input collection of checkboxes. Evaluated initial boolean state $S_0$ using `is_selected()`, executed `.click()` events, and asserted dynamic state inversion:
    $$S_1 = \neg S_0 \quad \text{and} \quad S_1 \neq S_0$$
- **Key Takeaways:**
  - `find_elements()` safely queries dynamic DOM existence without raising `NoSuchElementException` when counts equal zero ($len = 0$).
  - Defensive handling for `StaleElementReferenceException` is mandatory when iterating dynamically mutating single-page applications.

---

### Assignment 3: Dynamic Attribute Resolution via CSS3 Wildcards
- **Target Fixture:** Rahul Shetty Academy Automation Practice Portal
- **Objective:** Eliminate locator breakage caused by client-side JavaScript frameworks (React, Angular, Vue) injecting dynamic IDs, non-deterministic hashes, or shared functional prefixes.
- **Evaluated Selector Mechanics:**
  - **Starts-With Prefix (`^=`):** `[id^='checkBoxOption']` matches `checkBoxOption1`, `checkBoxOption2`, and `checkBoxOption3` across UI clusters in one query.
  - **Contains Substring (`*=`):** `[id*='BoxOption']` matches elements embedded between timestamps or random build GUIDs.
  - **Ends-With Suffix (`$=`):** `[id$='Option3']` singles out terminal indexes or state flags.
  - **Composite Grouping:** `[name^='radioButton']` accurately matches component clusters.
- **Key Takeaways:**
  - CSS wildcard selectors execute natively inside the browser layout engine (`document.querySelectorAll`), providing faster execution than complex XPath evaluators.
  - Pairing wildcards with parent scopes (e.g., `fieldset [id^='checkBoxOption']`) prevents accidental ambiguity matches.

---

### Assignment 4: Direct Child Combinators & Structural Pseudo-Classes
- **Target Fixture:** Rahul Shetty Academy Portal & Test Automation Practice Blog
- **Objective:** Prevent accidental deep-descent matching across nested composite UI components by combining direct child combinators (`>`) with positional pseudo-classes (`:nth-child()`).
- **Evaluated Patterns:**
  - **Strict Scoping:** `fieldset > label > input[type='checkbox']` isolates first-generation child checkboxes, preventing bleed into secondary wrappers.
  - **Tabular 2D Coordinate Addressing:**
    $$\text{Target Cell}(r, c) = \text{table\#productTable} > \text{tbody} > \text{tr:nth-child}(r) > \text{td:nth-child}(c)$$
  - **Column Vector Extraction:** `table#productTable > tbody > tr > td:nth-child(2)` extracted all product names (`Smartphone`, `Laptop`, `Tablet`, `Smartwatch`, `Wireless Earbuds`) without brittle absolute XPaths.
- **Key Takeaways:**
  - Structural pseudo-classes eliminate the fragility of positional absolute XPaths (e.g., `/html/body/div[2]/table/tbody/tr[1]/td[1]`).
  - Modular lifecycle partitioning prevents cascade failures during heavy multi-table parsing.

---

## 🚀 Capstone Automation Framework (Assignment 2)

An industrial-grade, dual-engine (PyTest + Unittest) test automation framework written in Python using the **Page Object Model (POM)** pattern to automate end-to-end user journeys for the **TutorialsNinja Demo E-Commerce platform**.

**Application Under Test (AUT):** [https://tutorialsninja.com/demo/](https://tutorialsninja.com/demo/)

---

### Framework Architecture & Directory Tree

```
Capstone-Project/
│
├── config/                         # Central Configuration Management
│   ├── __init__.py
│   └── config.ini                  # Environment, URLs, headless flag, timeouts
│
├── pages/                          # Page Object Model (POM) Abstraction Layer
│   ├── __init__.py
│   ├── base_page.py                # Wrapper for explicit waits, clicks, and inputs
│   ├── home_page.py                # Search bar, My Account navigation
│   ├── login_page.py               # Input fields, submit trigger, validation banners
│   ├── account_page.py             # Authenticated user dashboard, logout verification
│   └── search_results_page.py      # Results grid, product counts, titles, pricing
│
├── utilities/                      # Reusable Infrastructure Components
│   ├── __init__.py
│   ├── config_reader.py            # INI file parser helper
│   ├── driver_factory.py           # Cross-browser initialization (Chrome / Firefox / Edge)
│   ├── logger.py                   # Centralized dual file/console timestamped logging
│   ├── screenshot_util.py          # Automated capture hook on assertion failure
│   └── csv_reader.py               # CSV parameterization utility
│
├── test_data/                      # Externalized Test Datasets (CSV)
│   ├── test_data.csv               # Shared baseline parameters
│   ├── login_data.csv              # Valid/invalid credential payloads
│   └── search_data.csv             # Product queries and expected match types
│
├── tests/                          # Automated Test Suites
│   ├── __init__.py
│   ├── conftest.py                 # PyTest fixtures, hooks, failure triggers
│   ├── test_suite_runner.py        # Unittest HTML suite runner
│   │
│   ├── unittest_tests/             # Unittest Implementation
│   │   ├── __init__.py
│   │   ├── base_test.py            # Base test lifecycle (setUp / tearDown)
│   │   ├── test_login.py           # Login test cases (TC_LOGIN_001–008)
│   │   └── test_search.py          # Search test cases (TC_SEARCH_001–008)
│   │
│   └── pytest_tests/               # PyTest Implementation
│       ├── __init__.py
│       ├── test_login_pytest.py    # PyTest login suite (TC_PY_LOGIN_001–008)
│       └── test_search_pytest.py   # PyTest search suite (TC_PY_SEARCH_001–008)
│
├── reports/                        # Automated Execution Outputs
│   ├── pytest_report.html          # PyTest HTML execution report
│   ├── TestReport_<timestamp>.html # Unittest execution report
│   └── screenshots/                # Failure capture repository (PNG)
│
├── logs/                           # Runtime Log Files
│   ├── automation.log              # Framework log output
│   └── pytest.log                  # PyTest engine output
│
├── pytest.ini                      # PyTest marker definitions and flags
├── requirements.txt                # Production dependency manifest
└── README.md                       # Documentation
```

---

### Key Architectural Features

1. **Strict Page Object Model (POM):** Complete separation between web locators, page actions, and test assertions. Changes in the UI structure only require edits in `pages/`, leaving test scenarios untouched.
2. **Dual-Framework Parity:** Full functional test coverage implemented in both **PyTest** (fixtures, parameterization, markers) and **Unittest** (`TestCase`, `setUp`/`tearDown`, custom runners).
3. **Data-Driven Architecture (CSV):** Test cases consume datasets externalized in `test_data/login_data.csv` and `test_data/search_data.csv`, supporting positive, negative, and edge-case execution loops.
4. **Intelligent Driver Management:** `driver_factory.py` leverages `webdriver-manager` alongside manual binary paths to dynamically launch Chrome, Firefox, or Edge.
5. **Automated Failure Screenshots:** PyTest hooks (`pytest_runtest_makereport`) and Unittest `tearDown` methods automatically capture PNG artifacts upon assertion failure and link them to generated reports.
6. **Cross-Browser & Headless Ready:** Driven entirely by `config.ini` or CLI flags, allowing headless execution in Linux CI/CD environments.

---

### Test Suite Matrix (32 Scenarios)

#### 🔐 Authentication Suite (16 Tests)

| Unittest Case ID | PyTest Case ID | Description | Validation Strategy |
|---|---|---|---|
| `TC_LOGIN_001` | `TC_PY_LOGIN_001` | Page Title Verification | Assert page title matches `"Account Login"` |
| `TC_LOGIN_002` | `TC_PY_LOGIN_002` | Valid User Authentication | Valid credentials redirect to `"My Account"` |
| `TC_LOGIN_003` | `TC_PY_LOGIN_003` | Invalid Password Rejection | Error warning displayed on invalid password |
| `TC_LOGIN_004` | `TC_PY_LOGIN_004` | Warning Content Verification | Verify alert text matches strict copy |
| `TC_LOGIN_005` | `TC_PY_LOGIN_005` | Empty Credentials Validation | Form triggers standard validation warning |
| `TC_LOGIN_006` | `TC_PY_LOGIN_006` | UI Component Visibility | Validate `"Returning Customer"` header exists |
| `TC_LOGIN_007` | `TC_PY_LOGIN_007` | Forgotten Password Link | Anchor redirects to password recovery page |
| `TC_LOGIN_008` | `TC_PY_LOGIN_008` | **Data-Driven (CSV)** Matrix | Parameterized iterations (Success & Failures) |

#### 🔍 Product Search Suite (16 Tests)

| Unittest Case ID | PyTest Case ID | Description | Validation Strategy |
|---|---|---|---|
| `TC_SEARCH_001` | `TC_PY_SEARCH_001` | Valid Query Execution | Search for `"MacBook"` returns matching listings |
| `TC_SEARCH_002` | `TC_PY_SEARCH_002` | Result Item Count | Assert returned item count is $> 0$ |
| `TC_SEARCH_003` | `TC_PY_SEARCH_003` | Zero-Match Negative Test | Non-existent queries display empty search prompt |
| `TC_SEARCH_004` | `TC_PY_SEARCH_004` | Search Heading Verification | Results header reflects queried terms |
| `TC_SEARCH_005` | `TC_PY_SEARCH_005` | Empty Search Query | System handles empty string input gracefully |
| `TC_SEARCH_006` | `TC_PY_SEARCH_006` | Dynamic URL Verification | URL path contains `/index.php?route=product/search` |
| `TC_SEARCH_007` | `TC_PY_SEARCH_007` | Pricing / Metadata Presence | Ensure extracted price tags are visible |
| `TC_SEARCH_008` | `TC_PY_SEARCH_008` | **Data-Driven (CSV)** Matrix | Parameterized queries mapped to expected counts |

---

### Installation & Quick Start

#### 1. Clone the repository & create a virtual environment:
```bash
git clone <repository-url>
cd Capstone-Project
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Update configuration settings (`config/config.ini`):
```ini
[browser]
browser = chrome       # Options: chrome | firefox | edge
headless = False       # True for headless / CI environments

[application]
base_url = https://tutorialsninja.com/demo/
```

#### 4. Prepare local test credentials:
Edit `test_data/login_data.csv` to specify a registered account:
```csv
email,password,expected_result
user.test@example.com,SecurePass123!,success
invalid.user@example.com,WrongPassword,failure
```

---

### Execution Commands & PyTest Markers

#### 🔷 PyTest Test Suites
```bash
# Run all PyTest tests with self-contained HTML reporting
pytest tests/pytest_tests/ -v --html=reports/pytest_report.html --self-contained-html

# Run specific marker groups
pytest tests/pytest_tests/ -m smoke -v
pytest tests/pytest_tests/ -m login -v
pytest tests/pytest_tests/ -m search -v
pytest tests/pytest_tests/ -m regression -v

# Override browser or headless flag via CLI
pytest tests/pytest_tests/ --browser=firefox -v
pytest tests/pytest_tests/ --headless -v
```

#### 🔶 Unittest Test Suites
```bash
# Execute entire Unittest suite with HTML report generation
python tests/test_suite_runner.py

# Execute specific Unittest module
python -m unittest tests/unittest_tests/test_login.py -v
```

---

## 🖥️ Host Environment & POSIX Engineering Standards

The scripts and frameworks in this repository were engineered and validated on **Arch Linux x86_64** under strict POSIX conventions:

1. **Clean Process Lifecycle:** All browser invocations are wrapped inside deterministic `try...finally` teardown patterns, ensuring `driver.quit()` terminates GeckoDriver and ChromeDriver daemons and frees virtual display sockets.
2. **Dynamic Fallbacks:** Automated binary discovery checks native `/usr/bin/` paths before engaging `webdriver-manager` or `Selenium Manager`.
3. **CI/CD Stream Flushing:** Standard output streams use explicit `flush=True` calls to prevent terminal buffering issues across headless CI runners (e.g., GitHub Actions, GitLab CI, Jenkins).

---

## 👤 Author & Acknowledgments

- **Lead Engineer & Author:** Tanisha
- **Specialization Curriculum:** Software QA, Test Automation & Framework Architecture
- **Date:** September 2026