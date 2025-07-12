import datetime
from sklearn.linear_model import LinearRegression
import pandas as pd

def forecast_temperature(city):
    try:
        df = pd.read_csv("static/data_log.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        X = df[["hour"]]
        y = df["temperature"]

        model = LinearRegression()
        model.fit(X, y)

        now = datetime.datetime.now()
        forecast = []
        for i in range(1, 6):
            future_time = now + datetime.timedelta(hours=i)
            pred_temp = model.predict([[future_time.hour]])[0]
            forecast.append({
                "timestamp": future_time.strftime("%Y-%m-%d %H:%M"),
                "predicted_temp": round(pred_temp, 2)
            })
        return forecast
    except Exception as e:
        print("Forecast error:", e)
        return []
