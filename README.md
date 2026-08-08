# Remittances & Inflation in The Gambia

**Question:** How have remittance inflows and consumer price inflation moved together in The Gambia over time?

Remittances are a major share of Gambia's GDP. This project explores whether
inflows track (or diverge from) inflation trends, using publicly available
World Bank data.

## Data Sources

- **Personal remittances received (% of GDP)** — World Bank, indicator `BX.TRF.PWKR.DT.GD.ZS`
- **Personal remittances received (current US$)** — World Bank, indicator `BX.TRF.PWKR.CD.DT`
- **Consumer price inflation (annual %)** — World Bank, indicator `FP.CPI.TOTL.ZG`

All data is pulled live from the [World Bank API](https://api.worldbank.org/v2/) —
no manual downloads needed.

## Project Structure

```
gambia-remittances-inflation/
├── data/
│   ├── raw/          # Raw CSVs pulled from World Bank API
│   └── clean/        # Merged, cleaned dataset
├── notebooks/
│   └── analysis.ipynb  # Exploratory notebook version
├── scripts/
│   ├── fetch_data.py    # Pulls data from World Bank API
│   └── analyze.py       # Merges data, plots trends, runs correlation/regression
├── outputs/           # Generated charts and regression summary
├── requirements.txt
└── README.md
```

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fetch the data
python scripts/fetch_data.py

# 3. Run the analysis
python scripts/analyze.py
```

This will produce:
- `data/clean/merged_data.csv` — the merged dataset
- `outputs/remittances_vs_inflation.png` — dual-axis trend chart
- `outputs/regression_summary.txt` — OLS regression output

## Method

1. Pull annual remittance (% of GDP) and CPI inflation (%) data for The Gambia
2. Merge on year, drop missing values
3. Visualize both series on a dual-axis time series chart
4. Compute the correlation coefficient between the two series
5. Run a simple OLS regression: `CPI inflation ~ Remittances (% of GDP)`

## Findings

*(Fill this in after running the analysis — summarize the correlation
coefficient, regression result, and any notable periods where the two
series moved together or diverged.)*

## Limitations

- World Bank CPI data is general inflation, not food-specific — for a
  more targeted look at food prices, Gambia Bureau of Statistics (GBoS)
  CPI reports would give more granular, food-category-level data.
- Correlation does not imply causation — remittances and inflation may
  both be driven by external factors (exchange rates, global commodity
  prices, etc.)

## Author

Kalilu Jabbie — Economics graduate, University of The Gambia
[LinkedIn](https://www.linkedin.com/in/ibrahm-khalil-ibkj3123my) · [Credly](https://www.credly.com/users/kalilu-jabbie)
