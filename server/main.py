import logging
import os
import sys
import json
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import firebase_admin
from firebase_admin import credentials
from google.cloud.firestore import AsyncClient

# Aggressive path resolution for Vercel
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from ingestion import IngestionEngine, SentimentProcessor
from stealth_utils import get_reddit_compliance_ua, get_stealth_headers

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("finvision")

# --- Globals ---
db = None
ingestion_engine = None
sentiment_processor = None # Lazy loaded

SENTIMENT_CACHE = {
    "latest": {}, 
    "historical": {},
    "news": {}
}

def get_processor():
    global sentiment_processor
    if sentiment_processor is None:
        sentiment_processor = SentimentProcessor()
    return sentiment_processor

# --- Firebase Init (Safe) ---
def init_firebase():
    global db
    if db: return db
    try:
        PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "finvision-68f62")
        service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        if service_account_json:
            info = json.loads(service_account_json)
            if "private_key" in info:
                info["private_key"] = info["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(info)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = AsyncClient(project=info.get('project_id', PROJECT_ID))
            logger.info("Firestore initialized via JSON")
        elif os.getenv("USE_ADC") == "true":
            db = AsyncClient(project=PROJECT_ID)
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            logger.info("Firestore initialized via ADC")
    except Exception as e:
        logger.error(f"Firebase init failed: {e}")
    return db

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ingestion_engine
    init_firebase()
    
    TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH"]
    FINNHUB_KEYS = [os.getenv(f"FINNHUB_API_KEY_{i}") for i in range(1, 6)]
    FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k] or [os.getenv("FINNHUB_API_KEY")]
    FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k]

    try:
        # Start ingestion in background
        ingestion_engine = IngestionEngine(db, TICKERS, FINNHUB_KEYS)
        asyncio.create_task(ingestion_engine.start())
        logger.info("Ingestion Engine started")
    except Exception as e:
        logger.error(f"Ingestion start failed: {e}")
        
    yield
    if ingestion_engine:
        try: ingestion_engine.stop()
        except: pass

app = FastAPI(title="FinVision Terminal API", lifespan=lifespan)
application = app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Logic ---
class TickerBatch(BaseModel):
    tickers: List[str]

async def process_ticker_logic(ticker: str):
    ticker = ticker.upper().strip()
    # Lazy load processor to avoid startup timeout
    proc = get_processor()
    
    # Simple News-based sentiment for quick results
    try:
        t = yf.Ticker(ticker)
        news = await asyncio.wait_for(asyncio.to_thread(lambda: t.news), timeout=10.0)
        titles = [n["title"] for n in news if n.get("title")]
        if not titles: return
        
        scores = [proc.analyze(title) for title in titles]
        avg_score = sum(scores) / len(scores)
        now = datetime.now(timezone.utc)
        
        # Cache update
        SENTIMENT_CACHE["latest"][ticker] = {"ticker": ticker, "score": avg_score, "timestamp": now}
        if ticker not in SENTIMENT_CACHE["historical"]: SENTIMENT_CACHE["historical"][ticker] = []
        SENTIMENT_CACHE["historical"][ticker].append({"ticker": ticker, "score": avg_score, "timestamp": now, "volume": len(titles)})
        SENTIMENT_CACHE["historical"][ticker] = SENTIMENT_CACHE["historical"][ticker][-500:]
        
        # Firestore update if available
        if db:
            await db.collection("sentimentLatest").document(ticker).set({"ticker": ticker, "score": avg_score, "timestamp": now})
            await db.collection("sentimentHistorical").add({"ticker": ticker, "score": avg_score, "timestamp": now, "volume": len(titles)})
    except Exception as e:
        logger.error(f"Processing failed for {ticker}: {e}")

# --- API Endpoints ---
@app.get("/api/v1/sentiment/health")
def health():
    return {"status": "ok", "db": db is not None}

@app.post("/api/v1/sentiment/process/{ticker}")
async def process_ticker(ticker: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": "Processing"}

@app.post("/api/v1/sentiment/process-batch")
async def process_batch(batch: TickerBatch, background_tasks: BackgroundTasks):
    for t in batch.tickers: background_tasks.add_task(process_ticker_logic, t)
    return {"message": "Batch Processing"}

@app.get("/api/v1/sentiment/quote/{ticker}")
async def get_quote(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        data = await asyncio.wait_for(asyncio.to_thread(lambda: t.fast_info), timeout=10.0)
        return {"ticker": ticker, "price": round(data['last_price'], 2), "change": round(data.get('year_change', 0), 2)}
    except: raise HTTPException(status_code=502)

@app.get("/api/v1/sentiment/news/{ticker}")
async def get_news(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        return await asyncio.wait_for(asyncio.to_thread(lambda: t.news), timeout=10.0)
    except: return []

@app.get("/api/v1/sentiment/fallback/sentiment/{ticker}")
async def get_fallback(ticker: str):
    t = ticker.upper()
    return {"latest": SENTIMENT_CACHE["latest"].get(t), "historical": SENTIMENT_CACHE["historical"].get(t, [])}

@app.get("/api/v1/sentiment/ticker/{ticker}")
async def get_details(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        hist = await asyncio.to_thread(lambda: t.history(period="5y"))
        history = [{"time": r['Date'].strftime('%Y-%m-%d'), "value": round(r['Close'], 2), "volume": int(r['Volume'])} for _, r in hist.reset_index().iterrows()]
        return {"ticker": ticker, "history": history}
    except: raise HTTPException(status_code=502)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
