from ast import Return

import yfinance as yf
import pandas as pd


def get_asset_data(
    ticker,
    period="5y"
):

    asset = yf.Ticker(
        ticker
    )

    data = asset.history(
        period=period
    )

    if data.empty:
        return None

    return data


def calculate_asset_metrics(
    ticker,
    asset_name=None
):

    df = get_asset_data(
        ticker
    )

    if df.empty:
        return None

    returns = (
        df["Close"]
        .pct_change()
        .dropna()
    )

    annual_return = (
        returns.mean()
        * 252
        * 100
    )

    volatility = (
        returns.std()
        * (252 ** 0.5)
        * 100
    )

    risk_free_rate = 6

    sharpe = (
        annual_return
        -
        risk_free_rate
    ) / volatility

    return {

        "Asset_Name":
        asset_name,

        "Ticker":
        ticker,

        "Annual Return":
        round(
            annual_return,
            2
        ),

        "Volatility":
        round(
            volatility,
            2
        ),

        "Sharpe":
        round(
            sharpe,
            2
        )
    }
    returns = df["Close"].pct_change().dropna()

    annual_return = (
        returns.mean()
        * 252
        * 100
    )

    volatility = (
        returns.std()
        * (252 ** 0.5)
        * 100
    )

    sharpe = (
        (Return - 6) / Volatility
    )

    return {

        "Ticker": ticker,

        "Annual Return":
        round(
            annual_return,
            2
        ),

        "Volatility":
        round(
            volatility,
            2
        ),

        "Sharpe":
        round(
            sharpe,
            2
        )
    }