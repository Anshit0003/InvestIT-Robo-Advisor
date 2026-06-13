import plotly.express as px
import pandas as pd


def create_allocation_chart(
    portfolio
):

    df = pd.DataFrame(portfolio)

    fig = px.pie(
        df,
        names="Asset",
        values="Weight",
        title="Portfolio Allocation"
    )

    return fig


def create_profit_chart(
    backtest_result
):

    df = pd.DataFrame(
        backtest_result["Assets"]
    )

    fig = px.bar(
        df,
        x="Ticker",
        y="Profit",
        title="Profit by Asset"
    )

    return fig