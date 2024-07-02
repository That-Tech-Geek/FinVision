import yfinance as yf
import pandas as pd
import os

# Define the ticker symbol of the company
ticker_symbol = input("Enter NSE Ticker whose data needed:")

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

time = input("Enter Duration of data needed (Use mo for month and y for years.): ")

# Get the historical market data
hist = ticker.history(period=f"{time}")
print("Is hist empty?", hist.empty)

# Calculate variation factor
hist['variation_factor'] = hist['Low'] / hist['High']
hist['Average Price'] = (hist['High'] + hist['Low']) / 2
hist['Market Capital'] = hist['Average Price'] * hist['Volume']

# Export data
file_path = f"C:\\Users\\91891\\OneDrive\\Desktop\\{ticker_symbol}_Stock_{time}.csv"
export_data = hist[['Volume', 'Open', 'High', 'Low', 'Close', 'variation_factor', 'Average Price', 'Market Capital']]
print("Is export_data empty?", export_data.empty)
export_data.to_csv(file_path, index=True)
print("Has the file been created?", os.path.exists(file_path))
#StreamLit``
