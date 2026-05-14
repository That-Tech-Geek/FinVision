import logging
import os
import json
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
import yfinance as yf
from textblob import TextBlob
from pydantic import BaseModel, field_validator
import firebase_admin
from firebase_admin import auth, credentials
import praw
from dotenv import load_dotenv
from ingestion import IngestionEngine, SentimentProcessor
from stealth_utils import get_reddit_compliance_ua, get_stealth_headers

# Load environment variables from .env
load_dotenv()

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("finvision")

# --- Configuration ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "finvision-68f62")
COLLECTION_HISTORICAL = "sentimentHistorical"
COLLECTION_LATEST = "sentimentLatest"
COLLECTION_RAW = "rawMentions"

# Initialize Firestore client
try:
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    if service_account_path and os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        # Explicitly pass credentials
        db = AsyncClient(project=PROJECT_ID, credentials=cred.get_credential())
        logger.info(f"Firestore initialized with Service Account file: {service_account_path}")
    else:
        # Fallback to JSON string if provided (for cloud deployments)
        service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        if service_account_json:
            service_account_info = json.loads(service_account_json)
            if "private_key" in service_account_info:
                service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(service_account_info)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = AsyncClient(project=service_account_info.get('project_id', PROJECT_ID))
            logger.info("Firestore initialized with Service Account JSON string")
        else:
            # Fallback to ADC
            db = AsyncClient(project=PROJECT_ID)
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            logger.info(f"Firestore initialized with ADC for project: {PROJECT_ID}")
except Exception as e:
    logger.error(f"Critical: Could not initialize Firebase: {e}")
    db = None

# --- Ingestion Configuration ---
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH"]

# Load all available Finnhub keys
FINNHUB_KEYS = [
    os.getenv(f"FINNHUB_API_KEY_{i}") for i in range(1, 6)
]
FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k]  # Filter out None

# Load all available Polygon keys
POLYGON_KEYS = [
    os.getenv(f"POLYGON_API_KEY_{i}") for i in range(1, 4)
]
POLYGON_KEYS = [k for k in POLYGON_KEYS if k]

# Fallback to single key if numbered ones aren't set
if not FINNHUB_KEYS and os.getenv("FINNHUB_API_KEY"):
    FINNHUB_KEYS = [os.getenv("FINNHUB_API_KEY")]

ingestion_engine = None
sentiment_processor = SentimentProcessor()

# --- Lifespan (replaces deprecated @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ingestion_engine
    # Startup
    if db:
        ingestion_engine = IngestionEngine(db, TICKERS, FINNHUB_KEYS)
        asyncio.create_task(ingestion_engine.start())
        logger.info(f"Ingestion Engine started with {len(FINNHUB_KEYS)} Finnhub keys")
    yield
    # Shutdown
    if ingestion_engine:
        ingestion_engine.stop()
        logger.info("Ingestion Engine stopped")

app = FastAPI(title="FinVision Sentiment Engine", lifespan=lifespan)

# CORS — lock down to known origins in production
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",")] if _raw_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
# --- Security Middleware ---
async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    id_token = auth_header.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

class TickerBatch(BaseModel):
    tickers: List[str]

    @field_validator("tickers")
    @classmethod
    def validate_tickers(cls, v):
        if not v:
            raise ValueError("Ticker list cannot be empty")
        return [t.upper().strip() for t in v]

# --- Sentiment Analysis ---
# --- Sentiment Analysis ---
def analyze_sentiment(text: str) -> float:
    """Analyze sentiment using the ensemble processor."""
    return sentiment_processor.analyze(text)

# --- Sentiment Sources ---
class SentimentSource:
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

class YFinanceSource(SentimentSource):
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        try:
            t = yf.Ticker(ticker)
            # Run blocking news fetch in a thread pool to avoid freezing the event loop
            news = await asyncio.to_thread(lambda: t.news)
            if not news: return []
            return [{
                "title": item.get("title"),
                "platform": "yfinance",
                "link": item.get("link"),
                "publisher": item.get("publisher"),
                "time": item.get("providerPublishTime")
            } for item in news]
        except Exception as e:
            logger.error(f"YFinance fetch error for {ticker}: {e}")
            return []

class RedditSource(SentimentSource):
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit = None
        if self.client_id and "YOUR_" not in self.client_id:
            try:
                # Use Gold Standard Compliance UA
                reddit_username = os.getenv("REDDIT_USERNAME", "unknown_user")
                compliance_ua = get_reddit_compliance_ua(reddit_username)
                
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=compliance_ua
                )
            except Exception as e:
                logger.warning(f"Failed to initialize PRAW: {e}")

    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        mentions = []
        subreddits = "wallstreetbets+stocks+investing+options"
        
        # Try PRAW first if available
        if self.reddit:
            try:
                for submission in self.reddit.subreddit(subreddits).search(ticker, limit=10, sort='new'):
                    mentions.append({
                        "title": submission.title,
                        "platform": "reddit",
                        "link": f"https://reddit.com{submission.permalink}",
                        "publisher": str(submission.author),
                        "time": submission.created_utc
                    })
                return mentions
            except Exception as e:
                logger.error(f"Reddit PRAW fetch error for {ticker}: {e}. Trying JSON fallback...")

        # Fallback to Public JSON Search
        try:
            headers = get_stealth_headers(use_json=True)
            url = f"https://www.reddit.com/search.json?q={ticker}&sort=new&limit=10"
            async with httpx.AsyncClient() as client:
                res = await client.get(url, headers=headers, timeout=10.0)
                if res.status_code == 200:
                    data = res.json()
                    for post in data.get('data', {}).get('children', []):
                        pdata = post.get('data', {})
                        mentions.append({
                            "title": pdata.get('title'),
                            "platform": "reddit-json-search",
                            "link": f"https://reddit.com{pdata.get('permalink')}",
                            "publisher": pdata.get('author'),
                            "time": pdata.get('created_utc')
                        })
                return mentions
        except Exception as e:
            logger.error(f"Reddit JSON fallback search error for {ticker}: {e}")
            return []

class MockSocialSource(SentimentSource):
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        # Keep this as a fallback if keys are missing
        return [{
            "title": f"Bullish on {ticker} for the next quarter! 🚀",
            "platform": "social_mock",
            "link": "#",
            "publisher": "RetailTraders",
            "time": datetime.now(timezone.utc).timestamp()
        }]

SOURCES = [YFinanceSource(), RedditSource(), MockSocialSource()]

# --- Core Logic ---
async def process_ticker_logic(ticker: str):
    """Core processing loop for a single ticker."""
    if not db:
        logger.error("Firestore DB not initialized. Aborting process.")
        return

    ticker = ticker.upper().strip()
    logger.info(f"Starting processing for ticker: {ticker}")
    
    all_items = []
    for source in SOURCES:
        items = await source.fetch(ticker)
        all_items.extend(items)

    all_sentiments = []
    mentions_to_store = []
    
    for item in all_items:
        title = item.get("title", "")
        if not title: continue
            
        score = analyze_sentiment(title)
        all_sentiments.append(score)
        
        mentions_to_store.append({
            "ticker": ticker,
            "timestamp": datetime.now(timezone.utc),
            "platform": item.get("platform", "unknown"),
            "text": title,
            "sentiment_score": score,
            "metadata": {
                "link": item.get("link"),
                "publisher": item.get("publisher"),
                "providerPublishTime": item.get("time")
            }
        })

    if not all_sentiments:
        logger.info(f"No valid sentiment data found for {ticker}")
        # Still update 'latest' with a neutral or stale flag if needed? 
        # For now, just exit to avoid skewing data.
        return

    avg_score = sum(all_sentiments) / len(all_sentiments)
    timestamp_now = datetime.now(timezone.utc)

    try:
        # Use the IngestionEngine's batched writer if available for efficiency and circuit breaking
        if ingestion_engine and ingestion_engine.writer:
            # 1. Historical Entry
            await ingestion_engine.writer.add(COLLECTION_HISTORICAL, None, {
                "ticker": ticker,
                "timestamp": timestamp_now,
                "score": avg_score,
                "volume": len(all_sentiments),
                "sources": {"count": len(all_items)}
            })
            
            # 2. Latest Sentiment
            await ingestion_engine.writer.add(COLLECTION_LATEST, ticker, {
                "ticker": ticker,
                "timestamp": timestamp_now,
                "score": avg_score
            })
            
            # 3. Raw Mentions (Limit for auditing)
            for mention in mentions_to_store[:3]:
                await ingestion_engine.writer.add(COLLECTION_RAW, None, mention)
                
            logger.info(f"✅ Queued update for {ticker} via BatchedWriter: Score={avg_score:.4f}")
        else:
            # Fallback to direct batch if engine not running
            batch = db.batch()
            batch.set(db.collection(COLLECTION_HISTORICAL).document(), {
                "ticker": ticker, "timestamp": timestamp_now, "score": avg_score, "volume": len(all_sentiments), "sources": {"count": len(all_items)}
            })
            batch.set(db.collection(COLLECTION_LATEST).document(ticker), {
                "ticker": ticker, "timestamp": timestamp_now, "score": avg_score
            })
            for mention in mentions_to_store[:3]:
                batch.set(db.collection(COLLECTION_RAW).document(), mention)
            await batch.commit()
            logger.info(f"✅ Successfully updated {ticker} (Direct Batch): Score={avg_score:.4f}")

    except Exception as e:
        logger.error(f"Firestore update failed for {ticker}: {e}")

# --- Endpoints ---

@app.get("/")
def read_root():
    db_status = "online" if db else "offline (Firestore Not Connected)"
    return {
        "status": "online",
        "database": db_status,
        "engine": "FinVision Sentiment Engine",
        "tickers_monitored": TICKERS
    }

@app.get("/health")
def health_check():
    """Health endpoint consumed by OpenRun and load balancers."""
    db_status = "ok" if db else "degraded"
    engine_status = "running" if (ingestion_engine and ingestion_engine.is_running) else "idle"
    return {
        "status": "healthy",
        "database": db_status,
        "engine": engine_status,
        "version": "1.0.0"
    }

# --- API Router for v1 ---
from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1/sentiment")

@api_router.get("/health")
def api_health():
    return health_check()

@api_router.post("/process/{ticker}")
async def process_ticker(ticker: str, background_tasks: BackgroundTasks, user: dict = Depends(verify_token)):
    background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": f"Processing started for {ticker}", "triggered_by": user.get("email")}

@api_router.post("/process-batch")
async def process_batch(batch: TickerBatch, background_tasks: BackgroundTasks, user: dict = Depends(verify_token)):
    for ticker in batch.tickers:
        background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": f"Processing started for {len(batch.tickers)} tickers", "triggered_by": user.get("email")}

@api_router.get("/ticker/{ticker}")
async def get_ticker_details(ticker: str, period: str = "5y", user: dict = Depends(verify_token)):
    """Fetch multi-year historical data and fundamental info from Yahoo Finance."""
    ticker = ticker.upper().strip()
    yf_ticker = ticker
    if ticker in ["BTC", "ETH", "SOL", "DOGE"]:
        yf_ticker = f"{ticker}-USD"
    
    try:
        t = yf.Ticker(yf_ticker)
        hist = await asyncio.to_thread(lambda: t.history(period=period))
        if hist.empty:
            raise HTTPException(status_code=404, detail="No historical data found")
        
        hist_data = hist.reset_index()
        history = []
        for _, row in hist_data.iterrows():
            history.append({
                "time": row['Date'].strftime('%Y-%m-%d'),
                "value": round(row['Close'], 2),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "volume": int(row['Volume'])
            })

        info = await asyncio.to_thread(lambda: t.info)
        return {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "peRatio": info.get("forwardPE"),
            "dividendYield": info.get("dividendYield"),
            "summary": info.get("longBusinessSummary"),
            "history": history
        }
    except Exception as e:
        logger.error(f"Failed to fetch YFinance data for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch market data: {str(e)}")

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
