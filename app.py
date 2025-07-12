# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from weather import get_weather
from forecast import forecast_temperature
import csv
import os
from datetime import datetime

app = Flask(__name__)

DATA_LOG = "static/data_log.csv"

@app.route("/")
def dashboard():
    state = request.args.get("state", "Telangana")
    city = request.args.get("city", "Hyderabad")

    weather = get_weather(city)
    forecast = forecast_temperature(city)

    temperature = weather["temperature"]
    humidity = weather["humidity"]
    solar_radiation = weather["solar_radiation"]

    # Estimate demand
    demand = 100
    if temperature > 30:
        demand += (temperature - 30) * 5
    if humidity > 70:
        demand += 10

    # Estimate solar output and battery storage
    solar = round(solar_radiation * 0.2, 2)
    battery = min(max(solar * 0.5, 100), 1000)

    # Determine grid load status
    if demand < 150:
        status = "Normal"
    elif demand < 200:
        status = "High"
    else:
        status = "Critical"

    solar_eff = f"{round(solar / 10, 2)}%"
    savings = round(solar * 0.3, 2)

    # Log data
    log_entry = [datetime.now().strftime("%Y-%m-%d %H:%M"), temperature, solar_radiation, humidity]
    os.makedirs(os.path.dirname(DATA_LOG), exist_ok=True)
    with open(DATA_LOG, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log_entry)

    return render_template(
        "dashboard.html",
        city=city,
        state=state,
        weather=weather,
        forecast=forecast,
        demand=demand,
        solar=solar,
        battery=battery,
        status=status,
        solar_eff=solar_eff,
        savings=savings
    )

@app.route("/data")
def get_chart_data():
    try:
        with open(DATA_LOG, newline="") as f:
            reader = csv.DictReader(f)
            data = []
            for row in reader:
                data.append({
                    "timestamp": row["timestamp"],
                    "temperature": row["temperature"],
                    "solar_radiation": row["solar_radiation"],
                    "humidity": row["humidity"]
                })
            return jsonify(data)
    except Exception as e:
        print("Data read error:", e)
        return jsonify([])


@app.route("/static/<path:filename>")
def download_file(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
