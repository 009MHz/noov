#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logging.info(f"Loaded environment from {dotenv_path}")
else:
    logging.warning(f".env file not found at {dotenv_path}")

# Add project root to Python path to allow imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.sess_handler import SessionHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def setup_session(user_types=None):
    if user_types is None:
        user_types = ["user", "admin"]
    elif isinstance(user_types, str):
        user_types = [user_types]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        handler = SessionHandler(browser, is_headless=True)
        
        # Process each user type sequentially
        for user_type in user_types:
            try:
                logging.info(f"Creating session for {user_type}...")
                session_file = await handler.create_session(user_type)
                logging.info(f"✅ Session for {user_type} created successfully at {session_file}")
            except Exception as e:
                logging.error(f"❌ Failed to create session for {user_type}: {str(e)}")

        await browser.close()
    
    logging.info("Session setup completed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "all" or len(sys.argv) == 1:
            user_types = ["user", "admin"]
        else:
            user_types = sys.argv[1:]
    else:
        user_types = ["user", "admin"] 
    # Run the session setup
    asyncio.run(setup_session(user_types))
