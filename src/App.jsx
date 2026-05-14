import React, { useState, useEffect, useMemo, useRef } from 'react';
import { db, auth, googleProvider } from './firebase';
import { onAuthStateChanged, signInWithPopup, signOut, signInAnonymously } from 'firebase/auth';
import { collection, query, where, onSnapshot, orderBy, limit } from 'firebase/firestore';
import { 
  Activity, Search, Settings, User, Bell, ChevronDown, 
  TrendingUp, TrendingDown, RefreshCw, LogOut, Info, Clock, Landmark
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import SentimentChart from './SentimentChart';
import PriceChart from './PriceChart';

const TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH", "SOL", "DOGE"];

function App() {
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [command, setCommand] = useState("");
  const [latestData, setLatestData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [rawMentions, setRawMentions] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [marketLoading, setMarketLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('sentiment');
  const [livePrice, setLivePrice] = useState(null);
  const [orderBook, setOrderBook] = useState({ bids: [], asks: [] });
  
  const commandInputRef = useRef(null);

  useEffect(() => {
    const unsubAuth = onAuthStateChanged(auth, (u) => {
      setUser(u);
      if (!u) signInAnonymously(auth); // Default to anonymous for Guest Access
    });
    return () => unsubAuth();
  }, []);

  useEffect(() => {
    // 1. Listen for Latest Sentiment
    const qLatest = query(collection(db, "sentimentLatest"), limit(50));
    const unsubLatest = onSnapshot(qLatest, (snapshot) => {
      const currentDoc = snapshot.docs.find(d => d.id === selectedTicker);
      if (currentDoc) setLatestData(currentDoc.data());
      else setLatestData(null);
    });

    // 2. Listen for Historical Sentiment (500 pts)
    const qHist = query(
      collection(db, "sentimentHistorical"), 
      where("ticker", "==", selectedTicker),
      orderBy("timestamp", "desc"),
      limit(500)
    );
    const unsubHist = onSnapshot(qHist, (snapshot) => {
      const data = snapshot.docs.map(d => ({
        ...d.data(),
        timestamp: d.data().timestamp.seconds
      })).reverse();
      setHistoricalData(data);
    });

    // 3. Listen for Raw Mentions
    const qRaw = query(
      collection(db, "rawMentions"),
      where("ticker", "==", selectedTicker),
      orderBy("timestamp", "desc"),
      limit(15)
    );
    const unsubRaw = onSnapshot(qRaw, (snapshot) => {
      setRawMentions(snapshot.docs.map(d => d.data()));
    });

    // 4. Fetch Yahoo Finance
    const fetchMarketData = async () => {
      setMarketLoading(true);
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/ticker/${selectedTicker}?period=5y`);
        if (res.ok) {
          const data = await res.json();
          setMarketData(data);
        }
      } catch (err) {
        console.error("Market fetch failed:", err);
      } finally {
        setMarketLoading(false);
      }
    };
    fetchMarketData();

    // 5. Polling for Live Price
    const pollQuote = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/quote/${selectedTicker}`);
        if (res.ok) {
          const data = await res.json();
          setLivePrice(data);
          
          // Simulation logic
          const price = data.price;
          const newBids = Array.from({length: 8}, (_, i) => ({
            price: price - (i * 0.05 + Math.random() * 0.01),
            size: (Math.random() * 500).toFixed(0)
          }));
          const newAsks = Array.from({length: 8}, (_, i) => ({
            price: price + (i * 0.05 + Math.random() * 0.01),
            size: (Math.random() * 500).toFixed(0)
          })).reverse();
          setOrderBook({ bids: newBids, asks: newAsks });
        }
      } catch (err) {
        console.error("Quote poll failed:", err);
      }
    };
    
    pollQuote();
    const interval = setInterval(pollQuote, 10000);

    return () => {
      unsubLatest();
      unsubHist();
      unsubRaw();
      clearInterval(interval);
    };
  }, [selectedTicker]);

  const handleCommand = (e) => {
    if (e.key === 'Enter') {
      const parts = command.toUpperCase().split(' ');
      if (parts[0] === 'GO' && parts[1]) {
        setSelectedTicker(parts[1]);
      } else if (TICKERS.includes(parts[0])) {
        setSelectedTicker(parts[0]);
      }
      setCommand("");
    }
  };

  const triggerUpdate = async () => {
    setLoading(true);
    try {
      const API_URL = import.meta.env.VITE_API_URL || '';
      await fetch(`${API_URL}/api/v1/sentiment/process/${selectedTicker}`, { method: 'POST' });
    } catch (err) {
      setError("Update failed.");
    } finally {
      setTimeout(() => setLoading(false), 2000);
    }
  };

  const triggerBulkUpdate = async () => {
    setLoading(true);
    try {
      const API_URL = import.meta.env.VITE_API_URL || '';
      await fetch(`${API_URL}/api/v1/sentiment/process-batch`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tickers: TICKERS })
      });
    } catch (err) {
      setError("Bulk update failed.");
    } finally {
      setTimeout(() => setLoading(false), 3000);
    }
  };

  const formatLargeNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toLocaleString();
  };

  if (!user) return <div className="flex-center" style={{height:'100vh', background:'#000'}}>Initializing Bloomberg Terminal...</div>;

  return (
    <div className="bb-terminal">
      {/* Header / Command Bar */}
      <header className="bb-header">
        <Activity size={18} color="var(--accent-amber)" />
        <span style={{ fontWeight: 700, color: 'var(--accent-amber)' }}>FINVISION</span>
        <input 
          ref={commandInputRef}
          type="text" 
          className="command-bar" 
          placeholder="TYPE TICKER OR COMMAND (e.g. AAPL, GO BTC)"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyDown={handleCommand}
        />
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Bell size={14} color="var(--text-secondary)" />
          <Settings size={14} color="var(--text-secondary)" />
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-cyan)' }}>
            <User size={14} />
            <span>{user.isAnonymous ? 'GUEST' : user.email.split('@')[0]}</span>
          </div>
          <button className="bb-btn" onClick={() => signOut(auth)}>EXIT</button>
        </div>
      </header>

      {/* Watchlist */}
      <aside className="panel bb-watchlist">
        <div className="section-header">WATCHLIST</div>
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {TICKERS.map(ticker => {
            const isSelected = selectedTicker === ticker;
            const change = (Math.sin(ticker.charCodeAt(0)) * 2.5).toFixed(2);
            const isUp = parseFloat(change) > 0;
            return (
              <div 
                key={ticker} 
                className={`bb-list-item ${isSelected ? 'active' : ''}`}
                onClick={() => setSelectedTicker(ticker)}
              >
                <span style={{ fontWeight: 600, color: isSelected ? 'var(--accent-amber)' : 'white' }}>{ticker}</span>
                <span className={isUp ? 'value-up' : 'value-down'}>
                  {isUp ? '+' : ''}{change}%
                </span>
              </div>
            );
          })}
        </div>
      </aside>

      {/* Main Analysis Area */}
      <main className="panel bb-main" style={{ borderLeft: '1px solid var(--border-color)', borderRight: '1px solid var(--border-color)' }}>
        <div className="bb-header" style={{ borderBottom: '1px solid var(--border-color)', height: '32px', background: '#050505' }}>
          <div style={{ display: 'flex', gap: '16px' }}>
            <span 
              className={activeTab === 'sentiment' ? 'value-neutral' : ''} 
              style={{ cursor: 'pointer', fontWeight: 700 }}
              onClick={() => setActiveTab('sentiment')}
            >
              1) SENTIMENT
            </span>
            <span 
              className={activeTab === 'market' ? 'value-neutral' : ''} 
              style={{ cursor: 'pointer', fontWeight: 700 }}
              onClick={() => setActiveTab('market')}
            >
              2) MARKET
            </span>
          </div>
          <div style={{ flex: 1, textAlign: 'right', fontSize: '10px', color: 'var(--text-secondary)' }}>
            {selectedTicker} {marketData?.name} | {marketData?.sector}
          </div>
        </div>
        
        <div style={{ flex: 1, position: 'relative', background: '#000' }}>
          {activeTab === 'sentiment' ? (
             <SentimentChart 
                data={historicalData} 
                priceData={marketData?.history || []}
                color={latestData?.score > 0 ? 'var(--accent-green)' : 'var(--accent-red)'} 
              />
          ) : (
            <PriceChart data={marketData?.history || []} ticker={selectedTicker} />
          )}

          {/* HUD Overlay */}
          <div style={{ position: 'absolute', top: '10px', left: '10px', pointerEvents: 'none', background: 'rgba(0,0,0,0.6)', padding: '8px', border: '1px solid #333' }}>
            <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--accent-amber)' }}>
              {livePrice ? `$${livePrice.price.toLocaleString()}` : 'LOADING...'}
            </div>
            <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>
              VOL: {formatLargeNumber(marketData?.marketCap)} | SENT: {(latestData?.score || 0).toFixed(4)}
            </div>
          </div>
        </div>
      </main>

      {/* Side Details / Order Book */}
      <aside className="panel bb-details">
        <div className="section-header">MARKET DEPTH</div>
        <div style={{ padding: '8px', fontSize: '10px', borderBottom: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', marginBottom: '4px' }}>
            <span>PRICE</span>
            <span>SIZE</span>
          </div>
          <div className="order-book" style={{ fontFamily: 'monospace' }}>
            {orderBook.asks.map((ask, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--accent-red)' }}>
                <span>{ask.price.toFixed(2)}</span>
                <span style={{ color: 'var(--text-dim)' }}>{ask.size}</span>
              </div>
            ))}
            <div style={{ textAlign: 'center', padding: '4px 0', color: 'white', fontWeight: 700, borderTop: '1px solid #333', borderBottom: '1px solid #333', margin: '4px 0' }}>
              {livePrice?.price.toFixed(2)}
            </div>
            {orderBook.bids.map((bid, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--accent-green)' }}>
                <span>{bid.price.toFixed(2)}</span>
                <span style={{ color: 'var(--text-dim)' }}>{bid.size}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="section-header" style={{ marginTop: 'auto' }}>CONTROLS</div>
        <div style={{ padding: '12px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <button className="bb-btn" onClick={triggerUpdate} disabled={loading} style={{ color: 'var(--accent-cyan)' }}>
             <RefreshCw size={10} className={loading ? 'spin' : ''} /> FORCE SCAN {selectedTicker}
          </button>
          <button className="bb-btn" onClick={triggerBulkUpdate} disabled={loading} style={{ color: 'var(--accent-amber)' }}>
             <RefreshCw size={10} className={loading ? 'spin' : ''} /> SYNC ALL SYMBOLS
          </button>
        </div>

        <div className="section-header">NEWS FEED</div>
        <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
          {rawMentions.map((m, i) => (
            <div key={i} style={{ marginBottom: '8px', borderBottom: '1px solid #111', paddingBottom: '4px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: 'var(--text-secondary)' }}>
                <span style={{ color: m.sentiment_score > 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                  {m.platform.toUpperCase()}
                </span>
                <span>{new Date(m.timestamp.seconds * 1000).toLocaleTimeString()}</span>
              </div>
              <div style={{ fontSize: '10px', lineHeight: 1.2 }}>{m.text.substring(0, 80)}...</div>
            </div>
          ))}
        </div>
      </aside>

      {/* Footer / Ticker */}
      <footer className="bb-footer">
        <div style={{ background: 'var(--accent-amber)', color: 'black', padding: '0 8px', fontWeight: 700, height: '100%', display: 'flex', alignItems: 'center' }}>
          LIVE
        </div>
        <div className="ticker-wrap">
          <div className="ticker-move">
            {TICKERS.map(t => (
              <span key={t} className="ticker-item">
                {t} <span className="value-up">{(Math.random() * 100).toFixed(2)}</span>
              </span>
            ))}
            {/* Repeat for seamless loop */}
            {TICKERS.map(t => (
              <span key={t+"_2"} className="ticker-item">
                {t} <span className="value-up">{(Math.random() * 100).toFixed(2)}</span>
              </span>
            ))}
          </div>
        </div>
        <div style={{ padding: '0 12px', color: 'var(--text-secondary)', fontSize: '10px' }}>
          {new Date().toLocaleTimeString()}
        </div>
      </footer>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spin { animation: spin 1s linear infinite; }
        .flex-center { display: flex; align-items: center; justify-content: center; }
      `}</style>
    </div>
  );
}

export default App;
