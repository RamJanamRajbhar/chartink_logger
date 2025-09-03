from flask import Flask, request
import os
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback

app = Flask(__name__)

# Setup Google Sheets API using credentials from Render environment variable
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
key_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
client = gspread.authorize(creds)
print("✅ Google Sheets client authorized")

# Open your sheet by name
sheet = client.open("Chartink Alerts").sheet1  # Make sure this matches your sheet name exactly

@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.json
        if not data:
            return "❌ No JSON received", 400

        stocks_list = data["stocks"].split(",")
        prices_list = data["trigger_prices"].split(",")

        if len(stocks_list) != len(prices_list):
            return "❌ Stock and price counts do not match", 400

        print("📌 Entering Google Sheets logging block")

        for stock, price in zip(stocks_list, prices_list):
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                stock.strip(),
                price.strip(),
                data.get("triggered_at", ""),
                data.get("scan_name", ""),
                data.get("scan_url", ""),
                data.get("alert_name", ""),
                data.get("webhook_url", "")
            ])
            print(f"✅ Logged to Google Sheets: {stock.strip()} at {price.strip()}")

        return "✅ Alert logged to Google Sheets", 200

    except Exception as e:
        print("🔥 Top-level error caught")
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return f"❌ Fatal error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)