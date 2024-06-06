# List of all NSE-Registered Companies
require 'nsecorp'
# User searches for company through NSE Initials.
def search_company(initials)
    return nse_companies.get(initials.upcase, "Company not found")
end

while true
    initials = gets.chomp
    if initials.downcase == 'quit'
        break
    end
    puts search_company(initials)
end

# given the NSE Iitials, the model now has to search for that company on the internet to retrieve its financial data and news articles to analyze its public sentiments.
require 'httparty'
require 'nokogiri'
require 'newspaper'

def search_company(initials)
    company_name = nse_companies.get(initials.upcase, "Company not found")
    if company_name == "Company not found"
        return company_name
    else
        return company_name, retrieve_financial_data(company_name), retrieve_news_articles(company_name)
    end
end

def retrieve_financial_data(company_name)
    Company_name = company_name.gsub(" ", "+")
    Company_Name = Company_name.gsub("&", "+%26+")
    url = "https://www.google.com/search?q=#{Company_Name}+financials"
    response = HTTParty.get(url)
    if response.code == 200
        soup = Nokogiri::HTML(response.body)
        financial_data = []
        soup.css('div.rc').each do |result|
            financial_data << result.text.strip
        end
        return financial_data
    else
        return []
    end
end

def retrieve_news_articles(company_name)
    begin
        articles = Newspaper.build(company_name, memoize_articles: false)
        news_articles = []
        articles.each do |article|
            news_articles << [article.title, article.url, article.text]
        end
        return news_articles
    rescue Newspaper::ArticleException => e
        puts "Error: #{e}"
        return []
    end
end

def search_internet(company)
    # implementation of searching financials on the internet
    # you need to implement this function to retrieve the financial data
    return []
end

def calculate_cagr(initial_price, final_price, years)
    if initial_price <= 0 or final_price <= 0 or years <= 0
        return "Too less data obtained"
    else
        cagr = (final_price / initial_price) ** (1 / years) - 1
        return cagr
    end
end

def evaluate_investment(cagr, market_average)
    if cagr > market_average
        return "Good investment"
    else
        return "Forego the investment"
    end
end

def calculate_market_average(market_data)
    total_cagr = 0
    count = 0
    market_data.each do |company|
        data = search_internet(company)
        if data.length >= 10
            initial_price = data[0]
            final_price = data[-1]
            years = data.length
            cagr = calculate_cagr(initial_price, final_price, years)
            total_cagr += cagr
            count += 1
        end
    end
    if count == 0
        return "Not enough data to calculate market average"
    else
        market_average = total_cagr / count
        return market_average
    end
end

def main
    puts "Enter the list of companies in the market (comma separated): "
    market_data = gets.chomp.split(',')
    market_data = market_data.map { |company| company.strip }

    puts "Select a company from the list:"
    market_data.each_with_index do |company, index|
        puts "#{index+1}. #{company}"
    end
    company_index = gets.chomp.to_i - 1
    company = market_data[company_index]

    market_average = calculate_market_average(market_data)

    data = search_internet(company)

    if data.length < 10
        puts "Cannot evaluate investment currently"
    else
        initial_price = data[0]
        final_price = data[-1]
        years = data.length

        cagr = calculate_cagr(initial_price, final_price, years)

        result = evaluate_investment(cagr, market_average)
        puts "Investment evaluation: #{result}"
    end
end

if __FILE__ == $0
    main
end

while true
    puts "Enter NSE Initials (or 'quit' to exit): "
    initials = gets.chomp
    if initials.downcase == 'quit'
        break
    end
    company_name, financial_data, news_articles = search_company(initials)
    puts "Company Name: #{company_name}"
    puts "Financial Data:"
    financial_data.each do |title, link|
        puts "Title: #{title}, Link: #{link}"
    end
    puts "News Articles:"
    news_articles.each do |title, link, text|
        puts "Title: #{title}, Link: #{link}, Text: #{text}"
    end
end

puts "Do you want to save the data? (yes/no): "
save_data = gets.chomp.downcase
if save_data == 'yes'
    File.open("#{company_name}.txt", "w") do |f|
        f.puts "Company Name: #{company_name}"
        f.puts "Financial Data:"
        financial_data.each do |title, link|
            f.puts "Title: #{title}, Link: #{link}"
        end
        f.puts "News Articles:"
        news_articles.each do |title, link, text|
            f.puts "Title: #{title}, Link: #{link}, Text: #{text}"
        end
        puts "Data saved successfully!"
    end
else
    puts "Data not saved. Exiting the program."
    exit
end

require 'numpy'
require 'matplotlib.pyplot'
require 'scipy.stats'

# Define the NIFTY500 dictionary
require 'nifty500.py'
require 'pandas'
require 'yfinance'
require 'requests'
require 'beautifulsoup'

# Step 1: Get the list of NIFTY500 companies
nifty500 = pd.read_csv('nifty500.csv')

# Step 2: Retrieve stock prices
stock_prices = {}
nifty500['Symbol'].each do |symbol|
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1y')
    stock_prices[symbol] = hist['Close']
end

# Step 3: Retrieve company parameters
company_params = {}
nifty500['Symbol'].each do |symbol|
    url = "https://www.google.com/search?q=#{symbol}+company+info"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    company_params[symbol] = {
        'Company Name': soup.find('h3', {'class': 'r'}).text,
        'Industry': soup.find('span', {'class': 'st'}).text,
        'Sector': soup.find('span', {'class': 'st'}).text,
        # Add more parameters as needed
    }
end

# Step 4: Merge the data
df = pd.DataFrame(stock_prices).T
df = df.merge(pd.DataFrame(company_params).T, on='Symbol')

# Step 5: Analyze and visualize the data
# Calculate daily returns
df['Returns'] = df['Close'].pct_change()

# Visualize the data
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

puts "Beta Value of Target Stock: #{slope}"

if slope > 1
    puts "Volatile Stock"
elsif slope < 1
    if slope < 0
        puts "Negative Investment"
    else
        puts "Lax Stock"
    end
else
    puts "Average Stock"
end

#Add Stock reading capabilities from learnings of stock market.
require 'pandas'
require 'matplotlib.pyplot'
require 'mpl_finance'
require 'matplotlib.dates'
require 'talib'

# Load financial data from CSV file
df = pd.read_csv('nse_data.csv')

# Convert date column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Reset index and convert to OHLC format
df['date'] = df['date'].map(mpl_dates.date2num)
ohlc = df[['date', 'open', 'high', 'low', 'close']]

# Calculate candlestick patterns
patterns = talib.get_function_groups()['Pattern Recognition']

patterns.each do |pattern|
    result = talib.send(pattern, df['open'], df['high'], df['low'], df['close'])
    df[pattern] = result
end

# Plot candlestick chart
fig, ax = plt.subplots()
candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title('NSE Candlestick Chart')
plt.show()

# Analyze candlestick patterns
buy_signals = df[(df['CDLHAMMER'] == 100) | (df['CDLINVERTEDHAMMER'] == 100)]
sell_signals = df[(df['CDLSHOOTINGSTAR'] == 100) | (df['CDLEVENINGSTAR'] == 100)]

puts 'Buy Signals:'
puts buy_signals
puts 'Sell Signals:'
puts sell_signals

require 'pandas'
require 'numpy'
require 'matplotlib.pyplot'
require 'statsmodels.tsa.arima.model'
require 'sklearn.metrics'

# Load your dataset (replace with your own data)
df = pd.read_csv('prices.csv', index_col='date', parse_dates=['date'])

# Convert the index to a datetime object
df.index = pd.to_datetime(df.index)

# Resample the data to a monthly frequency (optional)
df_monthly = df.resample('M').mean()

# Plot the original data
plt.plot(df_monthly.index, df_monthly['price'])
plt.title('Original Data')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

# Split the data into training and testing sets
train_size = (0.8 * len(df_monthly)).to_i
train, test = df_monthly[0:train_size], df_monthly[train_size:]

# Define the ARIMA model
model = ARIMA(train, order=[5, 1, 0])  # p=5, d=1, q=0

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
puts model_fit.summary()

# Forecast future prices
forecast_steps = 12  # predict 12 months into the future
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Plot the forecast
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
puts "Mean Squared Error: #{mse.round(2)}"
