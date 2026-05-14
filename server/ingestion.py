import asyncio
import json
import logging
import time
import nltk
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import websockets
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
import httpx
import praw
import os
from dotenv import load_dotenv
from stealth_utils import get_stealth_headers, async_jitter, get_reddit_compliance_ua

load_dotenv()

logger = logging.getLogger("finvision.ingestion")

class KeyRotator:
    def __init__(self, keys: List[str]):
        self.keys = keys
        self._index = 0

    def get_key(self) -> str:
        if not self.keys:
            return ""
        key = self.keys[self._index]
        self._index = (self._index + 1) % len(self.keys)
        return key

class SentimentProcessor:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        resources = ['tokenizers/punkt', 'tokenizers/punkt_tab']
        for res in resources:
            try:
                nltk.data.find(res)
            except (LookupError, AttributeError):
                resource_name = res.split('/')[-1]
                logger.info(f"Downloading NLTK resource: {resource_name}")
                nltk.download(resource_name, quiet=True)

    def analyze(self, text: str) -> float:
        if not text or not isinstance(text, str): return 0.0
        # Clean text: remove non-printable characters to avoid VADER/TextBlob crashes
        clean_text = "".join(char for char in text if char.isprintable())
        if not clean_text: return 0.0
        
        # Ensemble: 60% VADER (better for short text/social), 40% TextBlob
        try:
            v_score = self.vader.polarity_scores(clean_text)['compound']
            t_score = TextBlob(clean_text).sentiment.polarity
            return (v_score * 0.6) + (t_score * 0.4)
        except Exception as e:
            logger.error(f"Sentiment Analysis failed for text: {e}")
            return 0.0

class FirestoreBatchedWriter:
    def __init__(self, db: AsyncClient, batch_size: int = 50, interval: int = 5, max_queue_size: int = 2000):
        self.db = db
        self.batch_size = batch_size
        self.interval = interval
        self.max_queue_size = max_queue_size
        self.queue = []
        self._lock = asyncio.Lock()

    async def add(self, collection: str, doc_id: Optional[str], data: Dict[str, Any]):
        async with self._lock:
            # Hard limit to prevent memory exhaustion
            if len(self.queue) >= self.max_queue_size:
                if len(self.queue) % 100 == 0: # Log every 100th drop to avoid log spam
                    logger.critical(f"Firestore Queue CIRCUIT BREAKER: {len(self.queue)} items in queue. Dropping new data.")
                return
            
            self.queue.append((collection, doc_id, data))
            
            # Auto-flush if batch size reached
            if len(self.queue) >= self.batch_size:
                await self._flush_unlocked()

    async def flush(self):
        async with self._lock:
            await self._flush_unlocked()

    async def _flush_unlocked(self):
        if not self.queue:
            return
        
        try:
            batch = self.db.batch()
            for collection, doc_id, data in self.queue:
                ref = self.db.collection(collection)
                if doc_id:
                    ref = ref.document(doc_id)
                else:
                    ref = ref.document()
                batch.set(ref, data)
            
            await batch.commit()
            logger.info(f"Batched {len(self.queue)} writes to Firestore.")
            self.queue = []
        except Exception as e:
            logger.error(f"Firestore batch write failed: {e}")
            if len(self.queue) > 500:
                logger.critical(f"Firestore Queue Overflow: {len(self.queue)} items pending. Database may be unreachable!")

    async def run_periodic_flush(self):
        while True:
            await asyncio.sleep(self.interval)
            await self.flush()

class WebSocketManager:
    def __init__(self, url_template: str, key_rotator: KeyRotator, tickers: List[str], message_handler):
        self.url_template = url_template
        self.key_rotator = key_rotator
        self.tickers = tickers
        self.message_handler = message_handler
        self.active = True

    async def connect_and_listen(self):
        retry_delay = 1
        while self.active:
            api_key = self.key_rotator.get_key()
            url = self.url_template.replace("{API_KEY}", api_key)
            
            try:
                logger.info(f"Connecting to {url.split('?')[0]}...")
                async with websockets.connect(url) as ws:
                    retry_delay = 1 # Reset delay on success
                    
                    # Subscribe (Finnhub style)
                    for ticker in self.tickers:
                        await ws.send(json.dumps({"type": "subscribe", "symbol": ticker}))
                    
                    async for message in ws:
                        if not self.active: break
                        await self.message_handler(json.loads(message))
            
            except Exception as e:
                logger.error(f"WebSocket error: {e}. Reconnecting in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60) # Exponential backoff

class RedditStreamer:
    def __init__(self, tickers: List[str], message_handler):
        self.tickers = tickers
        self.message_handler = message_handler
        self.active = True
        
        # Gold Standard Compliance UA
        reddit_username = os.getenv("REDDIT_USERNAME", "unknown_user")
        compliance_ua = get_reddit_compliance_ua(reddit_username)
        
        # Capture loop for thread-safe calls
        self.loop = asyncio.get_event_loop()
        
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID", "YOUR_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET", "YOUR_CLIENT_SECRET"),
            user_agent=compliance_ua
        )

    async def stream(self):
        subreddits = "wallstreetbets+stocks+investing+options+pennystocks+smallcaps+stockmarket"
        
        # Check if we have valid PRAW keys
        client_id = os.getenv("REDDIT_CLIENT_ID")
        if not client_id or "YOUR_" in client_id:
            logger.warning("REDDIT_CLIENT_ID is missing or placeholder. Falling back to PUBLIC JSON POLLING.")
            await self.poll_public_json(subreddits)
            return

        logger.info(f"Starting Reddit PRAW stream for subreddits: {subreddits}")
        
        def process_item(item, is_comment=False):
            try:
                text = (item.body if is_comment else item.title).upper()
                if not is_comment:
                    text += " " + (item.selftext.upper() if item.selftext else "")
                
                for ticker in self.tickers:
                    if f" {ticker} " in f" {text} " or f"${ticker}" in text:
                        asyncio.run_coroutine_threadsafe(
                            self.message_handler({
                                "type": "social",
                                "ticker": ticker,
                                "text": item.body if is_comment else item.title,
                                "platform": "reddit",
                                "is_comment": is_comment,
                                "link": f"https://reddit.com{item.permalink}"
                            }),
                            self.loop
                        )
            except Exception as e:
                logger.error(f"Error processing Reddit item: {e}")

        def stream_submissions():
            try:
                for submission in self.reddit.subreddit(subreddits).stream.submissions(skip_existing=True):
                    if not self.active: break
                    process_item(submission, is_comment=False)
            except Exception as e:
                logger.error(f"Reddit Submission Stream Error: {e}")
                # If stream fails, we could trigger the fallback here too

        def stream_comments():
            try:
                for comment in self.reddit.subreddit(subreddits).stream.comments(skip_existing=True):
                    if not self.active: break
                    process_item(comment, is_comment=True)
            except Exception as e:
                logger.error(f"Reddit Comment Stream Error: {e}")

        async def supervisor(func, name):
            retry_wait = 5
            while self.active:
                try:
                    logger.info(f"Starting Reddit {name} stream thread...")
                    await asyncio.to_thread(func)
                except Exception as e:
                    logger.error(f"Reddit {name} stream failed: {e}. Restarting in {retry_wait}s...")
                    await asyncio.sleep(retry_wait)
                    retry_wait = min(retry_wait * 2, 300)

        # Run both streams in supervisor loops
        await asyncio.gather(
            supervisor(stream_submissions, "Submissions"),
            supervisor(stream_comments, "Comments")
        )

    async def poll_public_json(self, subreddits: str):
        """No-auth fallback that polls the .json endpoints with stealth headers and jitter."""
        subs_list = subreddits.split("+")
        
        async with httpx.AsyncClient() as client:
            while self.active:
                headers = get_stealth_headers(use_json=True)
                
                for sub in subs_list:
                    try:
                        url = f"https://www.reddit.com/r/{sub}/new.json?limit=25&t={int(time.time())}"
                        res = await client.get(url, headers=headers, timeout=10.0)
                        
                        if res.status_code == 200:
                            data = res.json()
                            posts = data.get('data', {}).get('children', [])
                            for post in posts:
                                pdata = post.get('data', {})
                                text = (pdata.get('title', '') + " " + pdata.get('selftext', '')).upper()
                                for ticker in self.tickers:
                                    if f" {ticker} " in f" {text} " or f"${ticker}" in text:
                                        await self.message_handler({
                                            "type": "social",
                                            "ticker": ticker,
                                            "text": pdata.get('title'),
                                            "platform": "reddit-json-fallback",
                                            "link": f"https://reddit.com{pdata.get('permalink')}"
                                        })
                        elif res.status_code == 429:
                            logger.warning(f"Rate limited (429) on r/{sub}. Backing off.")
                            await asyncio.sleep(60)
                        else:
                            logger.warning(f"Reddit JSON Fallback for r/{sub} failed: {res.status_code}")
                    except Exception as e:
                        logger.error(f"Reddit JSON Fallback Error for r/{sub}: {e}")
                    
                    await async_jitter(3.0, 1.5)
                
                await async_jitter(300, 30)

class IngestionEngine:
    def __init__(self, db: AsyncClient, tickers: List[str], api_keys: List[str]):
        self.db = db
        self.tickers = tickers
        self.processor = SentimentProcessor()
        self.writer = FirestoreBatchedWriter(db)
        self.key_rotator = KeyRotator(api_keys)
        self.is_running = False
        
        # Finnhub template
        self.manager = WebSocketManager(
            url_template="wss://ws.finnhub.io?token={API_KEY}",
            key_rotator=self.key_rotator,
            tickers=tickers,
            message_handler=self.handle_message
        )
        self.reddit_streamer = RedditStreamer(tickers, self.handle_message)

    async def handle_message(self, msg: Dict[str, Any]):
        # Handle Trade/Price data
        if msg.get("type") == "trade":
            for trade in msg.get("data", []):
                ticker = trade.get("s")
                # Price data doesn't have sentiment, so we log it or update a price field
                # For this dashboard, we focus on sentiment.
                pass
        
        # Handle News/Social data (Simulated or from other WS)
        elif msg.get("type") == "news" or msg.get("type") == "social":
            ticker = msg.get("ticker", "UNKNOWN")
            text = msg.get("text", "")
            if not text: return

            score = self.processor.analyze(text)
            timestamp = datetime.now(timezone.utc)

            # 1. Add to Historical
            await self.writer.add("sentimentHistorical", None, {
                "ticker": ticker,
                "timestamp": timestamp,
                "score": score,
                "text": text,
                "platform": msg.get("platform", "websocket")
            })

            # 2. Add to Latest
            await self.writer.add("sentimentLatest", ticker, {
                "ticker": ticker,
                "timestamp": timestamp,
                "score": score
            })

            # 3. Add to Raw
            await self.writer.add("rawMentions", None, {
                "ticker": ticker,
                "timestamp": timestamp,
                "text": text,
                "sentiment_score": score,
                "platform": msg.get("platform", "websocket")
            })

    async def run_simulator(self):
        """Simulates incoming social media mentions for demonstration purposes."""
        import random
        headlines = [
            "Just bought more {ticker}, looks like a breakout! 📈",
            "Not sure about {ticker}'s latest earnings report...",
            "The market is sleeping on {ticker}'s potential. 🚀",
            "Bearish sentiment growing for {ticker} due to supply chain issues.",
            "Incredible growth expected for {ticker} in Q3!",
            "Anyone else seeing the double bottom on {ticker}?",
            "Regulators are looking into {ticker} again. 📉"
        ]
        while True:
            await asyncio.sleep(random.randint(2, 8))
            ticker = random.choice(self.tickers)
            text = random.choice(headlines).format(ticker=ticker)
            await self.handle_message({
                "type": "social",
                "ticker": ticker,
                "text": text,
                "platform": "fin-twitter-stream"
            })

    async def start(self):
        self.is_running = True
        tasks = [
            self.writer.run_periodic_flush()
        ]
        
        # Only try live WS if we have keys (not placeholders)
        valid_keys = [k for k in self.key_rotator.keys if k and "YOUR_" not in k]
        if valid_keys:
            tasks.append(self.manager.connect_and_listen())
        else:
            logger.warning("No valid API keys found. Running in SIMULATOR mode.")
            tasks.append(self.run_simulator())
        
        # Start Reddit streaming if keys exist
        reddit_id = os.getenv("REDDIT_CLIENT_ID", "")
        if reddit_id and "YOUR_" not in reddit_id:
            tasks.append(self.reddit_streamer.stream())
            
        await asyncio.gather(*tasks)

    def stop(self):
        self.is_running = False
        self.manager.active = False
