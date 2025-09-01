# Noovoleum Test Automation Framework

This repository contains a sample automation framework for the Noovoleum platform. It demonstrates web, API, mobile and performance testing using Python and common tooling.

## Features
- Web UI automation with Playwright.
- API testing through HTTPX clients.
- Mobile testing via Appium.
- Performance checks with Locust.
- Centralized configuration loaded from YAML files.
- Reporting with pytest's HTML plugin and Allure.

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
Run tests with `pytest` or `locust`.

### Run all pytest suites
```bash
pytest
```

### Web UI tests
```bash
pytest tests/web
```

### Mobile tests
```bash
pytest tests/mobile
```

### Performance tests
```bash
locust -f tests/perf/locustfile.py --headless -u 50 -r 5 -t 5m --host https://api.example.com
```

## Project structure
```
config/                # Environment and device settings
fixtures/              # Reusable pytest fixtures
libs/                  # Shared utilities
sources/
  apis/                # API clients
  web/                 # Web page objects
  mobile/              # Mobile screen objects
tests/
  web/                 # Web UI tests
  mobile/              # Mobile tests
  perf/                # Locust performance scenarios
conftest.py            # Pytest configuration hooks
pytest.ini             # Pytest settings and markers
requirements.txt       # Project dependencies
```

## Configuration
The `load_settings` helper in `libs/config_loader.py` reads YAML files and environment variables to configure test runs.

## License
MIT
