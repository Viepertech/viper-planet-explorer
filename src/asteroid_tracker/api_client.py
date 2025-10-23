# api_client.py
import requests
from typing import Optional, Dict
from config import NASA_API_KEY, NEOWS_FEED_URL

def get_neo_feed_data(start_date: str, end_date: str) -> Optional[Dict]:
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY,
    }
    try:
        print(f"[api_client] Fetching NEO data {start_date} → {end_date}")
        resp = requests.get(NEOWS_FEED_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        print(f"[api_client] HTTP error: {e}\n{getattr(resp, 'text', '')[:500]}")
    except requests.RequestException as e:
        print(f"[api_client] Request error: {e}")
    return None
