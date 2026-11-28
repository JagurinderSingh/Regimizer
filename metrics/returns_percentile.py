import sys
from pathlib import Path
import pandas

# Ensures Python sees the Regimizer root folder from inside metrics/
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import the variable directly from data/tiingo_data_fetcher.py
from data.tiingo_data_fetcher import ohlcv_historical_data
from ui.window_input import window_duration

def returns_percentile (ohlcv_historical_data, window_duration): # adjClose, adjHigh, adjLow, adjOpen, adjVolume

  computer_df = ohlcv_historical_data.copy()

  # 1. Sort chronologically according to the date
  computer_df["date"] = pandas.to_datetime(computer_df["date"])
  computer_df = computer_df.sort_values("date").reset_index(drop=True)

  # 2. Compute rolling 30-day cumulative return across the full period for each day using last rolling windows
  return_pct_col = f"rolling_{window_duration}d return_pct"
  computer_df[return_pct_col] = computer_df["adjClose"].pct_change(periods=window_duration)*100

  # 3. Compute each day's percentile using only the historical data available up to that specific date (avoiding look-ahead bias) - Expanding percentile
  percentile_col = f"rolling_{window_duration}d return_percentile"
  computer_df[percentile_col] = computer_df[return_pct_col].expanding().rank(pct=True) * 100

  return computer_df


computer_df = returns_percentile(ohlcv_historical_data, window_duration)

print(computer_df.head(50))
print("")
print(computer_df.tail(50))


    
    
    
    
