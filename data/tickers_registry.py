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

    for chunk in response.iter_content (chunk_size=8192): #Loop to repeatedly append the chunks into ram buffer, it start from 8192 bytes chunk and runs until all the chunks are read.
      if chunk: #Returns True when not empty and returns false it is empty
        ram_buffer.write(chunk)

  #Bringing the pointer of memory buffer to the very first byte, ready for performing operations in the file.
  ram_buffer.seek(0) #Due to the repeated appending of the data, the pointer was in the very last byte but now we brought it forward to the very first byte.

  #MB consumed by ram_buffer holding our zipped file
  buffer_bytes = ram_buffer.getbuffer().nbytes
  buffer_mb = buffer_bytes / (1024 ** 2)

  #print(f"RAM buffer size: {buffer_bytes:,} bytes ({buffer_mb:.2f} MB)")

  #Opening the zip file directly from the RAM without saving .zip file into the disk
  with zipfile.ZipFile(ram_buffer) as zf:

    print("Files inside ZIP:", zf.namelist())

    with zf.open("supported_tickers.csv") as supported_tickers:
      df = pandas.read_csv(supported_tickers) #Putting the csv file into the dataframe for easy access

      #Computes how much RAM this dataframe is consuming
      df_bytes = df.memory_usage(deep=True).sum() #tells pandas to measure the actual memory used by text/string data (object or str columns) instead of only measuring the memory addresses (pointers) that point to those strings.
      df_mb = df_bytes / (1024 ** 2)

      #print(f"DataFrame size: {df_bytes:,} bytes ({df_mb:.2f} MB)")


  return df, buffer_bytes, buffer_mb, df_bytes, df_mb

get_tiingo_ticker()


