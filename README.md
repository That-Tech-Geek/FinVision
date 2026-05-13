# FinVision: Real-Time Financial Sentiment Engine

FinVision is a production-grade financial sentiment analysis platform that ingests data from Reddit, Finnhub, and other social/financial news sources to provide real-time sentiment signals for top-tier assets.

## 🚀 Key Features
- **Real-Time Ingestion**: Dual-layered ingestion (PRAW + Stealth Polling) for Reddit, and WebSocket-based trades/news from Finnhub.
- **Sentiment Ensemble**: Multi-faceted sentiment analysis using a weighted ensemble of **VADER (60%)** and **TextBlob (40%)**.
- **Resilient Backend**: FastAPI-based microservice with exponential backoff supervisors, circuit breakers for database writes, and stealth headers for no-auth fallbacks.
- **Interactive Frontend**: High-fidelity React-based "Terminal" UI with glassmorphism aesthetics and real-time WebSocket updates.
- **Secure Architecture**: Integrated with Firebase Authentication and Firestore for high-throughput, low-latency storage.

## 🏗️ Project Structure
```text
FinVision/
├── backend/            # FastAPI + PRAW + VADER Sentiment Engine
├── frontend/           # Vite + React + Tailwind + Recharts Dashboard
├── firestore.rules     # Security rules for sentiment data
└── README.md
```

## 🛠️ Setup & Installation

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Configure `.env` with:
   - `FIREBASE_SERVICE_ACCOUNT_PATH`: Path to your JSON credentials.
   - `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`: From Reddit Apps.
   - `FINNHUB_API_KEY_1...`: Your Finnhub keys.
4. `python main.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## 📊 Robustness Features
- **Firestore Circuit Breaker**: Prevents OOM by dropping data if the write queue exceeds 2000 items during network instability.
- **Reddit Supervisor**: Automatically restarts streams on failure with jittered exponential backoff.
- **Stealth Polling**: Fallback to public JSON endpoints using browser-grade headers when API keys are exhausted.

---
Developed by **Antigravity** via **Sagan Labs**.
