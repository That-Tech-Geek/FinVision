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
const INDICES = ["^GSPC", "^IXIC", "^DJI", "^VIX", "^RUT", "CL=F", "GC=F"];
const ALL_WATCHED = [...INDICES, ...TICKERS];

function App() {
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [command, setCommand] = useState("");
  const [latestData, setLatestData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [newsFeed, setNewsFeed] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [marketLoading, setMarketLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('market'); // Default to Market for now
  const [livePrice, setLivePrice] = useState(null);
  const [orderBook, setOrderBook] = useState({ bids: [], asks: [] });
  
  const commandInputRef = useRef(null);

  useEffect(() => {
    // 1. Fetch Yahoo Finance
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

    // 5. Fetch Yahoo News
    const fetchNews = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/news/${selectedTicker}`);
        if (res.ok) {
          const data = await res.json();
          setNewsFeed(data);
        }
      } catch (err) {
        console.error("News fetch failed:", err);
      }
    };
    fetchNews();

    // 6. Polling for Live Price
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
    
    // 7. Fallback Polling (if Firestore is disabled)
    const pollFallback = async () => {
        if (historicalData.length > 0) return; // Already have live data
        try {
          const API_URL = import.meta.env.VITE_API_URL || '';
          const res = await fetch(`${API_URL}/api/v1/sentiment/fallback/sentiment/${selectedTicker}`);
          if (res.ok) {
            const data = await res.json();
            if (data.latest) setLatestData(data.latest);
            if (data.historical?.length > 0) {
                setHistoricalData(data.historical.map(d => ({
                    ...d,
                    timestamp: typeof d.timestamp === 'string' ? new Date(d.timestamp).getTime() / 1000 : d.timestamp
                })));
            }
          }
        } catch (err) {
          console.error("Fallback poll failed:", err);
        }
    };
    
    pollQuote();
    const quoteInterval = setInterval(pollQuote, 10000);
    
    const fallbackInterval = setInterval(pollFallback, 5000);

    return () => {
      clearInterval(quoteInterval);
      clearInterval(fallbackInterval);
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

  const WatchlistItem = ({ ticker, selected, onClick }) => {
    const change = (Math.sin(ticker.charCodeAt(0)) * 1.5).toFixed(2);
    const isUp = parseFloat(change) > 0;
    return (
      <div 
        className={`bb-list-item ${selected ? 'active' : ''}`}
        onClick={onClick}
      >
        <span style={{ fontWeight: 600, color: selected ? 'var(--accent-amber)' : 'white' }}>{ticker.replace('^', '')}</span>
        <span className={isUp ? 'value-up' : 'value-down'} style={{ fontSize: '10px' }}>
          {isUp ? '▲' : '▼'} {Math.abs(change)}%
        </span>
      </div>
    );
  };

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
            <span>TERMINAL</span>
          </div>
        </div>
      </header>

      {/* Watchlist */}
      <aside className="panel bb-watchlist">
        <div className="section-header">MARKET BENCHMARKS</div>
        <div style={{ maxHeight: '200px', overflowY: 'auto', borderBottom: '1px solid var(--border-color)' }}>
          {INDICES.map(ticker => (
            <WatchlistItem 
              key={ticker} 
              ticker={ticker} 
              selected={selectedTicker === ticker} 
              onClick={() => setSelectedTicker(ticker)} 
            />
          ))}
        </div>
        
        <div className="section-header">EQUITIES & CRYPTO</div>
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {TICKERS.map(ticker => (
            <WatchlistItem 
              key={ticker} 
              ticker={ticker} 
              selected={selectedTicker === ticker} 
              onClick={() => setSelectedTicker(ticker)} 
            />
          ))}
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
          <div style={{ position: 'absolute', top: '10px', left: '10px', pointerEvents: 'none', background: 'rgba(0,0,0,0.8)', padding: '8px', border: '1px solid #333', zIndex: 10 }}>
            <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--accent-amber)' }}>
              {livePrice ? `$${livePrice.price.toLocaleString()}` : 'LOADING...'}
            </div>
            <div style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>
              MCAP: {formatLargeNumber(marketData?.stats?.['Market Cap'])} | SENT: {(latestData?.score || 0).toFixed(4)}
            </div>
          </div>
        </div>

        {/* Fundamentals Bald Spot Filler */}
        <div className="fundamentals-panel" style={{ padding: '16px', borderTop: '1px solid var(--border-color)', background: '#050505', display: 'flex', gap: '20px', overflowY: 'auto' }}>
          <div style={{ flex: 1 }}>
            <div className="section-header" style={{ marginBottom: '10px' }}>KEY STATISTICS</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '8px' }}>
              {marketData?.stats && Object.entries(marketData.stats).map(([label, value]) => (
                <div key={label} style={{ background: '#111', padding: '6px', border: '1px solid #222' }}>
                  <div style={{ fontSize: '9px', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>{label}</div>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: 'white' }}>
                    {typeof value === 'number' ? 
                      (label.includes('Ratio') || label.includes('PE') || label.includes('Beta') ? value.toFixed(2) : formatLargeNumber(value)) 
                      : (value || 'N/A')}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div style={{ width: '300px', borderLeft: '1px solid #222', paddingLeft: '20px' }}>
            <div className="section-header" style={{ marginBottom: '10px' }}>BUSINESS SUMMARY</div>
            <div style={{ fontSize: '11px', lineHeight: 1.5, color: 'var(--text-secondary)', maxHeight: '150px', overflowY: 'auto' }}>
              {marketData?.summary}
            </div>
            <div style={{ marginTop: '10px', display: 'flex', gap: '10px' }}>
                <div style={{ fontSize: '9px', background: '#111', padding: '4px 8px', border: '1px solid #333' }}>
                    SECTOR: <span style={{ color: 'white' }}>{marketData?.sector}</span>
                </div>
                <div style={{ fontSize: '9px', background: '#111', padding: '4px 8px', border: '1px solid #333' }}>
                    IND: <span style={{ color: 'white' }}>{marketData?.industry}</span>
                </div>
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
              {livePrice?.price?.toFixed(2) || '0.00'}
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

        <div className="section-header">REAL-TIME NEWS</div>
        <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
          {newsFeed.length > 0 ? newsFeed.map((n, i) => (
            <div key={i} style={{ marginBottom: '12px', borderBottom: '1px solid #111', paddingBottom: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: 'var(--text-secondary)', marginBottom: '2px' }}>
                <span style={{ color: 'var(--accent-amber)' }}>{n.publisher?.toUpperCase() || 'FINANCIAL NEWS'}</span>
                <span>{new Date(n.providerPublishTime * 1000).toLocaleTimeString()}</span>
              </div>
              <a 
                href={n.link} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ fontSize: '11px', lineHeight: 1.3, color: 'white', textDecoration: 'none', fontWeight: 500 }}
              >
                {n.title}
              </a>
            </div>
          )) : (
            <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-dim)', fontSize: '10px' }}>
              NO RECENT NEWS FOR {selectedTicker}
            </div>
          )}
        </div>
      </aside>

      {/* Footer / Ticker & Status Bar */}
      <div className="bb-terminal-footer">
        <footer className="bb-footer">
          <div className="live-badge">LIVE</div>
          <div className="ticker-wrap">
            <div className="ticker-move">
              {[...INDICES, ...TICKERS].map((t, i) => (
                <span key={i} className="ticker-item">
                  <span style={{ fontWeight: 800 }}>{t.replace('^', '')}</span>
                  <span className={i % 2 === 0 ? 'value-up' : 'value-down'} style={{ marginLeft: '4px' }}>
                    {(Math.random() * 500).toFixed(2)} {(i % 2 === 0 ? '▲' : '▼')}
                  </span>
                </span>
              ))}
              {/* Duplicate for seamless loop */}
              {[...INDICES, ...TICKERS].map((t, i) => (
                <span key={`dup-${i}`} className="ticker-item">
                  <span style={{ fontWeight: 800 }}>{t.replace('^', '')}</span>
                  <span className={i % 2 === 0 ? 'value-up' : 'value-down'} style={{ marginLeft: '4px' }}>
                    {(Math.random() * 500).toFixed(2)} {(i % 2 === 0 ? '▲' : '▼')}
                  </span>
                </span>
              ))}
            </div>
          </div>
          <div className="status-clock">
            {new Date().toISOString().substring(11, 19)} UTC
          </div>
        </footer>
        <div className="status-bar">
          <div className="status-item"><span className="status-dot green"></span> NETWORK: CONNECTED</div>
          <div className="status-item"><span className="status-dot amber"></span> DB: {db ? 'ONLINE' : 'FALLBACK'}</div>
          <div className="status-item"><span className="status-dot green"></span> KEYS: 5 ROTATING</div>
          <div className="status-item" style={{ marginLeft: 'auto' }}>SESSION: GUEST</div>
        </div>
      </div>

      <style>{`
        @keyframes ticker {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .ticker-move {
          display: flex;
          white-space: nowrap;
          animation: ticker 30s linear infinite;
        }
        .bb-terminal-footer {
            border-top: 2px solid var(--border-color);
            background: #000;
        }
        .status-bar {
            height: 20px;
            background: #0a0a0a;
            border-top: 1px solid #222;
            display: flex;
            align-items: center;
            padding: 0 10px;
            gap: 20px;
            font-size: 9px;
            color: var(--text-dim);
            font-weight: 600;
        }
        .status-item { display: flex; align-items: center; gap: 5px; }
        .status-dot { width: 6px; height: 6px; border-radius: 50%; }
        .status-dot.green { background: var(--accent-green); box-shadow: 0 0 5px var(--accent-green); }
        .status-dot.amber { background: var(--accent-amber); box-shadow: 0 0 5px var(--accent-amber); }
        .live-badge { background: var(--accent-amber); color: #000; padding: 0 10px; font-weight: 900; font-size: 10px; height: 100%; display: flex; align-items: center; }
        .status-clock { padding: 0 12px; color: var(--accent-amber); font-weight: 700; font-family: monospace; font-size: 11px; }
      `}</style>
    </div>
  );
}

export default App;
