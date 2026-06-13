import pandas as pd
import sklearn.ensemble as RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

from advisor.fund_engine import (
    calculate_fund_scores
)


def train_model():

    df = calculate_fund_scores()

    features = [
        "Sharpe",
        "Alpha",
        "Expense_Ratio",
        "Rank"
    ]

    X = df[features]

    y = df["Fund_Score"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model, df


def predict_fund_scores():

    model, df = train_model()

    features = [
        "Sharpe",
        "Alpha",
        "Expense_Ratio",
        "Rank"
    ]

    df["Predicted_Score"] = model.predict(
        df[features]
    )

    return df.sort_values(
        "Predicted_Score",
        ascending=False
    )