import React, { useState, useEffect } from 'react';
import { db, auth, googleProvider } from './firebase';
import { onAuthStateChanged, signInWithPopup, signOut } from 'firebase/auth';
import { collection, query, where, onSnapshot, orderBy, limit, doc } from 'firebase/firestore';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts'; // Switching to Recharts for better React integration
import { Activity, BarChart3, TrendingUp, RefreshCw, Layers } from 'lucide-react';

const TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"];

function App() {
  const [selectedTicker, setSelectedTicker] = useState("AAPL");
  const [latestData, setLatestData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [rawMentions, setRawMentions] = useState([]);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubAuth = onAuthStateChanged(auth, (u) => {
      setUser(u);
    });
    return () => unsubAuth();
  }, []);

  useEffect(() => {
    setLatestData(null);
    setHistoricalData([]);
    setRawMentions([]);
    setError(null);
    // 1. Listen for Latest Sentiment (Real-time Sync)
    const latestRef = collection(db, "sentimentLatest");
    const qLatest = query(latestRef, limit(10)); // Watch small batch for changes
    const unsubLatest = onSnapshot(qLatest, (snapshot) => {
      snapshot.docChanges().forEach((change) => {
        if (change.type === "modified" || change.type === "added") {
          const data = change.doc.data();
          if (data.ticker === selectedTicker) {
            setLatestData(data);
          }
        }
      });
      // Handle initial load if doc exists but no changes yet
      const currentDoc = snapshot.docs.find(d => d.id === selectedTicker);
      if (currentDoc) setLatestData(currentDoc.data());
    });

    // 2. Listen for Historical Data (For Charting)
    const historyRef = collection(db, "sentimentHistorical");
    const qHist = query(
      historyRef, 
      where("ticker", "==", selectedTicker),
      orderBy("timestamp", "desc"),
      limit(100)
    );
    const unsubHist = onSnapshot(qHist, (snapshot) => {
      const data = snapshot.docs.map(d => ({
        ...d.data(),
        time: new Date(d.data().timestamp.seconds * 1000).toLocaleTimeString(),
        timestamp: d.data().timestamp.seconds
      })).reverse();
      setHistoricalData(data);
    });

    // 3. Listen for Raw Mentions
    const rawRef = collection(db, "rawMentions");
    const qRaw = query(
      rawRef,
      where("ticker", "==", selectedTicker),
      orderBy("timestamp", "desc"),
      limit(5)
    );
    const unsubRaw = onSnapshot(qRaw, (snapshot) => {
      setRawMentions(snapshot.docs.map(d => d.data()));
    });

    return () => {
      unsubLatest();
      unsubHist();
      unsubRaw();
    };
  }, [selectedTicker]);

  const triggerUpdate = async () => {
    if (!user) {
      setError("Please sign in to trigger updates.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const idToken = await auth.currentUser.getIdToken();
      const response = await fetch(`http://localhost:8080/process/${selectedTicker}`, { 
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      });
      if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
    } catch (err) {
      console.error("Update failed:", err);
      setError("Failed to trigger update. Is the backend running?");
    } finally {
      setTimeout(() => setLoading(false), 2000);
    }
  };

  const login = () => signInWithPopup(auth, googleProvider).catch(e => setError(e.message));
  const logout = () => signOut(auth);

  if (!user) {
    return (
      <div className="dashboard-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <div className="glass-card" style={{ textAlign: 'center', maxWidth: '400px', padding: '3rem' }}>
          <Activity size={64} className="text-blue-500" style={{ margin: '0 auto 1.5rem' }} />
          <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>FinVision</h1>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            Enterprise-grade stock sentiment intelligence. Please sign in to access the terminal.
          </p>
          <button onClick={login} className="ticker-badge" style={{ padding: '1rem 2rem', fontSize: '1rem', cursor: 'pointer', border: 'none' }}>
            Sign in with Google
          </button>
        </div>
      </div>
    );
  }

  const getSentimentColor = (score) => {
    if (score > 0.1) return 'var(--accent-success)';
    if (score < -0.1) return 'var(--accent-danger)';
    return 'var(--accent-primary)';
  };

  return (
    <div className="dashboard-container">
      <header className="header">
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity className="text-blue-500" /> FinVision Terminal
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Real-time Sentiment Intelligence</p>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginRight: '1rem' }}>
            <img src={user.photoURL} alt={user.displayName} style={{ width: '32px', height: '32px', borderRadius: '50%' }} />
            <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{user.displayName}</span>
            <button onClick={logout} style={{ background: 'none', border: 'none', color: 'var(--accent-danger)', cursor: 'pointer', fontSize: '0.75rem' }}>Logout</button>
          </div>
          <select 
            value={selectedTicker} 
            onChange={(e) => setSelectedTicker(e.target.value)}
          >
            {TICKERS.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <button 
            onClick={triggerUpdate}
            disabled={loading}
            className="glass-card"
            style={{ padding: '0.5rem', display: 'flex', alignItems: 'center', cursor: 'pointer' }}
          >
            <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </header>

      <main className="grid-layout">
        {/* Main Sentiment Display */}
        <section className="col-main glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <span className="ticker-badge">{selectedTicker}</span>
              <h2 style={{ marginTop: '0.5rem', color: 'var(--text-secondary)' }}>Aggregated Sentiment</h2>
              <div className="sentiment-value" style={{ color: getSentimentColor(latestData?.score || 0) }}>
                {latestData ? latestData.score.toFixed(3) : '0.000'}
              </div>
            </div>
            <div className="glass-card" style={{ textAlign: 'right' }}>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>LAST UPDATED</p>
              <p style={{ fontWeight: 600 }}>{latestData ? new Date(latestData.timestamp.seconds * 1000).toLocaleTimeString() : '--'}</p>
            </div>
          </div>

          <div className="gauge-bar">
            <div 
              className="gauge-fill" 
              style={{ 
                width: `${(( (latestData?.score || 0) + 1) / 2) * 100}%`,
                backgroundColor: getSentimentColor(latestData?.score || 0)
              }} 
            />
          </div>

          <div style={{ marginTop: '2rem', height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {historicalData.length > 0 ? (
               <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={historicalData}>
                    <defs>
                      <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={getSentimentColor(latestData?.score || 0)} stopOpacity={0.3}/>
                        <stop offset="95%" stopColor={getSentimentColor(latestData?.score || 0)} stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                    <XAxis dataKey="time" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis domain={[-1, 1]} stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                      itemStyle={{ color: '#f4f4f5' }}
                    />
                    <Area type="monotone" dataKey="score" stroke={getSentimentColor(latestData?.score || 0)} fillOpacity={1} fill="url(#colorScore)" strokeWidth={2} />
                  </AreaChart>
               </ResponsiveContainer>
            ) : (
              <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                <Activity size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                <p>No historical sentiment data available yet.</p>
                <p style={{ fontSize: '0.75rem' }}>Click refresh to fetch new data.</p>
              </div>
            )}
          </div>
        </section>

        {/* Sidebar: Insights & Mentions */}
        <section className="col-sidebar" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="glass-card">
            <h3 style={{ fontSize: '1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <BarChart3 size={18} /> Market Insights
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Volatility</span>
                <span style={{ color: 'var(--accent-success)' }}>LOW</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-secondary)' }}>Volume</span>
                <span>{latestData?.volume || 0} hits</span>
              </div>
            </div>
          </div>

          <div className="glass-card" style={{ flexGrow: 1 }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers size={18} /> Recent Mentions
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {rawMentions.map((m, i) => (
                <div key={i} style={{ fontSize: '0.8125rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--glass-border)' }}>
                  <p style={{ fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>
                    {m.platform.toUpperCase()} • {m.sentiment_score.toFixed(2)}
                  </p>
                  <p>{m.text.substring(0, 80)}...</p>
                </div>
              ))}
              {rawMentions.length === 0 && <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>No recent mentions cached.</p>}
            </div>
          </div>
        </section>
      </main>
      
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin {
          animation: spin 1s linear infinite;
        }
      `}</style>
    </div>
  );
}

export default App;
