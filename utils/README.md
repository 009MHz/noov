# Utilities for the Test Automation Framework

## Allure Helpers

The `allure_helpers.py` module provides properly typed wrappers for Allure functionality.

### Step Context Manager

The `step()` function provides a properly typed context manager for Allure steps that works well with static type checking.

#### Usage:

```python
from utils.allure_helpers import step

async def test_example(page):
    with step("Step description"):
        # Actions to perform in this step
        await page.click("button")
        
    with step("Another step"):
        # More actions
        await page.fill("input", "text")
```

#### Benefits:

1. **Type Safety**: No more type checking errors that require `# type: ignore` comments
2. **Clean Code**: Maintains readability without cluttering the code with ignores
3. **IDE Support**: Full IDE support for code completion and refactoring
4. **Allure Integration**: Steps appear correctly in Allure reports

### Why Use This Instead of Direct `allure.step` Calls:

- The direct `allure.step()` function doesn't have proper type annotations for context manager usage
- Using our wrapper ensures consistent step reporting throughout the test suite
- Removes the need for `# type: ignore` comments while keeping all the benefits
