import requests, json, time
from datetime import datetime
import os

API_KEY = os.getenv("3QBW8KKOEHGVNVIO")
symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]

def fetch_price(symbol):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol[:3]}&to_currency={symbol[3:]}&apikey={API_KEY}"
    r = requests.get(url).json()
    try:
        return float(r["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except:
        return None

def run():
    while True:
        for symbol in symbols:
            price = fetch_price(symbol)
            if price:
                entry = {
                    "time": datetime.utcnow().isoformat(),
                    "symbol": symbol,
                    "price": price
                }
                with open(f"{symbol.lower()}.json", "a") as f:
                    f.write(json.dumps(entry) + "\n")
                print("Snimljeno:", entry)
        time.sleep(65)

if __name__ == "__main__":
    run()
