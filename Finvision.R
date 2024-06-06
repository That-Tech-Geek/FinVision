# List of all NSE-Registered Companies
library(nsecorp)

# User searches for company through NSE Initials.
search_company <- function(initials) {
  company_name <- nsecorp::get(initials, "Company not found")
  if (company_name == "Company not found") {
    return(company_name)
  } else {
    return(list(company_name, retrieve_financial_data(company_name), retrieve_news_articles(company_name)))
  }
}

while (TRUE) {
  initials <- readline("Enter NSE Initials (or 'quit' to exit): ")
  if (tolower(initials) == 'quit') {
    break
  }
  result <- search_company(initials)
  if (is.list(result)) {
    company_name <- result[[1]]
    financial_data <- result[[2]]
    news_articles <- result[[3]]
    cat("Company Name:", company_name, "\n")
    cat("Financial Data:\n")
    for (data in financial_data) {
      cat(data, "\n")
    }
    cat("News Articles:\n")
    for (article in news_articles) {
      cat("Title:", article[[1]], ", URL:", article[[2]], ", Text:", article[[3]], "\n")
    }
  } else {
    cat(result, "\n")
  }
}

# given the NSE Iitials, the model now has to search for that company on the internet to retrieve its financial data and news articles to analyze its public sentiments.
library(requests)
library(rvest)
library(purrr)
library(newspaper)

retrieve_financial_data <- function(company_name) {
  # Replace spaces with +
  Company_name <- gsub(" ", "+", company_name)
  Company_Name <- gsub("&", "+%26+", Company_name)
  url <- paste0("https://www.google.com/search?q=", Company_Name, "+financials")
  response <- requests::GET(url)
  response <- response$response
  response <- response[response$status_code == 200]
  if (length(response) == 0) {
    return(NULL)
  }
  soup <- read_html(response$content)
  financial_data <- soup %>% html_nodes(".rc") %>% html_text()
  return(financial_data)
}

retrieve_news_articles <- function(company_name) {
  url <- paste0("https://www.google.com/search?q=", company_name, "+news")
  response <- requests::GET(url)
  response <- response$response
  response <- response[response$status_code == 200]
  if (length(response) == 0) {
    return(NULL)
  }
  soup <- read_html(response$content)
  news_articles <- soup %>% html_nodes(".rc") %>% html_text()
  return(news_articles)
}

search_company <- function(initials) {
  company_name <- nsecorp::get(initials, "Company not found")
  if (company_name == "Company not found") {
    return(company_name)
  } else {
    return(list(company_name, retrieve_financial_data(company_name), retrieve_news_articles(company_name)))
  }
}

while (TRUE) {
  initials <- readline("Enter NSE Initials (or 'quit' to exit): ")
  if (tolower(initials) == 'quit') {
    break
  }
  result <- search_company(initials)
  if (is.list(result)) {
    company_name <- result[[1]]
    financial_data <- result[[2]]
    news_articles <- result[[3]]
    cat("Company Name:", company_name, "\n")
    cat("Financial Data:\n")
    for (data in financial_data) {
      cat(data, "\n")
    }
    cat("News Articles:\n")
    for (article in news_articles) {
      cat("Title:", article[[1]], ", URL:", article[[2]], ", Text:", article[[3]], "\n")
    }
  } else {
    cat(result, "\n")
  }
}

retrieve_financial_data <- function(company_name) {
  # Replace spaces with +
  Company_name <- gsub(" ", "+", company_name)
  Company_Name <- gsub("&", "+%26+", Company_name)
  url <- paste0("https://www.google.com/search?q=", Company_Name, "+financials")
  response <- requests::GET(url)
  response <- response$response
  response <- response[response$status_code == 200]
  if (length(response) == 0) {
    return(NULL)
  }
  soup <- read_html(response$content)
  financial_data <- soup %>% html_nodes(".rc") %>% html_text()
  return(financial_data)
}

retrieve_news_articles <- function(company_name) {
  url <- paste0("https://www.google.com/search?q=", company_name, "+news")
  response <- requests::GET(url)
  response <- response$response
  response <- response[response$status_code == 200]
  if (length(response) == 0) {
    return(NULL)
  }
  soup <- read_html(response$content)
  news_articles <- soup %>% html_nodes(".rc") %>% html_text()
  return(news_articles)
}

search_internet <- function(company) {
  # implementation of searching financials on the internet
  # you need to implement this function to retrieve the financial data
  pass
}

calculate_cagr <- function(initial_price, final_price, years) {
  if (initial_price <= 0 || final_price <= 0 || years <= 0) {
    return("Too less data obtained")
  } else {
    cagr <- (final_price / initial_price) ^ (1 / years) - 1
    return(cagr)
  }
}

evaluate_investment <- function(cagr, market_average) {
  if (cagr > market_average) {
    return("Good investment")
  } else {
    return("Forego the investment")
  }
}

calculate_market_average <- function(market_data) {
  total_cagr <- 0
  count <- 0
  for (company in market_data) {
    data <- search_internet(company)
    if (length(data) >= 10) {
      initial_price <- data[1]
      final_price <- data[length(data)]
      years <- length(data)
      cagr <- calculate_cagr(initial_price, final_price, years)
      total_cagr <- total_cagr + cagr
      count <- count + 1
    }
  }
  if (count == 0) {
    return("Not enough data to calculate market average")
  } else {
    market_average <- total_cagr / count
    return(market_average)
  }
}

main <- function() {
  # Get market data from user input
  market_data <- readline("Enter the list of companies in the market (comma separated): ")
  market_data <- strsplit(market_data, ",")[[1]]
  market_data <- trimws(market_data)

  # Ask the user to select a company from the market data
  cat("Select a company from the list:\n")
  for (i in seq_along(market_data)) {
    cat(paste0(i, ". ", market_data[i]), "\n")
  }
  company_index <- as.integer(readline("Enter the number of the company: ")) - 1
  company <- market_data[company_index]

  # Calculate market average
  market_average <- calculate_market_average(market_data)

  # Get company data from internet (assuming this function is defined elsewhere)
  data <- search_internet(company)

  # Check if we have enough data to evaluate the investment
  if (length(data) < 10) {
    cat("Cannot evaluate investment currently\n")
  } else {
    # Extract relevant data points
    initial_price <- data[1]
    final_price <- data[length(data)]
    years <- length(data)

    # Calculate CAGR
    cagr <- calculate_cagr(initial_price, final_price, years)

    # Evaluate the investment
    result <- evaluate_investment(cagr, market_average)
    cat("Investment evaluation:", result, "\n")
  }
}

main()

while (TRUE) {
  initials <- readline("Enter NSE Initials (or 'quit' to exit): ")
  if (tolower(initials) == 'quit') {
    break
  }
  result <- search_company(initials)
  if (is.list(result)) {
    company_name <- result[[1]]
    financial_data <- result[[2]]
    news_articles <- result[[3]]
    cat("Company Name:", company_name, "\n")
    cat("Financial Data:\n")
    for (title_link in financial_data) {
      cat("Title:", title_link[[1]], ", Link:", title_link[[2]], "\n")
    }
    cat("News Articles:\n")
    for (title_link_text in news_articles) {
      cat("Title:", title_link_text[[1]], ", Link:", title_link_text[[2]], ", Text:", title_link_text[[3]], "\n")
    }
  } else {
    cat(result, "\n")
  }
}

cat("Do you want to save the data? (yes/no): ")
save_data <- tolower(readline())
if (save_data == 'yes') {
  company_name <- result[[1]]
  financial_data <- result[[2]]
  news_articles <- result[[3]]
  file_name <- paste0(company_name, ".txt")
  file_conn <- file(file_name, "w")
  cat("Company Name: ", company_name, "\n", file=file_conn)
  cat("Financial Data:\n", file=file_conn)
  for (title_link in financial_data) {
    cat("Title:", title_link[[1]], ", Link:", title_link[[2]], "\n", file=file_conn)
  }
  cat("News Articles:\n", file=file_conn)
  for (title_link_text in news_articles) {
    cat("Title:", title_link_text[[1]], ", Link:", title_link_text[[2]], ", Text:", title_link_text[[3]], "\n", file=file_conn)
  }
  close(file_conn)
  cat("Data saved successfully!\n")
} else {
  cat("Data not saved. Exiting the program.\n")
  q()
}

library(ggplot2)
library(stats)

# Define the NIFTY500 dictionary
library(nifty500)

# Step 1: Get the list of NIFTY500 companies
nifty500 <- read.csv('nifty500.csv')

# Step 2: Retrieve stock prices
stock_prices <- list()
for (symbol in nifty500$Symbol) {
  ticker <- yf::getSymbols(symbol, auto.assign = FALSE)
  stock_prices[[symbol]] <- ticker[, "Close"]
}

# Step 3: Retrieve company parameters
company_params <- list()
for (symbol in nifty500$Symbol) {
  url <- paste0("https://www.google.com/search?q=", symbol, "+company+info")
  response <- requests::GET(url)
  response <- response$response
  response <- response[response$status_code == 200]
  if (length(response) == 0) {
    next
  }
  soup <- read_html(response$content)
  company_params[[symbol]] <- list(
    'Company Name' = soup %>% html_nodes("h3.r") %>% html_text(),
    'Industry' = soup %>% html_nodes("span.st") %>% html_text(),
    'Sector' = soup %>% html_nodes("span.st") %>% html_text()
    # Add more parameters as needed
  )
}

# Step 4: Merge the data
df <- do.call(rbind, lapply(names(stock_prices), function(symbol) {
  data.frame(Symbol = symbol, Date = index(stock_prices[[symbol]]), Close = stock_prices[[symbol]], stringsAsFactors = FALSE)
}))
df <- merge(df, do.call(rbind, lapply(names(company_params), function(symbol) {
  data.frame(Symbol = symbol, CompanyName = company_params[[symbol]]$`Company Name`, Industry = company_params[[symbol]]$Industry, Sector = company_params[[symbol]]$Sector, stringsAsFactors = FALSE)
})), by = 'Symbol')

# Step 5: Analyze and visualize the data
# Calculate daily returns
df$Returns <- c(NA, diff(df$Close) / lag(df$Close))

# Visualize the data
ggplot(df, aes(x = Date, y = Close)) +
  geom_line() +
  labs(title = 'Stock Price Chart', x = 'Date', y = 'Price')

# Calculate the average stock prices of NIFTY500
nifty500_avg_prices <- rowMeans(do.call(cbind, stock_prices))

# Calculate the company's stock prices
company_prices <- stock_prices$company_name

# Calculate the regression line
regression <- lm(company_prices ~ nifty500_avg_prices)

# Plot the regression line
ggplot(df, aes(x = company_prices, y = nifty500_avg_prices)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE) +
  labs(x = "Company Stock Prices", y = "NIFTY500 Average Stock Prices", title = "Regression Line")

cat("Beta Value of Target Stock", regression$coefficients[2], "\n")

if (regression$coefficients[2] > 1) {
  cat("Volatile Stock\n")
} else if (regression$coefficients[2] < 1) {
  if (regression$coefficients[2] < 0) {
    cat("Negative Investment\n")
  } else {
    cat("Lax Stock\n")
  }
} else {
  cat("Average Stock\n")
}

#Add Stock reading capabilities from learnings of stock market.
library(pandas)
library(matplotlib)
library(mpl_finance)
library(talib)

# Load financial data from CSV file
df <- pandas::read_csv('nse_data.csv')

# Convert date column to datetime format
df$date <- pandas::to_datetime(df$date)

# Reset index and convert to OHLC format
df$date <- mpl_dates::date2num(df$date)
ohlc <- df[, c('date', 'open', 'high', 'low', 'close')]

# Calculate candlestick patterns
patterns <- talib::get_function_groups()$`Pattern Recognition`

for (pattern in patterns) {
  result <- do.call(talib::MAGIC_FUNC, c(df$open, df$high, df$low, df$close))
  df[pattern] <- result
}

# Plot candlestick chart
fig, ax <- plt::subplots()
candlestick_ohlc(ax, ohlc, width=0.6, colorup='g', colordown='r')
ax::set_xlabel('Date')
ax::set_ylabel('Price')
ax::set_title('NSE Candlestick Chart')
plt::show()

# Analyze candlestick patterns
buy_signals <- df[df$CDLHAMMER == 100 | df$CDLINVERTEDHAMMER == 100, ]
sell_signals <- df[df$CDLSHOOTINGSTAR == 100 | df$CDLEVENINGSTAR == 100, ]

cat('Buy Signals:\n')
print(buy_signals)
cat('Sell Signals:\n')
print(sell_signals)

library(pandas)
library(numpy)
library(matplotlib.pyplot)
library(statsmodels.tsa.arima.model)
library(sklearn.metrics)

# Load your dataset (replace with your own data)
df <- pandas::read_csv('prices.csv', index_col='date', parse_dates=['date'])

# Convert the index to a datetime object
df.index <- pandas::to_datetime(df.index)

# Resample the data to a monthly frequency (optional)
df_monthly <- df.resample('M').mean()

# Plot the original data
plt::figure(figsize=(12, 6))
plt::plot(df_monthly.index, df_monthly$price)
plt::title('Original Data')
plt::xlabel('Date')
plt::ylabel('Price')
plt::show()

# Split the data into training and testing sets
train_size <- as.integer(0.8 * nrow(df_monthly))
train <- df_monthly[1:train_size, ]
test <- df_monthly[(train_size + 1):nrow(df_monthly), ]

# Define the ARIMA model
model <- ARIMA(train, order=c(5, 1, 0))  # p=5, d=1, q=0

# Fit the model
model_fit <- statsmodels.tsa.arima.model::ARIMAResults(model, train)

# Plot the residuals
residuals <- pandas::DataFrame(model_fit$resid)
plt::plot(residuals)
plt::title('Residuals')
plt::xlabel('Date')
plt::ylabel('Residual')
plt::show()

# Print the summary of the model
print(model_fit)

# Forecast future prices
forecast_steps <- 12  # predict 12 months into the future
forecast <- model_fit$forecast(steps=forecast_steps)$forecast
stderr <- model_fit$forecast(steps=forecast_steps)$stderr
conf_int <- model_fit$forecast(steps=forecast_steps)$conf_int

# Plot the forecast
plt::figure(figsize=(12, 6))
plt::plot(df_monthly.index, df_monthly$price, label='Original')
plt::plot(pandas::date_range(start=df_monthly.index[length(df_monthly.index)] + pandas::Timedelta(days=1), periods=forecast_steps, freq='M'), forecast, label='Forecast')
plt::fill_between(pandas::date_range(start=df_monthly.index[length(df_monthly.index)] + pandas::Timedelta(days=1), periods=forecast_steps, freq='M'), conf_int[, 1], conf_int[, 2], alpha=0.2, label='Confidence Interval')
plt::title('Forecast')
plt::xlabel('Date')
plt::ylabel('Price')
plt::legend()
plt::show()

# Evaluate the model using mean squared error
mse <- sklearn.metrics::mean_squared_error(test, forecast)
cat(paste0('Mean Squared Error: ', mse, '\n'))