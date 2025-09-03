# Noovoleum Test Automation Framework

This repository hosts a lightweight automation framework for the Noovoleum platform. It covers Web UI, API, mobile and basic performance scenarios using Python and popular open‑source tools.

## 1. Environment Setup
1. **Prerequisites**
   - Python 3.9+
   - Git
   - Browsers for Playwright (`playwright install` will download Chromium/Firefox/WebKit)
   - Optional Android/iOS emulators for mobile tests

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd noov
   ```

3. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

4. **Install dependencies and browsers**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## 2. Repository Structure
```
.
├── conftest.py            # Pytest fixtures and hooks
├── pytest.ini             # Pytest configuration and markers
├── requirements.txt       # Python dependencies
├── sources/
│   └── web/
│       └── home_page.py   # Playwright page object
├── tests/
│   ├── api/               # HTTP API tests
│   ├── mobile/
│   │   ├── android/       # Android Appium tests
│   │   └── ios/           # iOS Appium tests
│   ├── performance/       # Locust performance script
│   ├── web/
│   │   ├── desktop/       # Desktop web tests
│   │   ├── mobile/        # Responsive web tests
│   │   └── smoke/         # Smoke suite
│   └── test_suites.md     # Manual test cases
├── utils/                 # Helper utilities
│   ├── api_config.py
│   ├── browser_config.py
│   └── sess_handler.py
└── README.md
```

## 3. Test Configuration
- Environment variables are loaded from a `.env` file or your shell at runtime.
- Useful variables:
  - `API_URL` – base URL for API tests (default `https://api.noovoleum.com`).
  - `BROWSER` – Playwright browser (`chromium`, `firefox`, `webkit`).
  - `screenshot` – set to `on` to save screenshots in `reports/`.
  - `USER_EMAIL_*` / `USER_PASSWORD_*` – credentials used when session files are created.
- Pytest command line options:
  - `--env` – logical test environment (`test` by default).
  - `--mode` – execution mode (`local`, `grid`, `pipeline`).
  - `--headless` – run browsers without UI.

## 4. CLI Cheat Sheet
Run tests locally with pytest or locust.

```bash
# Run all tests with Allure results (default)
pytest

# Run tests without generating Allure data
pytest -p no:allure_pytest

# Web UI tests
pytest tests/web

# API tests
pytest tests/api

# Mobile tests
pytest tests/mobile

# Specific markers
pytest -m smoke            # Run smoke tests
pytest -m ui               # Run all web UI tests

# Headless or different environments
pytest --headless --env=staging

# Parallel execution
pytest -n auto

# Performance test (Locust)
locust -f tests/performance/locustfile.py --headless -u 50 -r 5 -t 5m --host https://api.example.com

# Generate and view Allure report
allure serve reports
allure generate reports -o reports/html --clean
```

## License
MIT
