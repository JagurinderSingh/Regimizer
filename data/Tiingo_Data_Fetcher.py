# Testing the Tiingo End of Day Stock Price Data API

from dotenv import load_dotenv
import os
import requests
import pandas
import sys
from pathlib import Path
import io

# Loads variables from .env into os environment
load_dotenv()

from ui.ticker_input import ticker_name_input

TIINGO_EOD_API_KEY = os.getenv("Tiingo_EOD_Stock_Price_Data_API_Key")

def fetch_OHLC_data (ticker_name, start_date, end_date):

  url_fetch = f"https://api.tiingo.com/tiingo/daily/{ticker_name}/prices" #URL to hit
  headers = {"Authorization": f"Token {TIINGO_EOD_API_KEY}"} #Attaches my API Key for valid authentication request
  params = {"startDate": start_date, "endDate": end_date, "format": "csv"} #parameters to take while hitting

  # 1. Send the GET request to Tiingo
  response = requests.get(url_fetch, headers=headers, params=params, timeout=15)

  # 2. Raise an error if the ticker is invalid (404) or API key fails (401)
  if response.raise_for_status() != None:
    print(f"Request Failed. Error Code {response.raise_for_status()}")

  else:
    # 3. Convert the returned CSV text into a pandas DataFrame and return it
    ohlc_dataframe = pandas.read_csv(io.StringIO(response.text))

    return ohlc_dataframe

# Function Testing
ticker_name = ticker_name_input()
start_date = "2012-1-1"
end_date = "2016-1-1"

print(fetch_OHLC_data(ticker_name, start_date, end_date))


  









