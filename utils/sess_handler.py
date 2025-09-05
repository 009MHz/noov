import os
import re
import time
import json
import logging
from filelock import FileLock
from sources.web.admin.login_page import LoginPage

SESSION_FILE = ".auth/session.json"
SESSION_DIR = os.path.dirname(SESSION_FILE)
SESSION_LOCK_FILE = f"{SESSION_FILE}.lock"


class SessionHandler:
    def __init__(self, browser, is_headless):
        self.browser = browser
        self.is_headless = is_headless

    def is_session_expired(self, session_file):
        if not os.path.exists(session_file):
            logging.info("Session file does not exist, creating new session")
            return True

        try:
            with open(session_file, "r") as file:
                session_data = json.load(file)

            if not session_data.get("cookies"):
                return True

            current_time = time.time()
            auth_cookies = [c for c in session_data.get("cookies", []) if c.get("name", "").lower() in ("auth", "session", "token", "jwt")]
            
            # If no auth cookies found, consider it expired
            if not auth_cookies:
                return True
            
            # Check if any authentication cookie is expired
            for cookie in auth_cookies:
                if cookie.get("expires", 0) <= current_time:
                    return True

            return False
            
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error reading session file: {str(e)}")
            return True

    def load_credentials(self, user_type):
        mapping = {
            "user": ["USER_EMAIL", "USER_PASSWORD"],
            "admin": ["ADMIN_EMAIL", "ADMIN_PASSWORD"],
            "super_admin": ["SUPER_ADMIN_EMAIL", "SUPER_ADMIN_PASSWORD"]
        }
        
        # Default to user type if not in mapping
        env_vars = mapping.get(user_type.lower(), ["USER_EMAIL", "USER_PASSWORD"])
        
        # Get credentials from environment variables
        email = os.getenv(env_vars[0])
        password = os.getenv(env_vars[1])
        
        if email and password:
            return email, password
        else:
            raise ValueError(f"Credentials for {user_type} not found. Set {env_vars[0]} and {env_vars[1]} in your .env file.")

    async def create_session(self, user_type: str):
        if not os.path.exists(SESSION_DIR):
            os.makedirs(SESSION_DIR)

        with FileLock(SESSION_LOCK_FILE):
            if not os.path.exists(SESSION_FILE) or self.is_session_expired(SESSION_FILE):
                context_options = {
                    "viewport": {"width": 1920, "height": 1080} if self.is_headless else None,
                    "no_viewport": not self.is_headless}

                context = await self.browser.new_context(**context_options)
                page = await context.new_page()

                if user_type:
                    email, password = self.load_credentials(user_type)
                    sess = LoginPage(page)
                    await sess.open()
                    await sess.login(email, password)
                    
                    # Wait for navigation to confirm login success
                    try:
                        await page.wait_for_url(re.compile(r"/profile"), timeout=5000)
                        await context.storage_state(path=SESSION_FILE)
                    except Exception as e:
                        logging.error(f"Login failed for {user_type}: {str(e)}")
                        # Take a screenshot for debugging
                        os.makedirs(SESSION_DIR, exist_ok=True)
                        await page.screenshot(path=f"{SESSION_DIR}/{user_type}_login_failed.png")
                        raise Exception(f"Failed to login as {user_type}. Check credentials and login page. Screenshot saved to {SESSION_DIR}/{user_type}_login_failed.png")
                    finally:
                        await context.close()

        return SESSION_FILE
