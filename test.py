import requests

url = "https://chartink-logger.onrender.com"  # Replace with your actual Replit URL

payload = {
    "stocks": "SEPOWER,ASTEC,EDUCOMP",
    "trigger_prices": "3.75,541.8,2.1",
    "triggered_at": "2:34 pm",
    "scan_name": "Short term breakouts",
    "scan_url": "short-term-breakouts",
    "alert_name": "Alert for Short term breakouts",
    "webhook_url": url
}

response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Response:", response.text)