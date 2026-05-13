import random
import time
import logging

logger = logging.getLogger("stealth_utils")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def get_stealth_headers(use_json=True):
    ua = get_random_user_agent()
    headers = {
        "User-Agent": ua,
        "Accept": "application/json" if use_json else "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1", # Do Not Track
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    return headers

def apply_jitter(base_seconds: float, variation: float = 0.5):
    """Sleeps for base_seconds +/- variation."""
    jitter = random.uniform(-variation, variation * 3) # Lean towards longer sleeps to be safe
    total = max(0.1, base_seconds + jitter)
    time.sleep(total)

async def async_jitter(base_seconds: float, variation: float = 0.5):
    """Async version of apply_jitter."""
    import asyncio
    jitter = random.uniform(-variation, variation * 3)
    total = max(0.1, base_seconds + jitter)
    await asyncio.sleep(total)

def get_reddit_compliance_ua(username="unknown_dev"):
    """Format: platform:program_id:version (by /u/username)"""
    return f"windows:finvision_sentinel:v1.2 (by /u/{username})"
