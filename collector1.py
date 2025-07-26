import requests, json, time
from datetime import datetime

# Prva grupa – Forex top 5
api_keys = {
    "3QBW8KKOEHGVNVIO": ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "USDCAD"]
}

def is_weekend():
    return datetime.utcnow().weekday() >= 5  # 5=subota, 6=nedelja

def fetch_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol[:3]}&to_currency={symbol[3:]}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        price = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        return price
    except:
        return None

def run():
    while True:
        if is_weekend():
            print(">> Vikend je – pauza.")
            time.sleep(3600)
            continue

        for key, symbols in api_keys.items():
            for symbol in symbols:
                price = fetch_price(symbol, key)
                if price:
                    entry = {
                        "time": datetime.utcnow().isoformat(),
                        "symbol": symbol,
                        "price": price
                    }
                    with open(f"{symbol.lower()}.json", "a") as f:
                        f.write(json.dumps(entry) + "\n")
                    print("Snimljeno:", entry)
                else:
                    print(f"Nema podatka za {symbol}")
                time.sleep(15)  # pauza da ne prekoračiš limit
        time.sleep(300)  # 5 minuta pauza

if __name__ == "__main__":
    run()
