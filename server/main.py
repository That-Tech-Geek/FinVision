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

from ingestion import IngestionEngine, SentimentProcessor, KeyRotator
from stealth_utils import get_reddit_compliance_ua, get_stealth_headers

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("finvision")

# --- Globals ---
db = None
ingestion_engine = None
sentiment_processor = None # Lazy loaded
rest_key_rotator = None # Global for quote cycling

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
        sa_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        if sa_json:
            try:
                info = json.loads(sa_json)
                if "private_key" in info:
                    info["private_key"] = info["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(info)
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred)
                db = AsyncClient(project=info.get('project_id', PROJECT_ID))
                logger.info(f"✅ Firestore initialized via JSON (Project: {info.get('project_id')})")
                return db
            except Exception as j_err:
                logger.error(f"❌ JSON SA Parse Failed: {j_err}")
        
        sa_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
        if sa_path and os.path.exists(sa_path):
            cred = credentials.Certificate(sa_path)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = AsyncClient(project=PROJECT_ID)
            logger.info(f"✅ Firestore initialized via Path")
            return db
    except Exception as e:
        logger.error(f"Firebase init failed: {e}")
    return db

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ingestion_engine, rest_key_rotator
    init_firebase()
    
    TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH"]
    FINNHUB_KEYS = [os.getenv(f"FINNHUB_API_KEY_{i}") for i in range(1, 6)]
    FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k] or [os.getenv("FINNHUB_API_KEY")]
    FINNHUB_KEYS = [k for k in FINNHUB_KEYS if k]
    
    rest_key_rotator = KeyRotator(FINNHUB_KEYS)

    try:
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
    proc = get_processor()
    try:
        t = yf.Ticker(ticker)
        news = await asyncio.wait_for(asyncio.to_thread(lambda: t.news), timeout=10.0)
        titles = [n["title"] for n in news if n.get("title")]
        if not titles: return
        scores = [proc.analyze(title) for title in titles]
        avg_score = sum(scores) / len(scores)
        now = datetime.now(timezone.utc)
        SENTIMENT_CACHE["latest"][ticker] = {"ticker": ticker, "score": avg_score, "timestamp": now}
        if ticker not in SENTIMENT_CACHE["historical"]: SENTIMENT_CACHE["historical"][ticker] = []
        SENTIMENT_CACHE["historical"][ticker].append({"ticker": ticker, "score": avg_score, "timestamp": now, "volume": len(titles)})
        SENTIMENT_CACHE["historical"][ticker] = SENTIMENT_CACHE["historical"][ticker][-500:]
        if db:
            await db.collection("sentimentLatest").document(ticker).set({"ticker": ticker, "score": avg_score, "timestamp": now})
    except Exception as e:
        logger.error(f"Processing failed for {ticker}: {e}")

# --- API Endpoints ---
@app.get("/api/v1/sentiment/health")
def health():
    return {"status": "ok", "db": db is not None, "rotator": rest_key_rotator is not None}

@app.get("/api/v1/sentiment/quote/{ticker}")
async def get_quote(ticker: str):
    ticker = ticker.upper().strip()
    # Try Finnhub via Rotator
    if rest_key_rotator and rest_key_rotator.keys:
        key = rest_key_rotator.get_key()
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}", timeout=5.0)
                if res.status_code == 200:
                    data = res.json()
                    if data.get('c'):
                        # Finnhub doesn't provide currency easily in quote, default to yf for currency
                        t = yf.Ticker(ticker)
                        info = await asyncio.wait_for(asyncio.to_thread(lambda: t.info), timeout=5.0)
                        return {
                            "ticker": ticker, 
                            "price": round(data['c'], 2), 
                            "change": round(data.get('dp', 0), 2),
                            "currency": info.get("currency", "USD")
                        }
        except: pass
    
    # Fallback to yfinance
    try:
        t = yf.Ticker(ticker)
        data = await asyncio.wait_for(asyncio.to_thread(lambda: t.fast_info), timeout=10.0)
        info = await asyncio.wait_for(asyncio.to_thread(lambda: t.info), timeout=5.0)
        return {
            "ticker": ticker, 
            "price": round(data['last_price'], 2), 
            "change": round(data.get('year_change', 0), 2),
            "currency": info.get("currency", "USD")
        }
    except: raise HTTPException(status_code=502)

@app.get("/api/v1/sentiment/ticker/{ticker}")
async def get_details(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        hist = await asyncio.to_thread(lambda: t.history(period="5y"))
        history = [{"time": r['Date'].strftime('%Y-%m-%d'), "value": round(r['Close'], 2), "volume": int(r['Volume'])} for _, r in hist.reset_index().iterrows()]
        info = await asyncio.wait_for(asyncio.to_thread(lambda: t.info), timeout=15.0)
        return {
            "ticker": ticker.upper(),
            "name": info.get("longName", ticker.upper()),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "currency": info.get("currency", "USD"),
            "summary": info.get("longBusinessSummary", "N/A"),
            "stats": {
                "Market Cap": info.get("marketCap"),
                "P/E Ratio": info.get("trailingPE"),
                "Forward P/E": info.get("forwardPE"),
                "Dividend Yield": info.get("dividendYield"),
                "Beta": info.get("beta"),
                "52W High": info.get("fiftyTwoWeekHigh"),
                "52W Low": info.get("fiftyTwoWeekLow"),
                "Analyst Target": info.get("targetMeanPrice"),
                "Recommendation": info.get("recommendationKey", "N/A").upper(),
                "Short Ratio": info.get("shortRatio"),
                "Debt/Equity": info.get("debtToEquity")
            },
            "history": history
        }
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

@app.post("/api/v1/sentiment/process/{ticker}")
async def process_ticker(ticker: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_ticker_logic, ticker)
    return {"message": "Processing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
