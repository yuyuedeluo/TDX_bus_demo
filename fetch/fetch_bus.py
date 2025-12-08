import requests
import time
import json
from datetime import datetime

ROUTE = "530"  
TDX_APP_ID = "113703031-e656deb9-3fe0-4f5d"
TDX_APP_KEY = "cff0b3ef-f040-423c-b33b-ed3e1eff779a"

def get_tdx_token():
    url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": TDX_APP_ID,
        "client_secret": TDX_APP_KEY
    }
    r = requests.post(url, data=data)
    return r.json()["access_token"]

def fetch_bus(token):
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/Taipei/{ROUTE}?$format=JSON"
    headers = {"authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return r.json()

def fetch_bus_stop_info(token):
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{ROUTE}?$format=JSON"
    headers = {"authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return r.json()

def save_data(data):
    with open(f"../data/{ROUTE}_bus.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "data": data
        }, f, ensure_ascii=False, indent=2)

def main():
    token = get_tdx_token()

    while True:
        print("Fetching bus data...")
        data = fetch_bus(token)
        save_data(data)
        data_stop_info = fetch_bus_stop_info(token)
        with open(f"../data/{ROUTE}_bus_stop_info.json", "w", encoding="utf-8") as f:
            json.dump(data_stop_info, f, ensure_ascii=False, indent=2)
        print("Updated.")
        time.sleep(60)          #每 60 秒更新一次

if __name__ == "__main__":
    main()
