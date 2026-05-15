import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', background: '#000', color: '#f00', fontFamily: 'monospace' }}>
          <h2>SYSTEM ERROR DETECTED</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()} style={{ background: '#333', color: '#fff', border: '1px solid #555', padding: '5px 10px', cursor: 'pointer' }}>
            REBOOT SYSTEM
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
