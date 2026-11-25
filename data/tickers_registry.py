# Download the tiingo supported tickers' zip file, unzip it and load it in dataframes in RAM

import requests
import pandas #To keep the data in dataframe
import sys
import io
import zipfile
from dotenv import load_dotenv
import os

# Loads variables from .env into os.environment
load_dotenv()

URL_supported_tickers = os.getenv("URL_supported_tickers")

# Creating an empty growable memory space in the RAM - an empty file that reserves the space for the upcoming file

#requests.get sends a signal to the Tiingo server to ask for the file, stream=True means a kind of pipe has been established between the Machine and Tiingo servers so the data smoothly flows from one end to another, timeout is the patience limit, with...as response is kind of a on and off switch, when the task is done, it completely shuts down the whole process and disconnect the pipe.

def get_tiingo_ticker ():

  ram_buffer = io.BytesIO() #RAM Space created

  with requests.get(URL_supported_tickers, stream=True, timeout=30) as response:
    response.raise_for_status() #Checks if the response from the servers are fine, if it is fine, then the data gets loaded in chunks in the memory

    print("Response is OK")

    for chunk in response.iter_content (chunk_size=8192): #Loop to repeatedly append the chunks into ram buffer, it start from 8192 bytes chunk and runs until all the chunks are read.
      if chunk: #Returns True when not empty and returns false it is empty
        ram_buffer.write(chunk)

    print("All Chunks appended")

  #Bringing the pointer of memory buffer to the very first byte, ready for performing operations in the file.
  ram_buffer.seek(0) #Due to the repeated appending of the data, the pointer was in the very last byte but now we brought it forward to the very first byte.
  print("Ram Buffer Reset...")

  #Opening the zip file directly from the RAM without saving .zip file into the disk
  with zipfile.ZipFile(ram_buffer) as zf:

    print("Files inside ZIP:", zf.namelist())

    with zf.open("supported_tickers.csv") as supported_tickers:
      df = pandas.read_csv(supported_tickers)

    print(df.head())

get_tiingo_ticker()