import numpy as np
import joblib
import os
from datetime import timedelta, datetime
from tensorflow.keras.models import load_model

from mybtcapp.models import BitcoinPrediction, BitcoinPrice

BASE_DIR = os.path.dirname(__file__)

def predict_next_10_days():
    # Load model and scaler
    model = load_model(os.path.join(BASE_DIR, 'model.h5'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.save'))

    # Get last 60 actual prices from DB
    recent_prices = BitcoinPrice.objects.order_by('-date')[:60]
    recent_prices = sorted(recent_prices, key=lambda x: x.date)  # Oldest to newest

    if len(recent_prices) < 60:
        print(f" Not enough data to make prediction. Only {len(recent_prices)} entries found.")
        return

    close_prices = np.array([p.close for p in recent_prices]).reshape(-1, 1)

    # Check for empty or invalid data
    if close_prices.size == 0:
        print(" close_prices array is empty. Cannot proceed.")
        return

    # Scale the prices safely
    try:
        scaled_input = scaler.transform(close_prices)
    except Exception as e:
        print(f" Error during scaling input: {e}")
        return

    predictions = []
    input_seq = scaled_input.copy()

    for _ in range(10):
        x_input = input_seq[-60:].reshape(1, 60, 1)
        pred_scaled = model.predict(x_input, verbose=0)
        pred_actual = scaler.inverse_transform(pred_scaled)[0][0]
        predictions.append(pred_actual)

        # Append the predicted value (scaled) to sequence for next prediction
        input_seq = np.append(input_seq, pred_scaled)[-60:]

    # Save predictions to DB
    last_date = recent_prices[-1].date
    for i, price in enumerate(predictions):
        future_date = last_date + timedelta(days=i+1)
        BitcoinPrediction.objects.update_or_create(
            date=future_date,
            defaults={'predicted_close': price}
        )

    print(" 10-day predictions saved successfully.")
    return predictions
