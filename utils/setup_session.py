#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
from typing import List, Optional, Union
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from pathlib import Path
from utils.sess_handler import SessionHandler


dotenv_path = Path(__file__).parent.parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)
    logging.info(f"Loaded environment from {dotenv_path}")
else:
    logging.warning(f".env file not found at {dotenv_path}")

project_root = str(Path(__file__).parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)


async def setup_session(user_types: Optional[Union[str, List[str]]] = None) -> None:
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
    if len(sys.argv) == 1:
        user_types = ["user", "admin"]
    elif sys.argv[1].lower() == "all":
        user_types = ["user", "admin"]
    else:
        user_types = sys.argv[1:]
    # Run the session setup
    asyncio.run(setup_session(user_types))
