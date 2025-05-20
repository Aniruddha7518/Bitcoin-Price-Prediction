from fetch_data.fetch_yahoo import fetch_bitcoin_data
from mybtcapp.models import BitcoinPrice

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(__file__)

def train_and_save():
    df = fetch_bitcoin_data()  # Function call
    df.dropna(inplace=True)
    df.reset_index(inplace=True)

    # Check correct date column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    elif 'index' in df.columns:
        df['Date'] = pd.to_datetime(df['index'])
    else:
        raise ValueError("Date column not found.")

    # Save raw data to MySQL
    for _, row in df.iterrows():
        # Safe conversion
        try:
            date_obj = row['Date']
            if isinstance(date_obj, pd.Timestamp):
                date = date_obj.date()
            else:
                date = pd.to_datetime(date_obj).date()
        except Exception as e:
            print(f"Error parsing date for row: {row}")
            continue

        BitcoinPrice.objects.update_or_create(
            date=date,
            defaults={'close': row['Close']}
        )

    # Scale and prepare data
    data = df[['Close']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i - 60:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Build and train model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    # Save model and scaler
    model.save(os.path.join(BASE_DIR, 'model.h5'))
    joblib.dump(scaler, os.path.join(BASE_DIR, 'scaler.save'))
