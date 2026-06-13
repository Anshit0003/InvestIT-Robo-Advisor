import pandas as pd

FILE_PATH = "data/investors.csv"


def load_investors():

    return pd.read_csv(FILE_PATH)


def get_total_investors():

    df = load_investors()

    return len(df)


def get_average_age():

    df = load_investors()

    return round(
        df["Age"].mean(),
        1
    )


def get_average_sip():

    df = load_investors()

    return round(
        df["Monthly_SIP"].mean(),
        0
    )


def get_risk_distribution():

    df = load_investors()

    return (
        df["Risk_Profile"]
        .value_counts()
        .to_dict()
    )