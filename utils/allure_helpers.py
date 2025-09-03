import allure
from typing import Any, Generator, Iterator, TypeVar, cast
from contextlib import contextmanager

T = TypeVar('T')

@contextmanager
def step(title: str) -> Iterator[None]:
    """
    A properly typed wrapper for allure.step that can be used as a context manager.
    
    Args:
        title: The title of the step to be shown in the report
        
    Example:
        ```python
        from utils.allure_helpers import step
        
        with step("My step description"):
            # actions to perform in this step
        ```
    """
    # Using cast to satisfy type checker while still using the underlying allure step
    allure_step = cast(Any, allure.step(title))
    allure_step.__enter__()
    try:
        yield None
    finally:
        allure_step.__exit__(None, None, None)
