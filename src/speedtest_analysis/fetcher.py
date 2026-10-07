import os

import requests
from dotenv import load_dotenv
from speedtest_analysis.storage import save_to_csv

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


def parsing_speedtest_data(results):
    parsed = []
    for result in results:
        if result["status"] != "completed":
            continue
        if "upload_bits" not in result:
            continue
        if "download_bits" not in result:
            continue
        parsed_dict = {
            "created_at": result["created_at"],
            "ping": result["ping"],
            "download": result["download_bits"] / 1_000_000,
            "upload": result["upload_bits"] / 1_000_000,
        }
        parsed.append(parsed_dict)
    return parsed


if __name__ == "__main__":
    results = fetch_speedtest_data()
    parsed = parsing_speedtest_data(results)
    save_to_csv(parsed)
    print(len(parsed))
    print(parsed[0])
