import requests, json, time
from datetime import datetime

# ----------- ALPHA VANTAGE – Forex grupa -----------
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

# ----------- YAHOO FINANCE – WTI, Silver, Gas -----------
yahoo_symbols = {
    "CL=F": "wti",
    "SI=F": "silver",
    "NG=F": "gas"
}

def fetch_yahoo_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    try:
        response = requests.get(url)
        data = response.json()
        return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except Exception as e:
        print(f"Greška za {symbol}: {e}")
        return None

def run_yahoo_group():
    for symbol, filename in yahoo_symbols.items():
        price = fetch_yahoo_price(symbol)
        if price:
            entry = {
                "time": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "price": price
            }
            with open(f"{filename}.json", "a") as f:
                f.write(json.dumps(entry) + "\n")
            print("Snimljeno:", entry)
        else:
            print(f"Nema cene za {symbol}")
        time.sleep(2)

# ----------- TWELVE DATA – XAU/USD, ETH/USD -----------
twelve_key = "a5879165ff4f4d03ba6e3a218a31cb24"
twelve_symbols = ["XAU/USD", "ETH/USD"]

def fetch_twelve_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={twelve_key}"
    try:
        response = requests.get(url)
        data = response.json()
        price = float(data["price"])
        return price
    except Exception as e:
        print(f"Greška za {symbol}: {e}")
        return None

def run_twelve_group():
    for symbol in twelve_symbols:
        price = fetch_twelve_price(symbol)
        if price:
            entry = {
                "time": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "price": price
            }
            filename = f"{symbol.replace('/', '_').lower()}.json"
            with open(filename, "a") as f:
                f.write(json.dumps(entry) + "\n")
            print("Snimljeno:", entry)
        else:
            print(f"Nema podatka za {symbol}")
        time.sleep(2)

# ----------- FINNHUB – Group 2 -----------
finnhub_api_key_2 = "d229d61r01qt8677e7ngd229d61r01qt8677e7o0"
finnhub_symbols_2 = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"]

def run_finnhub_group2():
    for symbol in finnhub_symbols_2:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={finnhub_api_key_2}"
        try:
            response = requests.get(url)
            data = response.json()
            price = float(data.get("c", 0))
            entry = {
                "time": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "price": price
            }
            with open(f"{symbol.lower()}.json", "a") as f:
                f.write(json.dumps(entry) + "\n")
            print("Snimljeno (Group 2):", entry)
        except Exception as e:
            print(f"Greška za {symbol} (Group 2): {e}")
        time.sleep(2)

# ----------- FINNHUB – Group 3 -----------
finnhub_api_key_3 = "d22dlg9r01qr7ajl04sgd22dlg9r01qr7ajl04t0"
finnhub_symbols_3 = ["NVDA", "META", "NFLX", "BABA", "AMD"]

def run_finnhub_group3():
    for symbol in finnhub_symbols_3:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={finnhub_api_key_3}"
        try:
            response = requests.get(url)
            data = response.json()
            price = float(data.get("c", 0))
            entry = {
                "time": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "price": price
            }
            with open(f"{symbol.lower()}.json", "a") as f:
                f.write(json.dumps(entry) + "\n")
            print("Snimljeno (Group 3):", entry)
        except Exception as e:
            print(f"Greška za {symbol} (Group 3): {e}")
        time.sleep(2)

# ----------- GLAVNA PETLJA -----------
def run():
    while True:
        if is_weekend():
            print(">> Vikend je – pauza.")
            time.sleep(3600)
            continue

        # Alpha Vantage
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
                time.sleep(15)  # Alpha limit

        # Yahoo Finance
        run_yahoo_group()

        # Twelve Data
        run_twelve_group()

        # Finnhub Group 2
        run_finnhub_group2()

        # Finnhub Group 3
        run_finnhub_group3()

        time.sleep(300)  # 5 minuta pauza

if __name__ == "__main__":
    run()
