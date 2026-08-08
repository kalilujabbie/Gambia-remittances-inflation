"""
analyze.py
Merges remittance and inflation data, visualizes trends, and tests
the relationship between them.

Run this after fetch_data.py: python scripts/analyze.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")


def load_and_merge():
    remit = pd.read_csv(os.path.join(RAW_DIR, "remittances_pct_gdp.csv"))
    cpi = pd.read_csv(os.path.join(RAW_DIR, "cpi_inflation_pct.csv"))

    merged = pd.merge(remit, cpi, on="year", how="inner")
    merged = merged.dropna()
    merged = merged.sort_values("year")

    os.makedirs(CLEAN_DIR, exist_ok=True)
    merged.to_csv(os.path.join(CLEAN_DIR, "merged_data.csv"), index=False)
    return merged


def plot_trends(df: pd.DataFrame):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Remittances (% of GDP)", color="tab:blue")
    ax1.plot(df["year"], df["BX.TRF.PWKR.DT.GD.ZS"], color="tab:blue", marker="o", label="Remittances (% GDP)")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("CPI Inflation (annual %)", color="tab:red")
    ax2.plot(df["year"], df["FP.CPI.TOTL.ZG"], color="tab:red", marker="s", label="CPI Inflation (%)")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    plt.title("The Gambia: Remittances vs. CPI Inflation")
    fig.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "remittances_vs_inflation.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved chart to {out_path}")


def correlation_and_regression(df: pd.DataFrame):
    corr = df["BX.TRF.PWKR.DT.GD.ZS"].corr(df["FP.CPI.TOTL.ZG"])
    print(f"\nCorrelation (remittances % GDP vs CPI inflation %): {corr:.3f}")

    try:
        import statsmodels.api as sm

        X = sm.add_constant(df["BX.TRF.PWKR.DT.GD.ZS"])
        y = df["FP.CPI.TOTL.ZG"]
        model = sm.OLS(y, X).fit()

        summary_path = os.path.join(OUTPUT_DIR, "regression_summary.txt")
        with open(summary_path, "w") as f:
            f.write(str(model.summary()))
        print(f"Saved regression summary to {summary_path}")
    except ImportError:
        print("statsmodels not installed — skipping regression. Run: pip install statsmodels")


def main():
    df = load_and_merge()
    print(f"Merged dataset: {len(df)} years, {df['year'].min()}–{df['year'].max()}")
    plot_trends(df)
    correlation_and_regression(df)


if __name__ == "__main__":
    main()
