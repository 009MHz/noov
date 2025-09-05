import asyncio
import sys
import logging
from playwright.async_api import async_playwright
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
