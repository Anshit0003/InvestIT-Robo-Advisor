import pandas as pd

FILE_PATH = "data/mutual_funds.csv"


def load_funds():

    df = pd.read_csv(FILE_PATH)

    return df


def calculate_fund_scores():

    df = load_funds()

    # Convert string columns to numeric

    numeric_cols = [
        "sortino",
        "alpha",
        "sd",
        "beta",
        "sharpe"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.fillna(0)

    # Fund Scoring Model

    df["Fund_Score"] = (

        0.20 * df["sharpe"]

        + 0.15 * df["sortino"]

        + 0.15 * df["alpha"]

        + 0.15 * df["returns_5yr"]

        + 0.10 * df["returns_3yr"]

        + 0.10 * df["rating"]

        + 0.10 *
        (
            df["fund_size_cr"]
            /
            df["fund_size_cr"].max()
        ) * 100

        - 0.05 * df["expense_ratio"]

    )

    return df


def rank_funds():

    df = calculate_fund_scores()

    df = df.sort_values(
        by="Fund_Score",
        ascending=False
    )

    return df


def get_top_funds(sub_category):

    df = rank_funds()

    return (
        df[
            df["sub_category"] == sub_category
        ]
        .head(4)
    )


def get_top_overall_funds(n=20):

    df = rank_funds()

    return df.head(n)