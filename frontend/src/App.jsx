import React, { useState, useEffect, useMemo } from 'react';
import { db, auth, googleProvider } from './firebase';
import { onAuthStateChanged, signInWithPopup, signOut } from 'firebase/auth';
import { collection, query, where, onSnapshot, orderBy, limit } from 'firebase/firestore';
import { 
  Activity, Layout, Search, Settings, User, Bell, ChevronDown, 
  TrendingUp, TrendingDown, BarChart2, MessageSquare, Info, 
  RefreshCw, LogOut, Globe, Shield, Clock, Landmark, DollarSign
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import SentimentChart from './SentimentChart';
import PriceChart from './PriceChart';

const TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "BTC", "ETH", "SOL"];

function App() {
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [latestData, setLatestData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [rawMentions, setRawMentions] = useState([]);
  const [marketData, setMarketData] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [marketLoading, setMarketLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('sentiment'); // sentiment, market

  useEffect(() => {
    const unsubAuth = onAuthStateChanged(auth, (u) => setUser(u));
    return () => unsubAuth();
  }, []);

  useEffect(() => {
    if (!user) return;

    // 1. Listen for Latest Sentiment
    const qLatest = query(collection(db, "sentimentLatest"), limit(50));
    const unsubLatest = onSnapshot(qLatest, (snapshot) => {
      const currentDoc = snapshot.docs.find(d => d.id === selectedTicker);
      if (currentDoc) setLatestData(currentDoc.data());
      else setLatestData(null);
    });

    // 2. Listen for Historical Sentiment
    const qHist = query(
      collection(db, "sentimentHistorical"), 
      where("ticker", "==", selectedTicker),
      orderBy("timestamp", "desc"),
      limit(200)
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
      limit(10)
    );
    const unsubRaw = onSnapshot(qRaw, (snapshot) => {
      setRawMentions(snapshot.docs.map(d => d.data()));
    });

    // 4. Fetch Yahoo Finance Multi-Year Data
    const fetchMarketData = async () => {
      setMarketLoading(true);
      try {
        const idToken = await auth.currentUser.getIdToken();
        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';
        const res = await fetch(`${API_URL}/ticker/${selectedTicker}?period=5y`, {
          headers: { 'Authorization': `Bearer ${idToken}` }
        });
        if (res.ok) {
          const data = await res.json();
          setMarketData(data);
        } else {
          setMarketData(null);
          setError("Market data unavailable for this ticker.");
        }
      } catch (err) {
        console.error("Failed to fetch market data:", err);
        setMarketData(null);
        setError("Network error fetching market data.");
      } finally {
        setMarketLoading(false);
      }
    };
    fetchMarketData();

    return () => {
      unsubLatest();
      unsubHist();
      unsubRaw();
    };
  }, [selectedTicker, user]);

  const triggerUpdate = async () => {
    if (!user) return setError("Please sign in.");
    setLoading(true);
    try {
      const idToken = await auth.currentUser.getIdToken();
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';
      await fetch(`${API_URL}/process/${selectedTicker}`, { 
        method: 'POST',
        headers: { 'Authorization': `Bearer ${idToken}` }
      });
    } catch (err) {
      setError("Update failed. Check console.");
    } finally {
      setTimeout(() => setLoading(false), 2000);
    }
  };

  const getSentimentColor = (score) => {
    if (score > 0.1) return '#089981'; // TV Green
    if (score < -0.1) return '#f23645'; // TV Red
    return '#2962ff'; // TV Blue
  };

  const formatLargeNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toLocaleString();
  };

  if (!user) {
    return (
      <div className="tv-app flex-center" style={{ background: '#0a0a0c' }}>
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel" 
          style={{ maxWidth: '400px', textAlign: 'center', padding: '3rem' }}
        >
          <Activity size={48} color="#2962ff" style={{ margin: '0 auto 1.5rem' }} />
          <h1 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>FinVision Terminal</h1>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', fontSize: '14px' }}>
            Enterprise Sentiment Intelligence for modern markets.
          </p>
          <button 
            onClick={() => signInWithPopup(auth, googleProvider)}
            className="flex-center"
            style={{ 
              width: '100%', padding: '12px', background: '#2962ff', color: 'white', 
              border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 600
            }}
          >
            Launch Terminal
          </button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="tv-app">
      {/* Header */}
      <header className="tv-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Activity size={20} color="#2962ff" />
          <span style={{ fontWeight: 700, fontSize: '14px', letterSpacing: '0.5px' }}>FINVISION</span>
          <div style={{ width: '1px', height: '20px', background: 'var(--border-color)' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <span className="token-badge">{selectedTicker}</span>
            <ChevronDown size={14} color="var(--text-secondary)" />
          </div>
          <div style={{ display: 'flex', gap: '4px', marginLeft: '12px' }}>
            <button 
              className={`tab-btn ${activeTab === 'sentiment' ? 'active' : ''}`}
              onClick={() => setActiveTab('sentiment')}
            >
              Sentiment
            </button>
            <button 
              className={`tab-btn ${activeTab === 'market' ? 'active' : ''}`}
              onClick={() => setActiveTab('market')}
            >
              Market
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)', fontSize: '12px' }}>
            <div className="live-indicator" />
            LIVE DATA
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <Bell size={18} color="var(--text-secondary)" />
            <Settings size={18} color="var(--text-secondary)" />
            <div onClick={() => signOut(auth)} style={{ cursor: 'pointer' }}>
              <LogOut size={18} color="var(--accent-red)" />
            </div>
          </div>
        </div>
      </header>

      <div className="tv-container">
        {/* Watchlist */}
        <aside className="tv-watchlist">
          <div className="watchlist-header">
            <span>Watchlist</span>
            <Search size={14} color="var(--text-secondary)" />
          </div>
          <div style={{ flex: 1, overflowY: 'auto' }}>
            {TICKERS.map(ticker => (
              <div 
                key={ticker} 
                className={`watchlist-item ${selectedTicker === ticker ? 'active' : ''}`}
                onClick={() => setSelectedTicker(ticker)}
              >
                <span style={{ fontWeight: 600 }}>{ticker}</span>
                <div style={{ textAlign: 'right' }}>
                  <div className={Math.random() > 0.5 ? 'price-up' : 'price-down'}>
                    {Math.random() > 0.5 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                    <span style={{ marginLeft: '4px' }}>{(Math.random() * 2).toFixed(2)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Main Chart Area */}
        <main className="tv-main">
          <div style={{ flex: 1, position: 'relative' }}>
            <AnimatePresence mode="wait">
              {activeTab === 'sentiment' ? (
                <motion.div 
                  key="sentiment"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  style={{ height: '100%' }}
                >
                  <SentimentChart 
                    data={historicalData} 
                    color={getSentimentColor(latestData?.score || 0)} 
                  />
                </motion.div>
              ) : (
                <motion.div 
                  key="market"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  style={{ height: '100%', position: 'relative' }}
                >
                  {marketLoading ? (
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                      <RefreshCw size={24} className="spin" style={{ marginRight: '8px' }} />
                      Loading Market Data...
                    </div>
                  ) : (
                    <PriceChart 
                      data={marketData?.history || []} 
                      ticker={selectedTicker}
                    />
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
          
          {/* Legend Overlay */}
          <div style={{ position: 'absolute', top: '20px', left: '20px', pointerEvents: 'none' }}>
            <h2 style={{ fontSize: '24px', fontWeight: 700 }}>{marketData?.name || selectedTicker}</h2>
            <div style={{ display: 'flex', gap: '16px', marginTop: '4px', fontSize: '12px', color: 'var(--text-secondary)' }}>
              <span>SENTIMENT: {latestData?.score.toFixed(3) || 'N/A'}</span>
              {marketData && (
                <>
                  <span>SECTOR: {marketData.sector}</span>
                  <span>INDUSTRY: {marketData.industry}</span>
                </>
              )}
            </div>
          </div>
        </main>

        {/* Right Details Panel */}
        <aside className="tv-details">
          <div style={{ padding: '20px', borderBottom: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '14px', marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
              Sentiment Analysis
              <Info size={14} color="var(--text-secondary)" />
            </h3>
            
            <div style={{ textAlign: 'center', marginBottom: '24px' }}>
              <div style={{ fontSize: '48px', fontWeight: 700, color: getSentimentColor(latestData?.score || 0) }}>
                {latestData ? latestData.score.toFixed(3) : '0.000'}
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '-4px' }}>
                AGGREGATED SCORE
              </div>
            </div>

            <div className="sentiment-gauge">
              <div 
                className="sentiment-pointer" 
                style={{ 
                  left: `${(( (latestData?.score || 0) + 1) / 2) * 100}%`,
                  borderColor: getSentimentColor(latestData?.score || 0)
                }} 
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              <span>BEARISH</span>
              <span>NEUTRAL</span>
              <span>BULLISH</span>
            </div>

            <button 
              onClick={triggerUpdate}
              disabled={loading}
              style={{ 
                width: '100%', marginTop: '24px', padding: '10px', background: 'var(--bg-hover)', 
                border: '1px solid var(--border-color)', color: 'white', borderRadius: '4px',
                cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'
              }}
            >
              <RefreshCw size={14} className={loading ? 'spin' : ''} />
              {loading ? 'ANALYZING...' : 'FORCE RE-SCAN'}
            </button>
          </div>

          {/* Fundamental Stats */}
          <div style={{ padding: '20px', borderBottom: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '14px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Landmark size={14} /> Fundamentals
            </h3>
            <div className="stats-grid">
              <div className="stat-row">
                <span>Market Cap</span>
                <span>{formatLargeNumber(marketData?.marketCap)}</span>
              </div>
              <div className="stat-row">
                <span>P/E Ratio</span>
                <span>{marketData?.peRatio?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="stat-row">
                <span>Div Yield</span>
                <span>{marketData?.dividendYield ? `${(marketData.dividendYield * 100).toFixed(2)}%` : 'N/A'}</span>
              </div>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '12px', lineHeight: '1.4' }}>
              {marketData?.summary?.substring(0, 150)}...
            </p>
          </div>

          <div style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '14px', marginBottom: '16px' }}>Real-time Mentions</h3>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              {rawMentions.map((m, i) => (
                <div key={i} className="mention-card">
                  <div className="mention-meta">
                    <span style={{ color: getSentimentColor(m.sentiment_score) }}>
                      {m.sentiment_score > 0 ? 'Bullish' : 'Bearish'}
                    </span>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Clock size={10} /> {new Date(m.timestamp.seconds * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                  </div>
                  <p className="mention-text">{m.text.substring(0, 100)}...</p>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .spin { animation: spin 1s linear infinite; }
        .tab-btn {
          background: transparent;
          border: none;
          color: var(--text-secondary);
          font-size: 12px;
          font-weight: 600;
          padding: 4px 8px;
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.2s;
        }
        .tab-btn:hover { background: var(--bg-hover); }
        .tab-btn.active { color: white; background: var(--bg-active); }
        .stats-grid { display: flex; flex-direction: column; gap: 8px; }
        .stat-row { display: flex; justify-content: space-between; font-size: 12px; }
        .stat-row span:first-child { color: var(--text-secondary); }
        .stat-row span:last-child { color: white; font-weight: 500; }
      `}</style>
    </div>
  );
}

export default App;

