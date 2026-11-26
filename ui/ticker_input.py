def ticker_name_input ():
  ticker_name = str(input("Ticker Name: "))
  ticker_name = ticker_name.strip().upper() #Removes all trailing spaces and make each letter capitalized

  return ticker_name
