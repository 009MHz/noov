# Noovoleum Test Automation Framework

This repository contains a comprehensive automation framework for the Noovoleum platform. It demonstrates advanced web, API, mobile and performance testing using Python with modern tooling and device emulation capabilities.

## Features
- **Advanced Web UI Automation** with Playwright and device emulation
- **Cross-Platform Testing** with mobile and desktop configurations
- **Device Emulation** using Playwright's 143+ built-in device profiles
- **Parallel Test Execution** with pytest-xdist for faster test runs
- **API Testing** through HTTPX clients with comprehensive validation
- **Mobile Testing** via Appium with Android and iOS support
- **Performance Testing** with Locust for load and stress testing
- **Intelligent Configuration** with platform-aware browser setup
- **Comprehensive Reporting** with pytest-html, Allure, and failure retry mechanisms

## Preparation & Installation
1. **Prerequisites**
   - Python 3.9+
   - Git
   - Browsers for Playwright (`playwright install` will download them)
   - Optional Android/iOS emulators for mobile tests

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd noovoleum
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

4. **Install dependencies and browsers**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Running tests
Run tests with `pytest` using the enhanced platform-aware configuration system.

### Platform Selection
The framework supports platform-specific testing with automatic device emulation:

```bash
# Run tests on desktop only (default)
pytest tests --platform=desktop

# Run tests on mobile devices only
pytest tests --platform=mobile

# Run tests on both desktop and mobile platforms
pytest tests --platform=all
```

### Parallel Execution
Leverage pytest-xdist for faster test execution:

```bash
# Run tests in parallel with automatic worker detection
pytest tests --platform=all -n=auto

# Run with specific number of workers
pytest tests --platform=mobile -n=4
```

### Headless Mode
Run tests without browser UI for CI/CD environments:

```bash
# Headless execution
pytest tests --platform=all --headless

# Combined with parallel execution and retries
pytest tests --platform=all --headless -n=auto --reruns=1 --reruns-delay=2
```

### Test Categories

#### Web UI tests
```bash
# All web tests (desktop and mobile)
pytest tests/web --platform=all

# Desktop web tests only
pytest tests/web --platform=desktop

# Mobile web tests with device emulation
pytest tests/web --platform=mobile

# Specific test with logging
pytest tests/web/test_home_page.py -v --log-cli-level=INFO
```

#### API tests
```bash
# All API tests (platform-independent)
pytest tests/api

# API tests with parallel execution
pytest tests/api -n=auto

# Specific API test categories
pytest tests/api/test_boxes.py tests/api/test_boxes_negative.py
```

#### Mobile Application tests
```bash
# Android tests
pytest tests/mobile/android

# iOS tests  
pytest tests/mobile/ios

# All mobile app tests
pytest tests/mobile
```

#### Smoke tests
```bash
# Quick smoke tests across all platforms
pytest tests/web/smoke --platform=all
```

#### Performance tests
```bash
# Load testing with Locust
locust -f tests/performance/locustfile.py --headless -u 50 -r 5 -t 5m --host https://api.example.com

# Performance testing with custom user load
locust -f tests/performance/locustfile.py --users 100 --spawn-rate 10 --run-time 300s
```

### Reporting
Generate comprehensive test reports:

```bash
# HTML reports
pytest tests --platform=all --html=reports/report.html

# Allure reports (requires allure installation)
pytest tests --platform=all --alluredir=reports/allure
allure serve reports/allure

# Combined reporting with parallel execution
pytest tests --platform=all -n=auto --alluredir=reports --html=reports/html_report.html
```

## Device Emulation

The framework uses Playwright's built-in device configurations for accurate mobile testing:

### Supported Devices
- **iPhone Series**: iPhone 6 through iPhone 15 (all variants)
- **Android Devices**: Pixel series, Galaxy series, Nexus series  
- **Tablets**: iPad models, Galaxy Tab, Nexus tablets
- **Desktop**: Chrome, Firefox, Safari, Edge (including HiDPI variants)

### Default Device Configurations
- **Mobile Platform**: Pixel 7 (modern Android device)
- **Desktop Platform**: Desktop Chrome
- **Custom Devices**: Specify via `device_name` parameter

### Device Configuration Features
- ✅ Accurate viewport dimensions and device pixel ratios
- ✅ Platform-specific user agent strings
- ✅ Touch event support (`has_touch`, `maxTouchPoints`)
- ✅ Mobile JavaScript API enablement (`is_mobile`)
- ✅ Orientation API support for mobile devices
- ✅ CSS media query responses for responsive design testing

## Project structure
```
utils/                 # Enhanced browser and pytest configuration
  browser_config.py    # Device emulation and browser management
  pytest_config.py     # Platform-aware test configuration
  sess_handler.py      # Session management utilities
sources/
  web/                 # Web page objects and components
    home_page.py       # Homepage page object model
tests/
  web/                 # Web UI tests
    desktop/           # Desktop-specific web tests
    mobile/            # Mobile web tests  
    smoke/             # Cross-platform smoke tests
    test_home_page.py         # Homepage tests (desktop + mobile)
    test_home_contact_form.py # Contact form tests (desktop + mobile)
    test_home_footer.py       # Footer tests (desktop + mobile)
  mobile/              # Mobile application tests
    android/           # Android app tests
      test_login_android.py
    ios/               # iOS app tests  
      test_login_ios.py
  api/                 # API tests
    test_boxes.py           # API functionality tests
    test_boxes_negative.py  # API error handling tests
    test_boxes_contract.py  # API contract validation
    test_boxes_scheme_param.py # API schema validation
  performance/         # Performance testing
    locustfile.py      # Locust performance scenarios
  test_suites.md       # Manual test case documentation
reports/               # Test execution reports
conftest.py            # Pytest configuration hooks and fixtures
pytest.ini             # Pytest settings, markers, and test discovery
requirements.txt       # Project dependencies
```

## Configuration

### Environment Configuration
The framework supports multiple execution environments and modes:

```bash
# Environment selection
pytest tests --env=dev --platform=all
pytest tests --env=staging --platform=mobile
pytest tests --env=prod --platform=desktop

# Execution modes
pytest tests --mode=local --platform=all        # Local execution (default)
pytest tests --mode=pipeline --headless         # CI/CD pipeline execution
```

### Platform-Aware Testing
Tests automatically adapt to the selected platform:

- **Desktop Tests**: Use Desktop Chrome with 1920x1080 viewport
- **Mobile Tests**: Use Pixel 7 device emulation with touch support
- **Cross-Platform**: Run the same test on both desktop and mobile configurations

### Browser Configuration
The enhanced `browser_config.py` provides:

- **Automatic Device Selection**: Platform-appropriate devices chosen automatically
- **Race Condition Handling**: Retry mechanisms for parallel execution stability
- **Session Management**: Reusable browser contexts for authenticated tests
- **Error Recovery**: Graceful fallbacks for device configuration issues

### Test Markers
Use pytest markers for test categorization:

```python
@pytest.mark.mobile          # Mobile-specific tests
@pytest.mark.desktop         # Desktop-specific tests  
@pytest.mark.smoke           # Smoke test suite
@pytest.mark.regression      # Regression test suite
```

## Advanced Features

### Parallel Execution with pytest-xdist
The framework supports parallel test execution across multiple workers:

- **Race Condition Protection**: Session-scoped fixtures prevent browser conflicts
- **Worker Safety**: Function-scoped browser instances for parallel safety
- **Load Balancing**: Automatic test distribution across available workers

### Failure Handling and Retries
Built-in retry mechanisms for flaky tests:

```bash
# Retry failed tests with delay
pytest tests --reruns=2 --reruns-delay=3

# Combined with parallel execution
pytest tests --platform=all -n=auto --reruns=1 --reruns-delay=2
```

### Device-Specific Testing
Target specific devices for precise testing:

```python
# In test code - specify device directly
context = await runner.context_init(device_name="iPhone 15 Pro")
context = await runner.context_init(device_name="Galaxy S24")
context = await runner.context_init(device_name="iPad Pro 11")
```

## Configuration
The framework uses environment variables and CLI options for flexible configuration. Test settings are managed through the `utils/pytest_config.py` module with support for dotenv files.

## Recent Updates

### v2.0 - Enhanced Device Emulation and Platform Support
- ✅ **Playwright Device Integration**: Native support for 143+ built-in device configurations
- ✅ **Cross-Platform Testing**: Unified `--platform=desktop/mobile/all` CLI option
- ✅ **Parallel Execution**: pytest-xdist integration with race condition protection
- ✅ **Mobile-First Architecture**: Automatic device selection with `is_mobile` and `has_touch` support
- ✅ **Enhanced Browser Configuration**: Intelligent fallback and error handling
- ✅ **Session Management**: Optimized browser context sharing for performance

### Key Improvements
- **Device Accuracy**: Real device emulation instead of manual viewport configuration
- **Performance**: Parallel test execution reduces run time by 60-80%
- **Reliability**: Race condition protection and retry mechanisms
- **Flexibility**: Platform-agnostic tests that adapt to desktop or mobile environments
- **Developer Experience**: Comprehensive logging and error reporting

## License
MIT
