import React, { useState, useEffect, useMemo, useRef } from 'react';
import ErrorBoundary from './ErrorBoundary';
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
  const [sentimentSeries, setSentimentSeries] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [marketLoading, setMarketLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('market');
  const [livePrice, setLivePrice] = useState(null);
  const [orderBook, setOrderBook] = useState({ bids: [], asks: [] });
  const [correlation, setCorrelation] = useState(0.0);
  const [sampleSize, setSampleSize] = useState(0);
  
  const commandInputRef = useRef(null);

  const getCurrencySymbol = (code) => {
    const symbols = {
      'USD': '$', 'INR': '₹', 'GBP': '£', 'EUR': '€', 'JPY': '¥', 
      'CNY': '¥', 'CAD': 'C$', 'AUD': 'A$', 'HKD': 'HK$'
    };
    return symbols[code] || code || '$';
  };

  useEffect(() => {
    const fetchMarketData = async () => {
      setMarketLoading(true);
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/ticker/${selectedTicker}?period=5y`);
        if (res.ok) {
          const data = await res.json();
          setMarketData(data);
          if (data.history) {
            setHistoricalData(data.history);
          }
        }
      } catch (err) {
        console.error("Market fetch failed:", err);
      } finally {
        setMarketLoading(false);
      }
    };
    fetchMarketData();

    const fetchNews = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/news/${selectedTicker}`);
        if (res.ok) {
          const data = await res.json();
          setNewsFeed(data.news || []);
          setSentimentSeries(data.time_series || []);
          setCorrelation(data.correlation || 0.0);
          setSampleSize(data.sample_size || 0);
        }
      } catch (err) {
        console.error("News fetch failed:", err);
      }
    };
    fetchNews();

    const pollQuote = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || '';
        const res = await fetch(`${API_URL}/api/v1/sentiment/quote/${selectedTicker}`);
        if (res.ok) {
          const data = await res.json();
          setLivePrice(data);
          
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
    
    const pollFallback = async () => {
        try {
          const API_URL = import.meta.env.VITE_API_URL || '';
          const res = await fetch(`${API_URL}/api/v1/sentiment/fallback/sentiment/${selectedTicker}`);
          if (res.ok) {
            const data = await res.json();
            if (data && data.latest) setLatestData(data.latest);
            if (data && Array.isArray(data.historical)) {
                setHistoricalData(data.historical.map(d => ({
                    ...d,
                    timestamp: d.timestamp ? (typeof d.timestamp === 'string' ? new Date(d.timestamp).getTime() / 1000 : d.timestamp) : Date.now()/1000
                })));
            }
          }
        } catch (err) {
          console.error("Fallback poll failed:", err);
        }
    };
    
    pollQuote();
    pollFallback();
    const quoteInterval = setInterval(pollQuote, 10000);
    const fallbackInterval = setInterval(pollFallback, 5000);

    return () => {
      clearInterval(quoteInterval);
      clearInterval(fallbackInterval);
    };
  }, [selectedTicker]);

  const handleCommand = (e) => {
    if (e.key === 'Enter') {
      const input = command.trim().toUpperCase();
      if (!input) return;
      const parts = input.split(' ');
      let newTicker = parts[0] === 'GO' ? parts[1] : parts[0];
      if (newTicker) {
        setSelectedTicker(newTicker);
        setCommand("");
        setTimeout(() => commandInputRef.current?.focus(), 50);
      }
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
    const currency = ticker.endsWith('.NS') || ticker.endsWith('.BO') ? 'INR' : 'USD';
    const dummyPrice = (100 + Math.random() * 900).toLocaleString(undefined, { minimumFractionDigits: 2 });
    
    return (
      <div className={`bb-list-item ${selected ? 'active' : ''}`} onClick={onClick}>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontWeight: 600, color: selected ? 'var(--accent-amber)' : 'white' }}>{ticker.replace('^', '')}</span>
          <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>
            {getCurrencySymbol(currency)}{dummyPrice}
          </span>
        </div>
        <span className={isUp ? 'value-up' : 'value-down'} style={{ fontSize: '10px' }}>
          {isUp ? '▲' : '▼'} {Math.abs(change)}%
        </span>
      </div>
    );
  };

  return (
    <div className="bb-terminal">
      <header className="bb-header">
        <Activity size={18} color="var(--accent-amber)" />
        <span style={{ fontWeight: 700, color: 'var(--accent-amber)' }}>FINVISION</span>
        <input 
          ref={commandInputRef}
          type="text" 
          className="command-bar" 
          placeholder="TYPE TICKER (e.g. AAPL, RELIANCE.NS)"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyDown={handleCommand}
        />
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-cyan)' }}>
            <User size={14} />
            <span>INSTITUTIONAL</span>
          </div>
        </div>
      </header>

      <aside className="panel bb-watchlist">
          <div className="section-header">TRENDING MARKETS</div>
          <div style={{ maxHeight: '200px', overflowY: 'auto', borderBottom: '1px solid var(--border-color)' }}>
            {INDICES.map(ticker => (
              <WatchlistItem key={ticker} ticker={ticker} selected={selectedTicker === ticker} onClick={() => setSelectedTicker(ticker)} />
            ))}
          </div>
          <div className="section-header">TRENDING STOCKS</div>
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {TICKERS.map(ticker => (
              <WatchlistItem key={ticker} ticker={ticker} selected={selectedTicker === ticker} onClick={() => setSelectedTicker(ticker)} />
            ))}
          </div>
        </aside>

        <main className="panel bb-main">
          <div className="bb-header-sub">
            <div style={{ display: 'flex', gap: '16px' }}>
              <span className={activeTab === 'sentiment' ? 'tab-active' : 'tab-inactive'} onClick={() => setActiveTab('sentiment')}>1) SENTIMENT</span>
              <span className={activeTab === 'market' ? 'tab-active' : 'tab-inactive'} onClick={() => setActiveTab('market')}>2) MARKET</span>
            </div>
            <div style={{ flex: 1, textAlign: 'right', fontSize: '10px', color: 'var(--text-secondary)' }}>
              {selectedTicker} {marketData?.name} | {marketData?.sector}
            </div>
          </div>
          
          <div className="main-chart-area" style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ flex: 1.5, position: 'relative' }}>
              <ErrorBoundary>
                {activeTab === 'sentiment' ? (
                  <SentimentChart data={sentimentSeries} priceData={marketData?.history || []} color={(latestData?.score || 0) > 0 ? 'var(--accent-green)' : 'var(--accent-red)'} />
                ) : (
                  <PriceChart data={marketData?.history || []} ticker={selectedTicker} />
                )}
              </ErrorBoundary>
              <div className="hud-overlay">
                <div style={{ fontSize: '20px', fontWeight: 800, color: 'var(--accent-amber)' }}>
                  {livePrice ? `${getCurrencySymbol(livePrice.currency)}${livePrice.price.toLocaleString()}` : 'LOADING...'}
                </div>
                <div style={{ fontSize: '10px', color: 'var(--text-secondary)', fontWeight: 600 }}>
                  MCAP: {getCurrencySymbol(marketData?.currency)}{formatLargeNumber(marketData?.stats?.['Market Cap'])} | 
                  NEWS SENTIMENT: <span style={{ color: (latestData?.score || 0) > 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                    {(latestData?.score || 0).toFixed(4)}
                  </span>
                </div>
              </div>
            </div>

            {activeTab === 'sentiment' && (
              <div style={{ flex: 1, borderTop: '1px solid #222', padding: '12px', background: '#050505', overflow: 'hidden', display: 'flex', gap: '20px' }}>
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <div className="section-header" style={{ marginBottom: '8px' }}>LATEST INTELLIGENCE: {selectedTicker}</div>
                    <div style={{ flex: 1, overflowY: 'auto' }}>
                    {newsFeed.map((n, i) => (
                        <div key={i} style={{ padding: '6px 0', borderBottom: '1px solid #111', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontSize: '11px', color: 'white', fontWeight: 600 }}>{n.title}</div>
                            <div style={{ fontSize: '9px', color: 'var(--text-dim)' }}>{n.publisher} | {n.time}</div>
                        </div>
                        <div style={{ width: '80px', textAlign: 'right' }}>
                            <span style={{ fontSize: '11px', fontWeight: 900, color: (n.sentiment?.score || 0) > 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                            {(n.sentiment?.score || 0) > 0 ? '+' : ''}{(n.sentiment?.score || 0).toFixed(4)}
                            </span>
                        </div>
                        </div>
                    ))}
                    </div>
                </div>

                <div style={{ width: '300px', borderLeft: '1px solid #222', paddingLeft: '20px', display: 'flex', flexDirection: 'column' }}>
                    <div className="section-header" style={{ marginBottom: '12px' }}>INTELLIGENCE ALIGNMENT</div>
                    <div style={{ background: '#0a0a0a', padding: '15px', border: '1px solid #1a1a1a', borderRadius: '4px', textAlign: 'center' }}>
                        <div style={{ fontSize: '10px', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '8px' }}>Pearson Correlation (30D)</div>
                        <div style={{ fontSize: '32px', fontWeight: 900, color: correlation > 0.5 ? 'var(--accent-green)' : (correlation > 0.2 ? 'var(--accent-amber)' : 'var(--text-dim)') }}>
                            {correlation.toFixed(4)}
                        </div>
                        <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                            {correlation > 0.6 ? 'HIGH POSITIVE ALIGNMENT' : (correlation > 0.3 ? 'MODERATE CORRELATION' : 'NOISY/DECOUPLED')}
                        </div>
                    </div>
                    <div style={{ marginTop: '15px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                        <div className="stat-card">
                            <div className="stat-label">SAMPLES</div>
                            <div className="stat-value">{sampleSize}</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-label">CONFIDENCE</div>
                            <div className="stat-value">{(sampleSize * Math.abs(correlation) * 10).toFixed(1)}%</div>
                        </div>
                    </div>
                    <div style={{ marginTop: 'auto', fontSize: '9px', color: 'var(--text-dim)', fontStyle: 'italic' }}>
                        *Correlation measures the linear relationship between daily aggregate sentiment and price returns.
                    </div>
                </div>
              </div>
            )}
          </div>

          <div className="fundamentals-panel">
            <div style={{ flex: 1.2 }}>
              <div className="section-header">KEY STATISTICS [{selectedTicker}]</div>
              <div className="stats-grid">
                {marketData?.stats && Object.entries(marketData.stats).map(([label, value]) => (
                  <div key={label} className="stat-card">
                    <div className="stat-label">{label}</div>
                    <div className="stat-value">
                      {typeof value === 'number' ? 
                        (label.includes('Ratio') || label.includes('PE') || label.includes('Beta') ? value.toFixed(2) : 
                         (label.includes('High') || label.includes('Low') || label.includes('Target') || label.includes('Cap') ? getCurrencySymbol(marketData?.currency) : '') + formatLargeNumber(value)) 
                        : (value || 'N/A')}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div style={{ width: '350px', borderLeft: '1px solid #222', paddingLeft: '20px' }}>
              <div className="section-header">BUSINESS SUMMARY</div>
              <div className="summary-text">{marketData?.summary}</div>
              <div className="tag-row">
                  <div className="tag">SECTOR: {marketData?.sector}</div>
                  <div className="tag">IND: {marketData?.industry}</div>
              </div>
            </div>
          </div>
        </main>

        <aside className="panel bb-details">
          <div className="section-header">MARKET DEPTH</div>
          <div className="depth-container">
            <div className="depth-header"><span>PRICE</span><span>SIZE</span></div>
            <div className="order-book">
              {orderBook.asks.map((ask, i) => (
                <div key={i} className="ask-row"><span>{ask.price.toFixed(2)}</span><span>{ask.size}</span></div>
              ))}
              <div className="mid-price">
                {getCurrencySymbol(livePrice?.currency)}{livePrice?.price?.toFixed(2) || '0.00'}
              </div>
              {orderBook.bids.map((bid, i) => (
                <div key={i} className="bid-row"><span>{bid.price.toFixed(2)}</span><span>{bid.size}</span></div>
              ))}
            </div>
          </div>

          <div className="section-header">NEWS ANALYTICS</div>
          <div className="news-feed">
            {newsFeed.length > 0 ? newsFeed.map((n, i) => (
              <div key={i} className="news-item">
                <div className="news-meta">
                  <span className="publisher">{n.publisher?.toUpperCase() || 'FINANCIAL NEWS'}</span>
                  <span>{n.time}</span>
                </div>
                <a href={n.link} target="_blank" rel="noopener noreferrer" className="news-title">{n.title}</a>
                <div className="sentiment-bar-wrap">
                  <div className="sentiment-track">
                    <div className="sentiment-fill" style={{ 
                      width: `${Math.min(100, Math.abs((n.sentiment?.score || 0) * 100))}%`, 
                      background: (n.sentiment?.score || 0) > 0 ? 'var(--accent-green)' : 'var(--accent-red)',
                      marginLeft: (n.sentiment?.score || 0) > 0 ? '0' : 'auto'
                    }} />
                  </div>
                  <span className="sentiment-val" style={{ color: (n.sentiment?.score || 0) > 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                    {(n.sentiment?.score || 0).toFixed(4)}
                  </span>
                </div>
              </div>
            )) : <div className="no-news">NO RECENT NEWS DATA</div>}
          </div>

          <div className="panel-controls">
            <button className="bb-btn" onClick={triggerUpdate} disabled={loading}>
               <RefreshCw size={10} className={loading ? 'spin' : ''} /> RE-SCAN MARKET INTELLIGENCE
            </button>
          </div>
        </aside>

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
        <div className="status-clock">{new Date().toISOString().substring(11, 19)} UTC</div>
      </footer>

      <style>{`
        .bb-content { display: flex; flex: 1; overflow: hidden; }
        .bb-header-sub { border-bottom: 1px solid var(--border-color); height: 32px; background: #050505; display: flex; align-items: center; padding: 0 12px; justify-content: space-between; }
        .tab-active { color: var(--accent-amber); cursor: pointer; font-weight: 800; border-bottom: 2px solid var(--accent-amber); height: 100%; display: flex; align-items: center; }
        .tab-inactive { color: var(--text-dim); cursor: pointer; font-weight: 600; height: 100%; display: flex; align-items: center; }
        .hud-overlay { position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.85); padding: 12px; border: 1px solid #333; z-index: 10; border-radius: 2px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
        .stat-card { background: #0a0a0a; padding: 10px; border: 1px solid #1a1a1a; }
        .stat-label { fontSize: 9px; color: var(--text-dim); text-transform: uppercase; margin-bottom: 4px; }
        .stat-value { fontSize: 15px; fontWeight: 800; color: white; }
        .summary-text { font-size: 13px; line-height: 1.5; color: var(--text-secondary); max-height: 160px; overflow-y: auto; }
        .tag-row { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
        .tag { font-size: 9px; background: #111; padding: 4px 8px; border: 1px solid #222; color: var(--text-secondary); }
        .depth-container { padding: 10px; border-bottom: 1px solid var(--border-color); }
        .depth-header { display: flex; justify-content: space-between; color: var(--text-dim); font-size: 10px; margin-bottom: 6px; }
        .mid-price { text-align: center; font-size: 14px; font-weight: 900; color: white; padding: 8px 0; border-top: 1px solid #222; border-bottom: 1px solid #222; margin: 6px 0; }
        .ask-row, .bid-row { display: flex; justify-content: space-between; font-size: 11px; font-family: 'JetBrains Mono', monospace; }
        .ask-row { color: var(--accent-red); }
        .bid-row { color: var(--accent-green); }
        .news-feed { flex: 1; overflow-y: auto; padding: 10px; }
        .news-item { margin-bottom: 16px; border-bottom: 1px solid #111; padding-bottom: 10px; }
        .news-meta { display: flex; justify-content: space-between; font-size: 9px; color: var(--text-dim); margin-bottom: 4px; }
        .publisher { color: var(--accent-amber); font-weight: 800; }
        .news-title { font-size: 12px; color: white; text-decoration: none; font-weight: 600; line-height: 1.4; display: block; }
        .sentiment-bar-wrap { display: flex; alignItems: center; gap: 10px; margin-top: 8px; }
        .sentiment-track { height: 3px; flex: 1; background: #111; border-radius: 2px; position: relative; }
        .sentiment-fill { height: 100%; border-radius: 2px; }
        .sentiment-val { font-size: 10px; font-weight: 900; min-width: 30px; text-align: right; }
        .panel-controls { padding: 12px; border-top: 1px solid var(--border-color); }
        .no-news { padding: 40px 20px; text-align: center; color: var(--text-dim); font-size: 11px; }
        .main-chart-area { height: 60%; position: relative; border-bottom: 1px solid var(--border-color); }
        .fundamentals-panel { flex: 1; padding: 20px; display: flex; gap: 24px; background: #020202; overflow: hidden; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spin { animation: spin 1s linear infinite; }
        .status-clock { font-size: 10px; color: var(--text-dim); font-weight: 800; padding: 0 12px; }
      `}</style>
    </div>
  );
}

export default App;
