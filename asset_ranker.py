import pandas as pd

from advisor.asset_engine import (
    calculate_asset_metrics
)


def rank_assets():

    assets = pd.read_csv(
        "data/assets.csv"
    )

    results = []

    for _, row in assets.iterrows():

        try:

            metrics = calculate_asset_metrics(
                row["Ticker"],
                row["Asset_Name"]
            )

            if metrics is None:
                continue

            metrics["Asset_Class"] = (
                row["Asset_Class"]
            )

            results.append(
                metrics
            )

        except Exception as e:

            print(
                row["Ticker"],
                e
            )

    df = pd.DataFrame(
        results
    )

    df["Rank_Score"] = (

        0.5 * df["Sharpe"]

        +

        0.3 * (
            df["Annual Return"]
            /
            df["Annual Return"].max()
        )

        -

        0.2 * (
            df["Volatility"]
            /
            df["Volatility"].max()
        )

    )

    df = df.sort_values(
        by="Rank_Score",
        ascending=False
    )

    return df