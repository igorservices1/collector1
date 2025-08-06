
import requests, json, time, os
from datetime import datetime

API_KEY = "$2a$10$XXs6.9JbjHs8LNVv2GyjoeFZlEAtVG3fF3wOCkmCcu2d6uSkxFGVW"

BINOVI = {
    "aapl": "6893979ef7e7a370d1f59500", 
    "msft": "689397a0f7e7a370d1f59502", 
    "tsla": "689397a3f7e7a370d1f59504", 
    "googl": "689397a57b4b8670d8aef805", 
    "amzn": "689397a7ae596e708fc35d33",
    "nvda": "689397aa7b4b8670d8aef809", 
    "meta": "689397acae596e708fc35d39", 
    "nflx": "689397afae596e708fc35d3c", 
    "baba": "689397b17b4b8670d8aef810", 
    "amd": "689397b4f7e7a370d1f59518",
    "xom": "689397b6f7e7a370d1f5951f", 
    "f": "689397b8ae596e708fc35d4a", 
    "bito": "689397bbae596e708fc35d4e", 
    "spy": "689397bdae596e708fc35d51", 
    "qqq": "689397c0ae596e708fc35d53",
    "eurusd": "6893a14ff7e7a370d1f59dd8", 
    "usdjpy": "6893a1cd7b4b8670d8af00dd", 
    "gbpusd": "6893a2247b4b8670d8af0142", 
    "usdchf": "6893a265ae596e708fc366ca", 
    "usdcad": "6893a2aaae596e708fc3670a",
    "cl=f": "6893a3067b4b8670d8af0219", 
    "si=f": "6893a33f7b4b8670d8af0243", 
    "ng=f": "6893a3977b4b8670d8af0297", 
    "xau_usd": "68939799f7e7a370d1f594f9", 
    "eth_usd": "6893979bae596e708fc35d24"
}

finnhub_keys = [
    "d229d61r01qt8677e7ngd229d61r01qt8677e7o0",
    "d22dlg9r01qr7ajl04sgd22dlg9r01qr7ajl04t0",
    "d1pl3r9r01qu436fdcs0d1pl3r9r01qu436fdcsg"
]

def append_to_jsonbin(api_key, bin_id, novi_entry):
    url = f"https://api.jsonbin.io/v3/b/{bin_id}/latest"
    headers = {"X-Master-Key": api_key}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json().get("record", [])
            if not isinstance(data, list):
                data = [data]
        else:
            data = []
    except:
        data = []

    data.append(novi_entry)
    put_url = f"https://api.jsonbin.io/v3/b/{bin_id}"
    headers["Content-Type"] = "application/json"
    update = requests.put(put_url, headers=headers, data=json.dumps(data))
    if update.status_code == 200:
        print(f"✅ Dodat u bin {bin_id}")
    else:
        print(f"❌ Greška: {update.status_code} - {update.text}")

def sacuvaj_lokalno(entry, filename):
    try:
        os.makedirs("backup", exist_ok=True)
        with open(f"backup/{filename}.json", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"⚠️ Greška pri lokalnom upisu {filename}: {e}")

def is_weekend():
    return datetime.utcnow().weekday() >= 5

def fetch_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol[:3]}&to_currency={symbol[3:]}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    except:
        return None

def fetch_yahoo_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except:
        return None

def fetch_twelve_price(symbol):
    key = "a5879165ff4f4d03ba6e3a218a31cb24"
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={key}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["price"])
    except:
        return None

def fetch_finnhub(symbol, key):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data.get("c", 0))
    except:
        return None

def run(api_key):
    forex_keys = {
        "3QBW8KKOEHGVNVIO": ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "USDCAD"]
    }

    yahoo_symbols = {
        "CL=F": "cl=f", "SI=F": "si=f", "NG=F": "ng=f"
    }

    twelve_symbols = ["XAU/USD", "ETH/USD"]

    finnhub_symbols = [
        "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN",
        "NVDA", "META", "NFLX", "BABA", "AMD",
        "XOM", "F", "BITO", "SPY", "QQQ"
    ]

    while True:
        if is_weekend():
            print(">> Vikend – pauza.")
            time.sleep(3600)
            continue

        for key, symbols in forex_keys.items():
            for symbol in symbols:
                price = fetch_price(symbol, key)
                if price:
                    entry = {"time": datetime.utcnow().isoformat(), "symbol": symbol, "price": price}
                    sacuvaj_lokalno(entry, symbol.lower())
                    append_to_jsonbin(api_key, BINOVI[symbol.lower()], entry)
                time.sleep(5)

        for sym, fname in yahoo_symbols.items():
            price = fetch_yahoo_price(sym)
            if price:
                entry = {"time": datetime.utcnow().isoformat(), "symbol": sym, "price": price}
                sacuvaj_lokalno(entry, fname)
                append_to_jsonbin(api_key, BINOVI[fname], entry)
            time.sleep(5)

        for symbol in twelve_symbols:
            price = fetch_twelve_price(symbol)
            if price:
                fname = symbol.replace("/", "_").lower()
                entry = {"time": datetime.utcnow().isoformat(), "symbol": symbol, "price": price}
                sacuvaj_lokalno(entry, fname)
                append_to_jsonbin(api_key, BINOVI[fname], entry)
            time.sleep(5)

        for i, symbol in enumerate(finnhub_symbols):
            key = finnhub_keys[i % len(finnhub_keys)]
            price = fetch_finnhub(symbol, key)
            if price:
                entry = {"time": datetime.utcnow().isoformat(), "symbol": symbol, "price": price}
                sacuvaj_lokalno(entry, symbol.lower())
                append_to_jsonbin(api_key, BINOVI[symbol.lower()], entry)
            time.sleep(5)

        print(">> Ciklus završen. Pauza 5 minuta.")
        time.sleep(300)

if __name__ == "__main__":
    run(API_KEY)
