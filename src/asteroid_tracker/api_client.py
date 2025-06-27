# api_client.py
import requests
import json
from datetime import date, timedelta
from config import NASA_API_KEY, NEOWS_FEED_URL

def get_neo_feed_data(start_date: str, end_date: str) -> dict | None:
    """
    Fetches Near-Earth Object (NEO) feed data from the NASA NeoWs API.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        dict | None: A dictionary containing the NEO data, or None if an error occurs.
    """
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "api_key": NASA_API_KEY
    }
    try:
        print(f"Fetching NEO data from {start_date} to {end_date}...")
        response = requests.get(NEOWS_FEED_URL, params=params)
        response.raise_for_status()
        print("Data fetched successfully.")
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response content: {response.text}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected request error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage for testing
    today = date.today()
    start_date_str = today.strftime("%Y-%m-%d")
    end_date_str = (today + timedelta(days=2)).strftime("%Y-%m-%d") 

    neo_data = get_neo_feed_data(start_date_str, end_date_str)
    if neo_data:
        # print(json.dumps(neo_data, indent=2)) # Uncomment to debug
        print(f"Successfully retrieved data for {len(neo_data.get('near_earth_objects', {}))} days.")
