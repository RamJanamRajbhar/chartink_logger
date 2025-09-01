from flask import Flask, request
import csv
import os
from datetime import datetime

app = Flask(__name__)

# CSV file path
CSV_FILE = "chartink_alerts.csv"

# Create file with headers if it doesn't exist
if not os.path.isfile(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Received At (Local Time)",
            "Stock",
            "Trigger Price",
            "Triggered At",
            "Scan Name",
            "Scan URL",
            "Alert Name",
            "Webhook URL"
        ])

@app.route("/", methods=["POST"])
def webhook():
    """Receive webhook JSON from Chartink and log to CSV."""
    data = request.json
    if not data:
        return "❌ No JSON received", 400

    stocks_list = data["stocks"].split(",")
    prices_list = data["trigger_prices"].split(",")

    if len(stocks_list) != len(prices_list):
        return "❌ Stock and price counts do not match", 400

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for stock, price in zip(stocks_list, prices_list):
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # local timestamp
                stock.strip(),
                price.strip(),
                data.get("triggered_at", ""),
                data.get("scan_name", ""),
                data.get("scan_url", ""),
                data.get("alert_name", ""),
                data.get("webhook_url", "")
            ])

    return "✅ Alert logged", 200


if __name__ == "__main__":
    # Host set to 0.0.0.0 so ngrok can tunnel to it
    app.run(host="0.0.0.0", port=5000)