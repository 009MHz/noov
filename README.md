# Selenium Python Test Automation Framework

A comprehensive Selenium-based test automation framework for testing the Noovoleum website using Python, pytest, and Allure reporting.

## 🚀 Features

- **Object-Oriented Design**: Page Object Model (POM) implementation
- **Cross-Platform**: Runs on local machines and GitHub Actions
- **Flexible Execution**: Supports both headless and headed browser modes
- **Rich Reporting**: Allure reports with screenshots and detailed logs
- **CI/CD Integration**: Automated testing via GitHub Actions
- **Parallel Execution**: Support for running tests in parallel
- **Test Categories**: Smoke, regression, and critical test markers
- **Retry Mechanism**: Automatic retry for flaky tests

## 📋 Prerequisites

- Python 3.9+ 
- Chrome browser
- Git

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏗️ Project Structure

```
root/
├─ README.md
├─ pyproject.toml                # or requirements/*.txt per package
├─ pytest.ini                    # markers, addopts, allure dir
├─ .env.example                  # shared env keys (never commit real secrets)
├─ config/
│  ├─ base.yaml                  # default settings
│  ├─ dev.yaml                   # env overrides
│  ├─ staging.yaml
│  ├─ prod.yaml
│  └─ devices.yaml               # mobile & emulation profiles
├─ libs/                         # shared libs reused by all packs
│  ├─ config_loader.py
│  ├─ logger.py
│  ├─ data_factory.py
│  ├─ allure_utils.py
│  └─ waiters.py
├─ common/                       # domain-agnostic abstractions
│  ├─ pages/                     # base classes
│  │  ├─ base_page.py
│  │  ├─ base_mobile_screen.py
│  │  └─ base_api_client.py
│  └─ fixtures/                  # cross-cutting pytest fixtures
│     ├─ auth_context.py         # reusable login/session (storageState)
│     ├─ playwright_fixtures.py  # browser/page/context
│     ├─ appium_fixtures.py      # android/ios drivers
│     ├─ api_fixtures.py         # request_context
│     └─ env_fixtures.py         # config per run
├─ web/                          # desktop & mobile web (Playwright)
│  ├─ pages/                     # POM pages
│  │  └─ login_page.py
│  ├─ tests/
│  │  ├─ smoke/
│  │  └─ regression/
│  └─ elements/                  # locator maps if you separate
├─ api/                          # API tests (Playwright request)
│  ├─ clients/
│  │  └─ auth_client.py
│  └─ tests/
├─ mobile/                       # Appium Python (Android/iOS)
│  ├─ screens/
│  │  └─ login_screen.py
│  └─ tests/
├─ perf/                         # Locust load tests
│  ├─ locustfile.py
│  └─ scenarios/
├─ reports/
│  ├─ allure-results/            # raw results (CI artifact)
│  └─ allure-report/             # generated site (GH Pages)
└─ .github/
   └─ workflows/
      ├─ ui_api.yml              # web & api
      ├─ mobile_android.yml
      ├─ mobile_ios.yml
      └─ publish_allure.yml      # merge + publish to Pages
```

## 🎯 Usage

### Local Execution

**Run all tests:**
```bash
pytest tests/
```

**Run specific test categories:**
```bash
# Smoke tests
pytest tests/ -m smoke

# Regression tests  
pytest tests/ -m regression

# Critical tests
pytest tests/ -m critical
```

**Run in headless mode:**
```bash
pytest tests/ --headless
```

**Run with custom browser:**
```bash
pytest tests/ --browser=chrome
```

**Run with custom base URL:**
```bash
pytest tests/ --base-url=https://noovoleum.com/id/
```

**Parallel execution:**
```bash
pytest tests/ -n auto  # Auto-detect CPU cores
pytest tests/ -n 4     # Use 4 parallel workers
```

### Environment Variables

Set these environment variables to customize test execution:

```bash
export BASE_URL="https://noovoleum.com/id/"
export BROWSER="chrome"
export HEADLESS="false"
export IMPLICIT_WAIT="10"
export EXPLICIT_WAIT="10"
export WINDOW_WIDTH="1920"
export WINDOW_HEIGHT="1080"
```

## 📊 Reporting

### Allure Reports

**Generate and view Allure reports:**
```bash
# After running tests
allure serve allure-results

# Or generate static report
allure generate allure-results --clean -o allure-report
allure open allure-report
```

### HTML Reports

HTML reports are automatically generated in the `reports/` directory after test execution.

## 🔄 CI/CD Pipeline

The framework includes a comprehensive GitHub Actions workflow that:

- Runs tests on multiple Python versions (3.9, 3.10, 3.11)
- Executes different test suites based on triggers:
  - **Pull Request**: Smoke tests
  - **Push to main**: Critical tests
  - **Scheduled**: Regression tests
  - **Manual trigger**: Configurable test suite
- Generates and deploys Allure reports to GitHub Pages
- Uploads artifacts (reports, screenshots, logs)
- Sends notifications on test results

### Workflow Triggers

```yaml
# Automatic triggers
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

# Manual trigger with options
workflow_dispatch:
  inputs:
    test_suite: [all, smoke, regression, critical]
    headless: boolean
```

## 🏷️ Test Markers

Use pytest markers to categorize and run specific tests:

- `@pytest.mark.smoke`: Quick validation tests
- `@pytest.mark.regression`: Comprehensive functionality tests  
- `@pytest.mark.critical`: Essential functionality tests
- `@pytest.mark.slow`: Long-running tests

## 🔧 Configuration

### pytest.ini
Contains pytest configuration including:
- Test discovery patterns
- Report generation settings
- Allure integration
- Custom markers

### utils/config.py
Centralized configuration management:
- Browser settings
- URL configuration  
- Timeouts and waits
- Chrome options
- Environment detection

## 📝 Writing Tests

### Example Test Structure

```python
@allure.epic("Website")
@allure.feature("Home Page")
@allure.story("Page Loading")
@pytest.mark.smoke
def test_home_page_loads(home_page):
    with allure.step("Navigate to home page"):
        home_page.open()
    
    with allure.step("Verify page loads"):
        assert home_page.is_page_loaded()
```

### Page Object Example

```python
class HomePage(BasePage):
    LOGO = (By.CSS_SELECTOR, ".logo")
    
    def open(self):
        self.navigate_to(self.page_url)
        return self
    
    def is_logo_displayed(self):
        return self.is_displayed(self.LOGO)
```

## 🐛 Debugging

### Screenshots
Screenshots are automatically captured:
- On test failures
- At specific test steps
- For debugging purposes

### Logs
Detailed logging is available:
- Console output
- File logging (`test_automation.log`)
- Allure step logging

### Debug Mode
Run tests with verbose output:
```bash
pytest tests/ -v -s --tb=long
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review test logs and reports

## 🔄 Updates and Maintenance

- Regularly update dependencies
- Monitor test execution in CI/CD
- Review and update page objects as the website changes  
- Maintain test data and configuration
- Update browser drivers as needed (handled automatically by webdriver-manager)

---

**Happy Testing! 🧪**