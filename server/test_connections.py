import os
import json
import asyncio
import logging
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
import requests
import praw
from dotenv import load_dotenv

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tester")

load_dotenv()

async def test_firestore():
    logger.info("Testing Firestore...")
    try:
        sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
        if sa_path and os.path.exists(sa_path):
            with open(sa_path) as f:
                info = json.load(f)
            cred = credentials.Certificate(sa_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            # EXPLICITLY PASS CREDENTIALS
            db = firestore.Client(project=info['project_id'], credentials=cred.get_credential())
            logger.info(f"[OK] Firestore initialized with SA file for project: {info['project_id']}")
        else:
            db = firestore.Client()
            logger.info("[WARN] Firestore initialized with default credentials.")
        
        # Test write
        test_ref = db.collection("test_connectivity").document("test")
        test_ref.set({"status": "connected", "time": firestore.SERVER_TIMESTAMP})
        logger.info("[OK] Firestore write successful.")
        
        # Test read
        doc = test_ref.get()
        if doc.exists:
            logger.info(f"[OK] Firestore read successful: {doc.to_dict()}")
        
        return True
    except Exception as e:
        logger.error(f"[FAIL] Firestore test failed: {e}")
        return False

def test_finnhub():
    logger.info("Testing Finnhub Keys...")
    keys = [os.getenv(f"FINNHUB_API_KEY_{i}") for i in range(1, 6)]
    keys = [k for k in keys if k]
    
    if not keys:
        logger.warning("No Finnhub keys found in .env")
        return False

    success_count = 0
    for i, key in enumerate(keys):
        try:
            url = f"https://finnhub.io/api/v1/stock/profile2?symbol=AAPL&token={key}"
            res = requests.get(url)
            if res.status_code == 200:
                logger.info(f"[OK] Finnhub Key {i+1} is valid.")
                success_count += 1
            else:
                logger.error(f"[FAIL] Finnhub Key {i+1} failed with status {res.status_code}")
        except Exception as e:
            logger.error(f"[FAIL] Finnhub Key {i+1} error: {e}")
    
    return success_count > 0

def test_polygon():
    logger.info("Testing Polygon Keys...")
    keys = [os.getenv(f"POLYGON_API_KEY_{i}") for i in range(1, 4)]
    keys = [k for k in keys if k]
    
    if not keys:
        logger.warning("No Polygon keys found in .env")
        return False

    success_count = 0
    for i, key in enumerate(keys):
        try:
            url = f"https://api.polygon.io/v3/reference/tickers/AAPL?apiKey={key}"
            res = requests.get(url)
            if res.status_code == 200:
                logger.info(f"[OK] Polygon Key {i+1} is valid.")
                success_count += 1
            else:
                logger.error(f"[FAIL] Polygon Key {i+1} failed with status {res.status_code}")
        except Exception as e:
            logger.error(f"[FAIL] Polygon Key {i+1} error: {e}")
    
    return success_count > 0

def test_reddit():
    logger.info("Testing Reddit...")
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not client_id or "YOUR_" in client_id:
        logger.warning("Reddit keys are placeholders. Use 'python reddit_hammer.py' for setup guide.")
        return "SKIPPED (Use reddit_hammer.py)"
    
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=os.getenv("REDDIT_USER_AGENT", "FinVision Tester")
        )
        for submission in reddit.subreddit("stocks").hot(limit=1):
            logger.info(f"[OK] Reddit connected. Latest post: {submission.title}")
            break
        return "OK"
    except Exception as e:
        logger.error(f"[FAIL] Reddit test failed: {e}")
        logger.info("Tip: Run 'python reddit_hammer.py' for a detailed diagnostic.")
        return "FAIL"

async def main():
    print("\n--- FinVision Connectivity Diagnostics ---\n")
    fs_ok = await test_firestore()
    fh_ok = test_finnhub()
    pg_ok = test_polygon()
    rd_status = test_reddit()
    
    print("\n--- Summary ---")
    print(f"Firestore: {'OK' if fs_ok else 'FAIL'}")
    print(f"Finnhub:   {'OK' if fh_ok else 'FAIL'}")
    print(f"Polygon:    {'OK' if pg_ok else 'FAIL'}")
    print(f"Reddit:     {rd_status}")
    print("----------------\n")

if __name__ == "__main__":
    asyncio.run(main())
