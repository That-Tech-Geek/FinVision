import yfinance as yf
import json

def test_yf():
    ticker = "AAPL"
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if hist.empty:
            print(json.dumps({"error": "No data found for AAPL"}))
        else:
            print(json.dumps({
                "ticker": ticker,
                "price": hist['Close'].iloc[-1],
                "status": "success"
            }))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    test_yf()
