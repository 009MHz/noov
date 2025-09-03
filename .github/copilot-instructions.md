# Copilot Instructions for Test Automation Framework

## Context
You are assisting with building a comprehensive test automation framework with the following specifications:

**Stack:**
- Language: Python
- UI/E2E Testing: Playwright (async methods, modern locators)
- API Testing: Playwright (async method)
- Performance Testing: locust - python
- Mobile Testing: Android & iOS automation (Appium)
- Test Pattern: Page Object Model (POM)
- Reporting: Allure
- CI/CD: GitHub Actions
- Report Hosting: GitHub Pages

## Key Principles
1. **Scalability**: Design for easy expansion across platforms
2. **Modularity**: Separate concerns with clear abstractions
3. **Maintainability**: Follow POM pattern and clean code practices
4. **Modern Approach**: Use async/await, modern Playwright locators
5. **Cross-Platform**: Support Web, Mobile Web, Android, iOS, API

## Code Generation Guidelines

### Structure & Organization
- Create clear separation between page objects, tests, and utilities
- Use async/await for all Playwright operations
- Organize tests by platform and feature

### Playwright Best Practices
- Use modern locators: `page.get_by_role()`, `page.get_by_text()`, `page.get_by_label()`
- Implement auto-waiting strategies
- Use fixtures for setup/teardown
- Configure for multiple browsers and devices

### Page Object Model
- Create base page class with common methods
- Implement platform-specific page classes
- Use composition over inheritance where appropriate
- Encapsulate element interactions

### Testing Patterns
- Use pytest fixtures for test data and configuration
- Implement data-driven testing approaches
- Create reusable test utilities
- Follow AAA pattern (Arrange, Act, Assert)

### CI/CD Integration
- Generate GitHub Actions workflows
- Configure matrix testing for different platforms
- Set up Allure report generation and GitHub Pages deployment
- Include proper artifact handling

### Performance & Mobile
- Suggest performance testing tools integration
- Provide mobile automation setup guidance
- Configure device farms and emulators
- Implement responsive testing strategies

When generating code, prioritize:
1. Type hints and documentation
2. Error handling and logging
3. Configuration management
4. Test data management
5. Parallel execution capabilities

## Test Generation Standards

### Code Quality Standards
- **Locators**: Prioritize user-facing, role-based locators (get_by_role, get_by_label, get_by_text) for resilience and accessibility.
- **Assertions**: Use auto-retrying web-first assertions via the expect API (e.g., expect(page).to_have_title(...)). Avoid expect(locator).to_be_visible() unless specifically testing for a change in an element's visibility, as more specific assertions are generally more reliable.
- **Timeouts**: Rely on Playwright's built-in auto-waiting mechanisms. Avoid hard-coded waits or increased default timeouts.
- **Clarity**: Use descriptive test titles (e.g., def test_navigation_link_works():) that clearly state their intent. Add comments only to explain complex logic, not to describe simple actions like "click a button."

### Test Structure & Organization
- **Imports**: Every test file should begin with from playwright.async_api import Page, expect for async implementation
- **Fixtures**: Use the page: Page fixture as an argument in your test functions to interact with the browser page
- **Setup**: Place navigation steps like page.goto() at the beginning of each test function. For setup actions shared across multiple tests, use standard Pytest fixtures
- **Location**: Store test files in a dedicated tests/ directory organized by platform (web/, mobile/, api/)
- **Naming**: Test files must follow the test_<feature-or-page>.py naming convention
- **Scope**: Aim for one test file per major application feature or page

### Assertion Best Practices
- **Element Counts**: Use expect(locator).to_have_count() to assert the number of elements found by a locator
- **Text Content**: Use expect(locator).to_have_text() for exact text matches and expect(locator).to_contain_text() for partial matches
- **Navigation**: Use expect(page).to_have_url() to verify the page URL
- **Assertion Style**: Prefer `expect` over `assert` for more reliable UI tests

### Test Execution Strategy
1. **Execution**: Tests are run from the terminal using the pytest command
2. **Debug Failures**: Analyze test failures and identify root causes
3. **Parallel Execution**: Configure pytest-xdist for concurrent test runs
4. **Cross-Platform**: Matrix testing for different browsers and devices

### Example Implementation