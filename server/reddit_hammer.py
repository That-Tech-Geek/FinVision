import os
import json
import asyncio
import logging
import praw
from dotenv import load_dotenv
import requests

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reddit-hammer")

load_dotenv()

def get_instructions():
    return """--- REDDIT API SETUP INSTRUCTIONS ---
1. Visit: https://www.reddit.com/prefs/apps
2. Scroll to the bottom and click [are you a developer? create an app...]
3. Give it a name (e.g., 'FinVision')
4. Select 'script' (This is critical for PRAW!)
5. About URL: http://localhost:8080 (doesn't really matter)
6. Redirect URI: http://localhost:8080
7. Click 'create app'
8. Copy the 'personal use script' ID (under the app name) -> REDDIT_CLIENT_ID
9. Copy the 'secret' -> REDDIT_CLIENT_SECRET
10. Update your .env file and re-run this script!
-----------------------------------------
"""

async def test_praw_connection():
    logger.info("Hammering PRAW...")
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "FinVision v1.0")

    if not client_id or "YOUR_" in client_id:
        logger.error("Reddit Client ID is missing or placeholder.")
        print(get_instructions())
        return False

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        # Test 1: Basic Read
        logger.info("Testing read access...")
        subreddit = reddit.subreddit("stocks")
        for submission in subreddit.hot(limit=1):
            logger.info(f"Success! Connected to r/stocks. Latest: {submission.title}")
            break
        
        # Test 2: Multi-Subreddit
        logger.info("Testing multi-subreddit stream capability...")
        multi = reddit.subreddit("wallstreetbets+stocks+investing")
        # Just check if we can get the display name
        logger.info(f"Multi-subreddit name: {multi.display_name}")
        
        return True
    except Exception as e:
        logger.error(f"PRAW Connection Failed: {e}")
        if "401" in str(e):
            logger.error("Error 401: Unauthorized. Your Client ID or Secret is likely wrong.")
        elif "redirect" in str(e).lower():
            logger.error("Error: Check your Redirect URI in Reddit settings.")
        print(get_instructions())
        return False

async def test_json_fallback():
    logger.info("Hammering Public JSON (No-Auth Fallback)...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        url = "https://www.reddit.com/r/wallstreetbets/hot.json"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            posts = data.get('data', {}).get('children', [])
            if posts:
                logger.info(f"JSON Fallback Success! Found {len(posts)} posts.")
                return True
        logger.warning(f"JSON Fallback failed with status {res.status_code}")
        return False
    except Exception as e:
        logger.error(f"JSON Fallback error: {e}")
        return False

async def main():
    print("\n--- REDDIT HAMMER DIAGNOSTIC ---\n")
    praw_ok = await test_praw_connection()
    
    if not praw_ok:
        print("\nTrying Fallback Method...")
        fallback_ok = await test_json_fallback()
        if fallback_ok:
            print("\nNOTE: Public JSON is working. We can use this as a temporary bridge while you fix the PRAW keys.")
        else:
            print("\nCRITICAL: Both PRAW and Public JSON are failing. Reddit is likely blocking this environment.")
    else:
        print("\nEVERYTHING IS SET! Your Reddit engine is ready for production.")
    
    print("\n------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(main())
