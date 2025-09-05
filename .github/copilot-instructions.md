# Copilot Instructions for Test Automation Framework

## Framework Stack
- **Language**: Python with async/await
- **Testing**: Playwright (Web/API), Appium (Mobile), Locust (Performance)
- **Pattern**: Page Object Model (POM)
- **Reporting**: Allure with GitHub Pages hosting
- **CI/CD**: GitHub Actions with matrix testing

## Core Principles
1. **Scalability**: Multi-platform support (Web, Mobile, API)
2. **Modularity**: Clear separation of concerns with clean abstractions
3. **Maintainability**: Modern locators, auto-waiting, comprehensive documentation
4. **Quality**: Type hints, error handling, parallel execution
5. **Validity**: Always run the test whenever the code is changed

## Development Standards

### Project Structure
```
tests/
├── web/          # Web UI tests
├── mobile/       # Mobile app tests
└── api/          # API tests
sources/
├── web/          # Web page objects
├── mobile/       # Mobile page objects
└── api/          # API clients
utils/            # Shared utilities and fixtures
```

### Code Requirements
- **Async Operations**: Use async/await for all Playwright interactions
- **Modern Locators**: Prioritize `get_by_role()`, `get_by_text()`, `get_by_label()`
- **Type Hints**: Include comprehensive type annotations
- **Documentation**: Document complex logic, not simple actions
- **Error Handling**: Implement robust error handling and logging

### Test Implementation

#### File Organization
- **Naming**: `test_<feature>.py` convention
- **Location**: Platform-specific directories (`tests/web/`, `tests/api/`, etc.)
- **Scope**: One test file per major feature or page

#### Required Imports
```python
from playwright.async_api import Page, expect
```

#### Test Structure
- **Setup**: Use `page.goto()` at test start; shared setup via pytest fixtures
- **Pattern**: Follow AAA (Arrange, Act, Assert) pattern
- **Focus**: One test per feature/user story for better maintainability

#### Locators & Interactions
- **Priority Order**: `get_by_role()` > `get_by_label()` > `get_by_text()` > CSS selectors
- **Auto-waiting**: Rely on Playwright's built-in waiting mechanisms
- **Timeouts**: Avoid hard-coded waits; use default timeouts

#### Assertions
- **Test Script Location**: Keep all assertions in test scripts, NOT in page objects
- **Separation of Concerns**: Page objects should return elements/data; tests should verify behavior
- **Priority**: Prioritize the `expect` syntax from playwright before using any assertions
- **Counts**: `expect(locator).to_have_count()` for element quantities
- **Text Matching**: `to_have_text()` (exact) vs `to_contain_text()` (partial)
- **Navigation**: `expect(page).to_have_url()` for URL verification
- **Avoid**: `expect(locator).to_be_visible()` unless testing visibility changes

#### Page Object Model
- **Encapsulation**: Wrap element interactions in methods that return data/elements
- **No Assertions**: Page objects should NOT contain assertions or test logic
- **Return Values**: Methods should return elements, text, or boolean states for test verification
- **Platform-specific**: Separate classes for web/mobile implementations
- **Composition**: Prefer composition over inheritance
- **Reusability**: Create shared base classes for common functionality

#### Test-Page Object Interaction Pattern
```python
# ✅ Correct: Assertion in test script
def test_login_success(page: Page):
    login_page = LoginPage(page)
    login_page.fill_credentials("user", "pass")
    login_page.click_login()
    
    # Assertions belong in test
    expect(page).to_have_url("/dashboard")
    expect(login_page.get_welcome_message()).to_contain_text("Welcome")

# ❌ Incorrect: Assertion in page object
class LoginPage:
    def verify_login_success(self):
        expect(self.page).to_have_url("/dashboard")  # Don't do this
```

### Execution & CI/CD
- **Local**: Run tests via `pytest` command
- **Parallel**: Configure `pytest-xdist` for concurrent execution
- **Matrix Testing**: Support multiple browsers, devices, and platforms
- **Reporting**: Generate Allure reports with artifact handling
- **Deployment**: Auto-deploy reports to GitHub Pages
