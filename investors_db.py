import pandas as pd
import os
from datetime import datetime

FILE_PATH = "data/investors.csv"

def save_investor(
    age,
    income,
    assets,
    liabilities,
    goal_amount,
    sip,
    risk_profile
):

    record = {
        "Date": datetime.now(),
        "Age": age,
        "Income": income,
        "Assets": assets,
        "Liabilities": liabilities,
        "Goal_Amount": goal_amount,
        "Monthly_SIP": sip,
        "Risk_Profile": risk_profile
    }

    df = pd.DataFrame([record])

    if os.path.exists(FILE_PATH):

        existing = pd.read_csv(FILE_PATH)

        df = pd.concat(
            [existing, df],
            ignore_index=True
        )

    df.to_csv(
        FILE_PATH,
        index=False
    )