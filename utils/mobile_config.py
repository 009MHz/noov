import contextlib
import os
import asyncio
from typing import Dict, Any, Optional, Callable, TypeVar, Awaitable
from dataclasses import dataclass
from functools import wraps
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.options.ios.xcuitest.base import XCUITestOptions

# Type variables for async bridge
T = TypeVar('T')


async def ensure_native_app_context(driver):
    """
    Switch to NATIVE_APP context if not already set. Safe for async/await usage.
    """
    try:
        current = getattr(driver, 'current_context', 'NATIVE_APP')
        if current != 'NATIVE_APP':
            # Some drivers may require sync context switch
            with contextlib.suppress(Exception):
                driver.switch_to.context('NATIVE_APP')
    except Exception:
        pass
    
    
def aify(sync_func: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    """
    Async bridge decorator for Appium synchronous methods.
    
    Converts synchronous Appium driver calls to async-compatible functions
    using asyncio.to_thread to prevent blocking the event loop.
    
    Args:
        sync_func: Synchronous function to make async-compatible
        
    Returns:
        Async wrapper function
        
    Example:
        @aify
        def _click_element(self, element):
            element.click()
            
        # Usage: await self._click_element(element)
    """
    @wraps(sync_func)
    async def async_wrapper(*args, **kwargs) -> T:
        # Use asyncio.to_thread to run sync function in thread pool
        return await asyncio.to_thread(sync_func, *args, **kwargs)
    
    return async_wrapper


class AsyncBridge:
    """
    Utility class providing common async bridge methods for mobile automation.
    
    This class contains pre-wrapped common Appium operations that mobile
    screen objects can inherit from or use as a mixin.
    """
    
    @staticmethod
    @aify
    def _sync_find_element(driver, by: str, value: str):
        """Find element synchronously."""
        return driver.find_element(by, value)
    
    @staticmethod
    @aify
    def _sync_find_elements(driver, by: str, value: str):
        """Find elements synchronously."""
        return driver.find_elements(by, value)
    
    @staticmethod
    @aify
    def _sync_tap(element):
        """Tap element synchronously."""
        element.click()
    
    @staticmethod
    @aify
    def _sync_type(element, text: str, clear_first: bool = True):
        """Type text synchronously."""
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    @staticmethod
    @aify
    def _sync_get_text(element) -> str:
        """Get element text synchronously."""
        return element.text
    
    @staticmethod
    @aify
    def _sync_get_attribute(element, attribute: str) -> Optional[str]:
        """Get element attribute synchronously."""
        return element.get_attribute(attribute)
    
    @staticmethod
    @aify
    def _sync_is_displayed(element) -> bool:
        """Check if element is displayed synchronously."""
        return element.is_displayed()
    
    @staticmethod
    @aify
    def _sync_is_enabled(element) -> bool:
        """Check if element is enabled synchronously."""
        return element.is_enabled()
    
    @staticmethod
    @aify
    def _sync_get_page_source(driver) -> str:
        """Get page source synchronously."""
        return driver.page_source
    
    @staticmethod
    @aify
    def _sync_navigate(driver, url: str):
        """Navigate to URL synchronously."""
        driver.get(url)
    
    @staticmethod
    @aify
    def _sync_back(driver):
        """Go back synchronously."""
        driver.back()
    
    @staticmethod
    @aify
    def _sync_refresh(driver):
        """Refresh page synchronously."""
        driver.refresh()
    
    @staticmethod
    @aify
    def _sync_screenshot(driver, filename: Optional[str] = None) -> str:
        """Take screenshot synchronously."""
        if filename:
            driver.save_screenshot(filename)
            return filename
        else:
            return driver.get_screenshot_as_base64()
    
    @staticmethod
    @aify
    def _sync_switch_context(driver, context: str):
        """Switch context synchronously."""
        driver.switch_to.context(context)
    
    @staticmethod
    @aify
    def _sync_get_contexts(driver) -> list:
        """Get available contexts synchronously."""
        return list(driver.contexts)


@dataclass
class MobileDeviceConfig:
    """Configuration for a mobile device."""
    platform: str
    device_name: str
    automation_name: str
    browser_name: Optional[str] = None
    app_package: Optional[str] = None
    app_activity: Optional[str] = None
    app_path: Optional[str] = None
    udid: Optional[str] = None
    system_port: Optional[int] = None
    wda_port: Optional[int] = None


class MobileConfig:
    """Mobile testing configuration manager."""
    
    def __init__(self):
        self.appium_server_url = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
        self.default_timeout = int(os.getenv("MOBILE_TIMEOUT", "30"))
        self.implicit_wait = int(os.getenv("MOBILE_IMPLICIT_WAIT", "10"))
        self.command_timeout = int(os.getenv("MOBILE_COMMAND_TIMEOUT", "120"))
    
    def get_android_browser_config(self) -> Dict[str, Any]:
        """Get Android Chrome browser configuration."""
        return {
            "platform_name": "Android",
            "automation_name": "UiAutomator2",
            "device_name": os.getenv("ANDROID_DEVICE", "Android Emulator"),
            "browser_name": "Chrome",
            "new_command_timeout": self.command_timeout,
            "no_reset": True,
            "full_reset": False,
            "implicit_wait": self.implicit_wait,
            # Chrome-specific options
            "goog:chromeOptions": {
                "w3c": False,  # Legacy protocol for better compatibility
                "args": [
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-default-apps"
                ]
            }
        }
    
    def get_android_app_config(self, app_package: str, app_activity: str) -> Dict[str, Any]:
        """Get Android native app configuration."""
        return {
            "platform_name": "Android",
            "automation_name": "UiAutomator2",
            "device_name": os.getenv("ANDROID_DEVICE", "Android Emulator"),
            "app_package": app_package,
            "app_activity": app_activity,
            "new_command_timeout": self.command_timeout,
            "no_reset": True,
            "full_reset": False,
            "implicit_wait": self.implicit_wait
        }
    
    def get_ios_browser_config(self) -> Dict[str, Any]:
        """Get iOS Safari browser configuration."""
        return {
            "platform_name": "iOS",
            "automation_name": "XCUITest",
            "device_name": os.getenv("IOS_DEVICE", "iPhone Simulator"),
            "browser_name": "Safari",
            "new_command_timeout": self.command_timeout,
            "no_reset": True,
            "implicit_wait": self.implicit_wait
        }
    
    def get_ios_app_config(self, bundle_id: str, app_path: Optional[str] = None) -> Dict[str, Any]:
        """Get iOS native app configuration."""
        config = {
            "platform_name": "iOS",
            "automation_name": "XCUITest",
            "device_name": os.getenv("IOS_DEVICE", "iPhone Simulator"),
            "bundle_id": bundle_id,
            "new_command_timeout": self.command_timeout,
            "no_reset": True,
            "implicit_wait": self.implicit_wait
        }
        
        if app_path:
            config["app"] = app_path
            
        return config
    
    def create_android_options(self, config_type: str = "browser") -> UiAutomator2Options:
        """Create Android UiAutomator2 options."""
        options = UiAutomator2Options()
        
        if config_type == "browser":
            config = self.get_android_browser_config()
        else:
            # For native apps, you'd pass app_package and app_activity
            config = self.get_android_browser_config()  # Default to browser
        
        # Set all capabilities
        for key, value in config.items():
            if key == "goog:chromeOptions":
                options.set_capability(key, value)
            else:
                setattr(options, key, value)
        
        return options
    
    def create_ios_options(self, config_type: str = "browser") -> XCUITestOptions:
        """Create iOS XCUITest options."""
        options = XCUITestOptions()
        
        if config_type == "browser":
            config = self.get_ios_browser_config()
        else:
            # For native apps, you'd pass bundle_id
            config = self.get_ios_browser_config()  # Default to browser
        
        # Set all capabilities
        for key, value in config.items():
            setattr(options, key, value)
        
        return options


class AndroidConfig(MobileConfig):
    """Android-specific configuration."""
    
    def __init__(self):
        super().__init__()
        self.device_name = os.getenv("ANDROID_DEVICE", "Android Emulator")
        self.udid = os.getenv("ANDROID_UDID")
        self.system_port = os.getenv("ANDROID_SYSTEM_PORT")
        self.chrome_driver_port = os.getenv("CHROME_DRIVER_PORT")
    
    def get_real_device_config(self) -> Dict[str, Any]:
        """Get configuration for real Android device."""
        config = self.get_android_browser_config()
        
        if self.udid:
            config["udid"] = self.udid
        
        if self.system_port:
            config["system_port"] = int(self.system_port)
            
        if self.chrome_driver_port:
            config["chrome_driver_port"] = int(self.chrome_driver_port)
        
        # Real device specific settings
        config["device_name"] = self.device_name
        config["no_reset"] = True
        config["skip_unlock"] = True  # Skip device unlock
        config["skip_log_capture"] = False  # Capture logs
        
        return config


class IOSConfig(MobileConfig):
    """iOS-specific configuration."""
    
    def __init__(self):
        super().__init__()
        self.device_name = os.getenv("IOS_DEVICE", "iPhone Simulator")
        self.udid = os.getenv("IOS_UDID")
        self.wda_port = os.getenv("WDA_PORT")
        self.xcode_org_id = os.getenv("XCODE_ORG_ID")
        self.xcode_signing_id = os.getenv("XCODE_SIGNING_ID")
    
    def get_real_device_config(self) -> Dict[str, Any]:
        """Get configuration for real iOS device."""
        config = self.get_ios_browser_config()
        
        if self.udid:
            config["udid"] = self.udid
        
        if self.wda_port:
            config["wda_local_port"] = int(self.wda_port)
        
        if self.xcode_org_id:
            config["xcode_org_id"] = self.xcode_org_id
            
        if self.xcode_signing_id:
            config["xcode_signing_id"] = self.xcode_signing_id
        
        # Real device specific settings
        config["device_name"] = self.device_name
        config["no_reset"] = True
        config["start_iwdp"] = True  # Start iOS WebKit Debug Proxy
        
        return config


# Global configuration instances
mobile_config = MobileConfig()
android_config = AndroidConfig()
ios_config = IOSConfig()


# Convenience functions
def get_android_driver_options() -> UiAutomator2Options:
    """Get Android driver options for browser testing."""
    return android_config.create_android_options("browser")


def get_ios_driver_options() -> XCUITestOptions:
    """Get iOS driver options for browser testing."""
    return ios_config.create_ios_options("browser")


def get_appium_server_url() -> str:
    """Get Appium server URL."""
    return mobile_config.appium_server_url


def get_mobile_timeouts() -> Dict[str, int]:
    """Get mobile testing timeouts."""
    return {
        "default": mobile_config.default_timeout,
        "implicit": mobile_config.implicit_wait,
        "command": mobile_config.command_timeout
    }


# Environment validation
def validate_mobile_environment() -> Dict[str, bool]:
    """Validate mobile testing environment setup."""
    checks = {
        "appium_server_configured": bool(os.getenv("APPIUM_SERVER")),
        "android_device_configured": bool(os.getenv("ANDROID_DEVICE")),
        "ios_device_configured": bool(os.getenv("IOS_DEVICE")),
        "android_udid_set": bool(os.getenv("ANDROID_UDID")),
        "ios_udid_set": bool(os.getenv("IOS_UDID"))
    }
    
    return checks


def print_mobile_config_summary():
    """Print mobile configuration summary for debugging."""
    print("🔧 Mobile Testing Configuration:")
    print(f"📱 Appium Server: {mobile_config.appium_server_url}")
    print(f"🤖 Android Device: {android_config.device_name}")
    print(f"🍎 iOS Device: {ios_config.device_name}")
    print(f"⏱️  Default Timeout: {mobile_config.default_timeout}s")
    print(f"⏳ Command Timeout: {mobile_config.command_timeout}s")
    
    validation = validate_mobile_environment()
    print("\n✅ Environment Status:")
    for check, status in validation.items():
        status_emoji = "✅" if status else "❌"
        print(f"{status_emoji} {check.replace('_', ' ').title()}")
