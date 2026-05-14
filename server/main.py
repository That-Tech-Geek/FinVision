import logging
import os
import sys
import json
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
import yfinance as yf
from textblob import TextBlob
from pydantic import BaseModel, field_validator
import firebase_admin
from firebase_admin import auth, credentials
import praw
from dotenv import load_dotenv

# Aggressive path resolution for Vercel/Production environments
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from ingestion import IngestionEngine, SentimentProcessor
from stealth_utils import get_reddit_compliance_ua, get_stealth_headers

# Load environment variables
load_dotenv()

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("finvision")

# --- Configuration & Globals ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "finvision-68f62")
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH"]
COLLECTION_HISTORICAL = "sentimentHistorical"
COLLECTION_LATEST = "sentimentLatest"
COLLECTION_RAW = "rawMentions"

# Globals for engines
db = None
ingestion_engine = None
sentiment_processor = SentimentProcessor()

SENTIMENT_CACHE = {
    "latest": {}, 
    "historical": {},
    "news": {}
}

# --- Firebase Initialization ---
try:
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    if service_account_path and os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = AsyncClient(project=PROJECT_ID, credentials=cred.get_credential())
        logger.info(f"Firestore initialized with Service Account file")
    else:
        service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        if service_account_json:
            service_account_info = json.loads(service_account_json)
            if "private_key" in service_account_info:
                service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(service_account_info)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = AsyncClient(project=service_account_info.get('project_id', PROJECT_ID))
            logger.info("Firestore initialized with Service Account JSON")
        else:
            if os.getenv("USE_ADC") == "true":
                db = AsyncClient(project=PROJECT_ID)
                if not firebase_admin._apps:
                    firebase_admin.initialize_app()
                logger.info(f"Firestore initialized with ADC")
            else:
                logger.warning("No Firebase credentials found. Firestore Disabled.")
except Exception as e:
    logger.error(f"Critical: Could not initialize Firebase: {e}")
    db = None

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ingestion_engine
    # Load keys for ingestion
    FINNHUB_KEYS = [os.getenv(f"FINNHUB_API_KEY_{i}") for i in range(1, 6)]
    FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k]
    if not FINNHUB_KEYS and os.getenv("FINNHUB_API_KEY"):
        FINNHUB_KEYS = [os.getenv("FINNHUB_API_KEY")]

    try:
        if db:
            ingestion_engine = IngestionEngine(db, TICKERS, FINNHUB_KEYS)
            asyncio.create_task(ingestion_engine.start())
            logger.info(f"Ingestion Engine started")
        else:
            logger.warning("Firestore not connected. Ingestion Engine will not start.")
    except Exception as e:
        logger.error(f"Failed to start Ingestion Engine: {e}")
        
    yield
    if ingestion_engine:
        try:
            ingestion_engine.stop()
        except:
            pass

# --- FastAPI App ---
app = FastAPI(title="FinVision Sentiment Engine", lifespan=lifespan)
application = app

# --- Middleware & Routes ---
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",")] if _raw_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# API Router
from fastapi import APIRouter
api_router = APIRouter(prefix="/api/v1/sentiment")

class TickerBatch(BaseModel):
    tickers: List[str]

# --- Sentiment Analysis ---
def analyze_sentiment(text: str) -> float:
    if not text: return 0.0
    return sentiment_processor.analyze(text)

# --- Sources ---
class SentimentSource:
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

class YFinanceSource(SentimentSource):
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        try:
            t = yf.Ticker(ticker)
            news = await asyncio.wait_for(asyncio.to_thread(lambda: t.news), timeout=10.0)
            return [{"title": n["title"], "publisher": n["publisher"], "link": n["link"], "time": n["providerPublishTime"], "platform": "yfinance_news"} for n in news]
        except: return []

class RedditSource(SentimentSource):
    async def fetch(self, ticker: str) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                headers = get_stealth_headers(use_json=True)
                url = f"https://www.reddit.com/r/wallstreetbets/search.json?q={ticker}&restrict_sr=1&sort=new&limit=10"
                res = await client.get(url, headers=headers, timeout=10.0)
                if res.status_code == 200:
                    data = res.json()
                    posts = data.get('data', {}).get('children', [])
                    return [{"title": p['data'].get('title'), "platform": "reddit_search", "link": f"https://reddit.com{p['data'].get('permalink')}"} for p in posts]
                return []
        except: return []

SOURCES = [YFinanceSource(), RedditSource()]

# --- Core Logic ---
async def process_ticker_logic(ticker: str):
    if not db and not SENTIMENT_CACHE: return
    ticker = ticker.upper().strip()
    all_items = []
    for source in SOURCES:
        items = await source.fetch(ticker)
        all_items.extend(items)

    all_sentiments = [analyze_sentiment(item.get("title", "")) for item in all_items if item.get("title")]
    if not all_sentiments: return

    avg_score = sum(all_sentiments) / len(all_sentiments)
    timestamp_now = datetime.now(timezone.utc)

    if ingestion_engine and ingestion_engine.writer:
        await ingestion_engine.writer.add(COLLECTION_HISTORICAL, None, {"ticker": ticker, "timestamp": timestamp_now, "score": avg_score, "volume": len(all_sentiments)})
        await ingestion_engine.writer.add(COLLECTION_LATEST, ticker, {"ticker": ticker, "timestamp": timestamp_now, "score": avg_score})

    SENTIMENT_CACHE["latest"][ticker] = {"ticker": ticker, "score": avg_score, "timestamp": timestamp_now}
    if ticker not in SENTIMENT_CACHE["historical"]: SENTIMENT_CACHE["historical"][ticker] = []
    SENTIMENT_CACHE["historical"][ticker].append({"ticker": ticker, "score": avg_score, "timestamp": timestamp_now, "volume": len(all_sentiments)})
    SENTIMENT_CACHE["historical"][ticker] = SENTIMENT_CACHE["historical"][ticker][-500:]

# --- Endpoints ---
@api_router.get("/health")
def api_health():
    return {"status": "ok", "db": db is not None, "engine": ingestion_engine is not None}

@api_router.post("/process/{ticker}")
async def process_ticker(ticker: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": f"Processing started for {ticker}", "triggered_by": "guest"}

@api_router.post("/process-batch")
async def process_batch(batch: TickerBatch, background_tasks: BackgroundTasks):
    for ticker in batch.tickers: background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": f"Processing started for {len(batch.tickers)} tickers", "triggered_by": "guest"}

@api_router.get("/quote/{ticker}")
async def get_ticker_quote(ticker: str):
    ticker = ticker.upper().strip()
    try:
        t = yf.Ticker(ticker)
        data = await asyncio.wait_for(asyncio.to_thread(lambda: t.fast_info), timeout=10.0)
        return {"ticker": ticker, "price": round(data['last_price'], 2), "change": round(data.get('year_change', 0), 2)}
    except:
        raise HTTPException(status_code=502, detail="Quote failed")

@api_router.get("/news/{ticker}")
async def get_ticker_news(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        news = await asyncio.wait_for(asyncio.to_thread(lambda: t.news), timeout=10.0)
        return news
    except: return []

@api_router.get("/fallback/sentiment/{ticker}")
async def get_fallback_sentiment(ticker: str):
    t = ticker.upper().strip()
    return {"latest": SENTIMENT_CACHE["latest"].get(t), "historical": SENTIMENT_CACHE["historical"].get(t, [])}

@api_router.get("/ticker/{ticker}")
async def get_ticker_details(ticker: str, period: str = "5y"):
    try:
        t = yf.Ticker(ticker.upper())
        hist = await asyncio.wait_for(asyncio.to_thread(lambda: t.history(period=period)), timeout=15.0)
        history = [{"time": row['Date'].strftime('%Y-%m-%d'), "value": round(row['Close'], 2), "volume": int(row['Volume'])} for _, row in hist.reset_index().iterrows()]
        info = await asyncio.wait_for(asyncio.to_thread(lambda: t.info), timeout=10.0)
        return {"ticker": ticker, "name": info.get("longName", ticker), "history": history}
    except: raise HTTPException(status_code=502, detail="Details failed")

app.include_router(api_router)

# --- Static Files (Serve Frontend) ---
# Check if dist exists (production build)
dist_path = os.path.join(os.path.dirname(_current_dir), "dist")
if os.path.exists(dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"): return None
        return FileResponse(os.path.join(dist_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
