import os
import pytest


@pytest.fixture(scope='class')
def credentials():
    """Centralized fixture for all environment variables used in tests"""
    return {
        # User credentials
        "user_email": os.getenv("USER_EMAIL"),
        "user_password": os.getenv("USER_PASSWORD"),
        
        # Admin credentials
        "admin_email": os.getenv("ADMIN_EMAIL"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        
        # 2FA credentials
        "user_2fa_email": os.getenv("USER_2FA_EMAIL"),
        "user_2fa_password": os.getenv("USER_2FA_PASSWORD"),
        "user_2fa_code": os.getenv("USER_2FA_CODE"),
        
        # Test data
        "invalid_email": os.getenv("INVALID_TEST_EMAIL", "invalid@example.com"),
        "invalid_format_email": os.getenv("INVALID_FORMAT_EMAIL", "test@example"),
        "invalid_tfa_code": os.getenv("INVALID_TFA_CODE", "000000"),
        "test_email": os.getenv("TEST_EMAIL", "test@example.com")
    }
