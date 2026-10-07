import os

import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SPEEDTEST_URL")
token = os.getenv("SPEEDTEST_TOKEN")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
params = {"page[size]": 500}


def fetch_speedtest_data():
    results = []
    next_url = f"{url}/api/v1/results"
    try:
        while next_url:
            response = requests.get(
                next_url, headers=headers, params=params, timeout=30
            )
            page = response.json()
            results.extend(page["data"])
            next_url = page["links"]["next"]
        return results
    except requests.RequestException as e:
        print(e)


if __name__ == "__main__":
    print(len(fetch_speedtest_data()))
