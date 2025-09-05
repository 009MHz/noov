import os
import time
import json
import logging
from filelock import FileLock
# from pages.login.login_page import LoginPage

SESSION_FILE = ".auth/session.json"
SESSION_DIR = os.path.dirname(SESSION_FILE)
SESSION_LOCK_FILE = f"{SESSION_FILE}.lock"


class SessionHandler:
    def __init__(self, browser, is_headless):
        self.browser = browser
        self.is_headless = is_headless

    def is_session_expired(self, session_file):
        if not os.path.exists(session_file):
            return True

        with open(session_file, "r") as file:
            session_data = json.load(file)

        current_time = time.time()
        for cookie in session_data.get("cookies", []):
            if cookie.get("expires", 0) <= current_time:
                return True

        return False

    def load_credentials(self, user_type):
        email = os.getenv(f"USER_EMAIL_{user_type.upper()}")
        password = os.getenv(f"USER_PASSWORD_{user_type.upper()}")

        # If not available, use default testing credentials based on user type
        if not email or not password:
            if user_type.lower() == "user":
                email = "germa69.reiju@gmail.com"
                password = "Test123"
            elif user_type.lower() == "admin":
                email = "harits.satriyo@noovoleum.com" 
                password = "Halo123456"
            # Add more user types as needed
        
        if email and password:
            return email, password
        else:
            raise ValueError(f"Credentials for {user_type} not found and no defaults available")

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
                    pass
                    # email, password = self.load_credentials(user_type)
                    # sess = LoginPage(page)
                    # await sess.create_session(email, password)
                    # logging.info(f"Login Success for {user_type}, Creating the session file . . .")
                    # await context.storage_state(path=SESSION_FILE)
                    # await context.close()

        return SESSION_FILE
