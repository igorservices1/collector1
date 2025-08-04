import requests, json, time
from datetime import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.auth import ServiceAccountCredentials

def upload_to_drive(local_filename, remote_name=None):
    if remote_name is None:
        remote_name = local_filename

    gauth = GoogleAuth()
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json",
        ["https://www.googleapis.com/auth/drive"]
    )
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': remote_name})
    file.SetContentFile(local_filename)
    file.Upload()
    print(f"📤 Poslato na Google Drive: {remote_name}")

def is_weekend():
    return datetime.utcnow().weekday() >= 5  # 5=subota, 6=nedelja
api_keys = {
    "3QBW8KKOEHGVNVIO": ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "USDCAD"]
}

def fetch_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol[:3]}&to_currency={symbol[3:]}&apikey={api_key}"
    try:
        print(f"FETCH AlphaVantage: {symbol}")
        response = requests.get(url, timeout=10)
        data = response.json()
        price = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        return price
    except Exception as e:
        print(f"Greška AlphaVantage za {symbol}: {e}")
        return None

yahoo_symbols = {
    "CL=F": "wti",
    "SI=F": "silver",
    "NG=F": "gas"
}

def fetch_yahoo_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    try:
        print(f"FETCH Yahoo: {symbol}")
        response = requests.get(url, timeout=10)
        data = response.json()
        return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except Exception as e:
        print(f"Greška Yahoo za {symbol}: {e}")
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
            upload_to_drive(f"{filename}.json")
        else:
            print(f"Nema cene za {symbol}")
        time.sleep(2)
# ----------- TWELVE DATA – XAU/USD, ETH/USD -----------
twelve_key = "a5879165ff4f4d03ba6e3a218a31cb24"
twelve_symbols = ["XAU/USD", "ETH/USD"]

def fetch_twelve_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={twelve_key}"
    try:
        print(f"FETCH Twelve: {symbol}")
        response = requests.get(url, timeout=10)
        data = response.json()
        price = float(data["price"])
        return price
    except Exception as e:
        print(f"Greška Twelve za {symbol}: {e}")
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
            upload_to_drive(filename)
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
            print(f"FETCH Finnhub 2: {symbol}")
            response = requests.get(url, timeout=10)
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
            upload_to_drive(f"{symbol.lower()}.json")
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
            print(f"FETCH Finnhub 3: {symbol}")
            response = requests.get(url, timeout=10)
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
            upload_to_drive(f"{symbol.lower()}.json")
        except Exception as e:
            print(f"Greška za {symbol} (Group 3): {e}")
        time.sleep(2)

# ----------- FINNHUB – Group 5 -----------
finnhub_api_key_5 = "d1pl3r9r01qu436fdcs0d1pl3r9r01qu436fdcsg"
finnhub_symbols_5 = ["XOM", "F", "BITO", "SPY", "QQQ"]

def run_finnhub_group5():
    for symbol in finnhub_symbols_5:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={finnhub_api_key_5}"
        try:
            print(f"FETCH Finnhub 5: {symbol}")
            response = requests.get(url, timeout=10)
            data = response.json()
            price = float(data.get("c", 0))
            entry = {
                "time": datetime.utcnow().isoformat(),
                "symbol": symbol,
                "price": price
            }
            with open(f"{symbol.lower()}.json", "a") as f:
                f.write(json.dumps(entry) + "\n")
            print("Snimljeno (Group 5):", entry)
            upload_to_drive(f"{symbol.lower()}.json")
        except Exception as e:
            print(f"Greška za {symbol} (Group 5): {e}")
        time.sleep(2)
# ----------- GLAVNA PETLJA -----------
def run():
    while True:
        start = time.time()

        if is_weekend():
            print(">> Vikend je – pauza.")
            time.sleep(3600)
            continue

        for key, symbols in api_keys.items():
            for symbol in symbols:
                price = fetch_price(symbol, key)
                print(f"FETCH Alpha: {symbol} = {price}")
                if price:
                    entry = {
                        "time": datetime.utcnow().isoformat(),
                        "symbol": symbol,
                        "price": price
                    }
                    with open(f"{symbol.lower()}.json", "a") as f:
                        f.write(json.dumps(entry) + "\n")
                    print("Snimljeno:", entry)
                    upload_to_drive(f"{symbol.lower()}.json")
                else:
                    print(f"Nema podatka za {symbol}")
                time.sleep(15)

        run_yahoo_group()
        run_twelve_group()
        run_finnhub_group2()
        run_finnhub_group3()
        run_finnhub_group5()

        end = time.time()
        trajanje = end - start
        pauza = max(0, 300 - trajanje)
        print(f">>> Ciklus trajao {trajanje:.2f}s, pauza {pauza:.2f}s")
        time.sleep(pauza)

if __name__ == "__main__":
    run()
