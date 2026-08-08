"""
fetch_data.py
Pulls remittance and inflation data for The Gambia from the World Bank API
and saves raw CSVs to data/raw/.

Run this first: python scripts/fetch_data.py
"""

import requests
import pandas as pd
import os
import time

COUNTRY = "GMB"  # The Gambia
INDICATORS = {
    "remittances_pct_gdp": "BX.TRF.PWKR.DT.GD.ZS",   # Personal remittances, % of GDP
    "remittances_usd": "BX.TRF.PWKR.CD.DT",           # Personal remittances, current US$
    "cpi_inflation_pct": "FP.CPI.TOTL.ZG",             # Consumer price inflation, annual %
}

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
MAX_RETRIES = 5
TIMEOUT_SECONDS = 60


def fetch_indicator(indicator_code: str) -> pd.DataFrame:
    """Fetch a single World Bank indicator for The Gambia as a tidy DataFrame.
    Retries automatically if the connection is slow or times out."""
    url = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{indicator_code}"
    params = {"format": "json", "per_page": 200}

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            payload = response.json()
            break
        except (requests.exceptions.RequestException, ValueError) as e:
            last_error = e
            print(f"  Attempt {attempt}/{MAX_RETRIES} failed ({e.__class__.__name__}), retrying...")
            time.sleep(3)
    else:
        raise RuntimeError(f"Failed to fetch {indicator_code} after {MAX_RETRIES} attempts") from last_error

    if len(payload) < 2 or payload[1] is None:
        raise ValueError(f"No data returned for indicator {indicator_code}")

    records = payload[1]
    df = pd.DataFrame(records)[["date", "value"]]
    df = df.rename(columns={"date": "year", "value": indicator_code})
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year").reset_index(drop=True)
    return df


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    for name, code in INDICATORS.items():
        out_path = os.path.join(RAW_DIR, f"{name}.csv")
        if os.path.exists(out_path):
            print(f"Skipping {name} — already downloaded at {out_path}")
            continue

        print(f"Fetching {name} ({code})...")
        df = fetch_indicator(code)
        df.to_csv(out_path, index=False)
        print(f"  Saved {len(df)} rows to {out_path}")

    print("\nDone. Raw data is in data/raw/")


if __name__ == "__main__":
    main()