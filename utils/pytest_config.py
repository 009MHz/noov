import pytest
import os
from dotenv import load_dotenv


def pytest_generate_tests_handler(metafunc):
    """Generate tests with platform parameters based on CLI options."""
    # Check if the test function has a platform parameter
    if "platform" in metafunc.fixturenames:
        platform_option = metafunc.config.getoption('platform')
        
        if platform_option == 'mobile':
            # Run only mobile tests
            platforms = ['mobile']
        elif platform_option == 'desktop':
            # Run only desktop tests
            platforms = ['desktop']
        elif platform_option == 'all':
            # Run both desktop and mobile tests
            platforms = ['desktop', 'mobile']
        else:
            # Default behavior: run only desktop tests when no platform specified
            platforms = ['desktop']
        
        metafunc.parametrize("platform", platforms, scope="function")


def configure_environment(config):
    """Configure environment variables from CLI options."""
    # Load environment variables from .env file first
    load_dotenv(override=True)  # Force override existing env vars
    
    # Override with command line options
    os.environ["env"] = config.getoption('env')
    os.environ["mode"] = config.getoption('mode') or 'local'
    os.environ["headless"] = str(config.getoption('headless'))
    
    # Store the platform option for global access
    platform_option = config.getoption('platform')
    config._platform_option = platform_option


def add_pytest_options(parser):
    """Add custom pytest command line options."""
    parser.addoption('--env', action='store', default='test', help='Specify the test environment')
    parser.addoption('--mode', help='Specify the execution mode: local, grid, pipeline', default='local')
    parser.addoption('--platform', help='Specify the platform: desktop, mobile, or all', default='desktop')
    parser.addoption('--headless', action='store_true', default=False, help='Run tests in headless mode')
