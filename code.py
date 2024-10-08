import streamlit as st
import yfinance as yf
import pandas as pd
from fbprophet import Prophet

# Set the app title and description
st.title("FinVision by AlfaZeta")
st.markdown("""
**Unveiling the future of market intelligence with AlfaZeta’s latest innovation, FinVision.**
This state-of-the-art AI model is engineered to navigate the complexities of financial markets, offering unparalleled predictive insights.
Whether you’re a seasoned investor or a financial novice, FinVision equips you with foresight to make informed decisions, stay ahead of the curve, and capitalize on emerging opportunities.
With FinVision, AlfaZeta is not just predicting the future; we’re defining it.
""")

# Sidebar for ticker input
st.sidebar.header("Stock Selection")
ticker = st.sidebar.text_input("Enter the stock ticker symbol", "AAPL")

# Function to fetch stock data using yfinance
def load_data(ticker):
    stock_data = yf.download(ticker, period="max", progress=False)
    stock_data.reset_index(inplace=True)
    return stock_data

# Load and display stock data
data = load_data(ticker)
st.subheader(f"Stock Data for {ticker}")
st.line_chart(data[['Date', 'Close']].set_index('Date'))

# Prepare data for Prophet
df_prophet = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

# Initialize Prophet model
model = Prophet()
model.fit(df_prophet)

# Make future predictions
future = model.make_future_dataframe(periods=30)  # Predict 30 days into the future
forecast = model.predict(future)

# Display predictive insights
st.subheader("Predictive Market Insights")
st.line_chart(forecast[['ds', 'yhat']].set_index('ds'))
st.write("Predictions generated by FinVision's state-of-the-art AI model.")

# Option to download the data
st.sidebar.header("Download Data")
st.sidebar.download_button(label="Download data as CSV", data=forecast.to_csv(), file_name=f"{ticker}_finvision_predictions.csv", mime='text/csv')
