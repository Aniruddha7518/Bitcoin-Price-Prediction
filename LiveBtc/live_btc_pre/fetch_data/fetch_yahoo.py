import yfinance as yf
import pandas as pd

def fetch_bitcoin_data(period='1y', interval='1d'):
    df = yf.download('BTC-USD', period=period, interval=interval)

    # Forcefully flatten column names
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]

    # Try renaming if 'Close_BTC-USD' exists
    if 'Close_BTC-USD' in df.columns:
        df.rename(columns={'Close_BTC-USD': 'Close'}, inplace=True)
    elif 'Close' not in df.columns:
        raise ValueError("Expected 'Close' column not found in fetched data")

    df = df[['Close']].dropna()
    df.reset_index(inplace=True)
    return df
