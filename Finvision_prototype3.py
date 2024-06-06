# List of all NSE-Registered Companies
import nsecorp.py as nse_companies
# User searches for company through NSE Initials.
def search_company(initials):
    return nse_companies.get(initials.upper(), "Company not found")

while True:
    initials = input("Enter NSE Initials (or 'quit' to exit): ")
    if initials.lower() == 'quit':
        break
    print(search_company(initials))

# given the NSE Iitials, the model now has to search for that company on the internet to retrieve its financial data and news articles to analyze its public sentiments.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from newspaper import Article

def search_company(initials):
    company_name = nse_companies.get(initials.upper(), "Company not found")
    if company_name == "Company not found":
        return company_name
    else:
        return company_name, retrieve_financial_data(company_name), retrieve_news_articles(company_name)

import requests
from bs4 import BeautifulSoup

def retrieve_financial_data(company_name: str) -> list:
    # Replace spaces with +
    Company_name = company_name.replace(" ", "+")
    Company_Name = Company_name.replace("&", "+%26+")
    url = f"https://www.google.com/search?q={Company_Name}+financials"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.text, 'html.parser')
    financial_data = []

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_et_money_data(company_name):
    url = f"https://etmoney.com/search/?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for result in soup.find_all('div', class_='stock-card'):
        stock_data = {}
        stock_data['company_name'] = result.find('h2').text.strip()
        stock_data['current_price'] = result.find('span', class_='current-price').text.strip()
        stock_data['change'] = result.find('span', class_='change').text.strip()
        data.append(stock_data)
    return data

def get_nse_data(company_name):
    url = f"https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying={company_name}&instrument=FUTIDX"
    url = f"https://www.nseindia.com/get-quotes/equity?symbol={}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {}
    data['company_name'] = company_name
    data['current_price'] = soup.find('span', id='lastPrice').text.strip()
    data['open'] = soup.find('span', id='open').text.strip()
    data['high'] = soup.find('span', id='high').text.strip()
    data['low'] = soup.find('span', id='low').text.strip()
    return data

def search_financials(company):
    et_money_data = get_et_money_data(company)
    nse_data = get_nse_data(company)
    return et_money_data, nse_data
    return financial_data

def retrieve_news_articles(company_name):
    url = f"https://www.google.com/search?q={company_name}+news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = []
    for result in soup.find_all('div', class_='rc'):
        title = result.find('h3').text
        link = result.find('a')['href']
        article = Article(link)
        article.download()
        article.parse()
        news_articles.append((title, link, article.text))
    return news_articles

def search_internet(company):
    # implementation of searching financials on the internet
    # you need to implement this function to retrieve the financial data
    pass

def calculate_cagr(initial_price, final_price, years):
    if initial_price <= 0 or final_price <= 0 or years <= 0:
        return "Too less data obtained"
    else:
        cagr = (final_price / initial_price) ** (1 / years) - 1
        return cagr

def evaluate_investment(cagr, market_average):
    if cagr > market_average:
        return "Good investment"
    else:
        return "Forego the investment"

def calculate_market_average(market_data):
    total_cagr = 0
    count = 0
    for company in market_data:
        data = search_internet(company)
        if len(data) >= 10:
            initial_price = data[0]
            final_price = data[-1]
            years = len(data)
            cagr = calculate_cagr(initial_price, final_price, years)
            total_cagr += cagr
            count += 1
    if count == 0:
        return "Not enough data to calculate market average"
    else:
        market_average = total_cagr / count
        return market_average

def main():
    """
    Main function to evaluate an investment
    """
    # Get market data from user input
    market_data = input("Enter the list of companies in the market (comma separated): ").split(',')
    market_data = [company.strip() for company in market_data]

    # Ask the user to select a company from the market data
    print("Select a company from the list:")
    for i, company in enumerate(market_data):
        print(f"{i+1}. {company}")
    company_index = int(input("Enter the number of the company: ")) - 1
    company = market_data[company_index]

    # Calculate market average
    market_average = calculate_market_average(market_data)

    # Get company data from internet (assuming this function is defined elsewhere)
    data = search_internet(company)

    # Check if we have enough data to evaluate the investment
    if len(data) < 10:
        print("Cannot evaluate investment currently")
    else:
        # Extract relevant data points
        initial_price = data[0]
        final_price = data[-1]
        years = len(data)

        # Calculate CAGR
        cagr = calculate_cagr(initial_price, final_price, years)

        # Evaluate the investment
        result = evaluate_investment(cagr, market_average)
        print(f" Investment evaluation: {result}")
if __name__ == "__main__":
    main()
    
def calculate_market_average(market_data):
    total_cagr = 0
    for company in market_data:
        data = search_internet(company)
        if len(data) >= 10:
            initial_price = data[0]
            final_price = data[-1]
            years = len(data)
            cagr = calculate_cagr(initial_price, final_price, years)
            total_cagr += cagr
    market_average = total_cagr / len(market_data)
    return market_average

def main():
    company = input("Enter the company name: ")
    market_data = ["Company A", "Company B", "Company C"]  # list of companies in the market
    market_average = calculate_market_average(market_data)
    data = search_internet(company)
    if len(data) < 10:
        print("Cannot evaluate investment currently")
    else:
        initial_price = data[0]
        final_price = data[-1]
        years = len(data)
        cagr = calculate_cagr(initial_price, final_price, years)
        print(evaluate_investment(cagr, market_average))

if __name__ == "__main__":
    main()

while True:
    initials = input("Enter NSE Initials (or 'quit' to exit): ")
    if initials.lower() == 'quit':
        break
    company_name, financial_data, news_articles = search_company(initials)
    print("Company Name:", company_name)
    print("Financial Data:")
    for title, link in financial_data:
        print(f"Title: {title}, Link: {link}")
    print("News Articles:")
    for title, link, text in news_articles:
        print(f"Title: {title}, Link: {link}, Text: {text}")

print("Do you want to save the data? (yes/no): ")
save_data = input().lower()
if save_data == 'yes':
    with open(f"{company_name}.txt", "w") as f:
        f.write("Company Name: " + company_name + "\n")
        f.write("Financial Data:\n")
        for title, link in financial_data:
            f.write(f"Title: {title}, Link: {link}\n")
        f.write("News Articles:\n")
        for title, link, text in news_articles:
            f.write(f"Title: {title}, Link: {link}, Text: {text}\n")
        print("Data saved successfully!")
else:
    print("Data not saved. Exiting the program.")
    exit()
    

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Define the NIFTY500 dictionary
import nifty500.py as nifty500
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# Step 1: Get the list of NIFTY500 companies
nifty500 = pd.read_csv('nifty500.csv')

# Step 2: Retrieve stock prices
stock_prices = {}
for symbol in nifty500['Symbol']:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1y')
    stock_prices[symbol] = hist['Close']

# Step 3: Retrieve company parameters
company_params = {}
for symbol in nifty500['Symbol']:
    url = f"https://www.google.com/search?q={symbol}+company+info"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract company parameters from the search results
    company_params[symbol] = {
        'Company Name': soup.find('h3', {'class': 'r'}).text,
        'Industry': soup.find('span', {'class': 'st'}).text,
        'Sector': soup.find('span', {'class': 'st'}).text,
        # Add more parameters as needed
    }

# Step 4: Merge the data
df = pd.DataFrame(stock_prices).T
df = df.merge(pd.DataFrame(company_params).T, on='Symbol')

# Step 5: Analyze and visualize the data
# Calculate daily returns
df['Returns'] = df['Close'].pct_change()

# Visualize the data
import matplotlib.pyplot as plt
plt.plot(df['Close'])
plt.title('Stock Price Chart')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Calculate the average stock prices of NIFTY500
nifty500_avg_prices = np.mean([company['stock_prices'] for company in nifty500.values()], axis=0)

# Calculate the company's stock prices
company_prices = company_name['stock_prices']

# Calculate the regression line
slope, intercept, r_value, p_value, std_err = linregress(company_prices, nifty500_avg_prices)

# Plot the regression line
plt.scatter(company_prices, nifty500_avg_prices)
plt.plot(company_prices, intercept + slope*company_prices, 'r')
plt.xlabel('Company Stock Prices')
plt.ylabel('NIFTY500 Average Stock Prices')
plt.title('Regression Line')
plt.show()

print("Beta Value of Target Stock", slope)

if slope > 1:
    print("Volatile Stock")
elif slope < 1:
    if slope < 0:
        print("Negative Investment")
    else:
        print("Lax Stock")
else:
    print("Average Stock")

#Add Stock reading capabilities from learnings of stock market

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Load your dataset (replace with your own data)
df = pd.read_csv('prices.csv', index_col='date', parse_dates=['date'])

# Convert the index to a datetime object
df.index = pd.to_datetime(df.index)

# Resample the data to a monthly frequency (optional)
df_monthly = df.resample('M').mean()

# Plot the original data
plt.figure(figsize=(12, 6))
plt.plot(df_monthly.index, df_monthly['price'])
plt.title('Original Data')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Split the data into training and testing sets
train_size = int(0.8 * len(df_monthly))
train, test = df_monthly[0:train_size], df_monthly[train_size:]

# Define the ARIMA model
model = ARIMA(train, order=(5,1,0))  # p=5, d=1, q=0

# Fit the model
model_fit = model.fit()

# Plot the residuals
residuals = pd.DataFrame(model_fit.resid)
residuals.plot()
plt.title('Residuals')
plt.xlabel('Date')
plt.ylabel('Residual')
plt.show()

# Print the summary of the model
print(model_fit.summary())

# Forecast future prices
forecast_steps = 12  # predict 12 months into the future
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Plot the forecast
plt.figure(figsize=(12, 6))
plt.plot(df_monthly.index, df_monthly['price'], label='Original')
plt.plot(pd.date_range(start=df_monthly.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='M'), forecast, label='Forecast')
plt.fill_between(pd.date_range(start=df_monthly.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='M'), conf_int[:, 0], conf_int[:, 1], alpha=0.2, label='Confidence Interval')
plt.title('Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Evaluate the model using mean squared error
mse = mean_squared_error(test, model_fit.forecast(steps=len(test)))
print(f'Mean Squared Error: {mse:.2f}')


# Plan to track stock prices of NIFTY500 Companies, and find all parameters of them.
# Import libraries unavailable as of now.