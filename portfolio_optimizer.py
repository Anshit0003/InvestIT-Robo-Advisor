import pandas as pd


def optimize_portfolio(asset_df):

    df = asset_df.copy()

    # Remove negative Sharpe assets

    df = df[df["Sharpe"] > 0]

    sharpe_sum = df["Sharpe"].sum()

    df["Weight"] = (
        df["Sharpe"] / sharpe_sum
    ) * 100

    df = df.sort_values(
        by="Weight",
        ascending=False
    )

    return df[
        [
            "Asset_Name",
            "Ticker",
            "Asset_Class",
            "Sharpe",
            "Weight"
        ]
    ]