import yfinance as yf


def backtest_asset(
    ticker,
    monthly_sip=10000,
    years=5
):

    data = yf.Ticker(
        ticker
    ).history(
        period=f"{years}y"
    )

    if data.empty:

        raise ValueError(
            f"No data found for {ticker}"
        )

    prices = data["Close"]

    monthly_prices = (
        prices
        .resample("ME")
        .last()
    )

    units = 0

    total_invested = 0

    history = []

    month = 0

    for price in monthly_prices:

        units += (
            monthly_sip
            / price
        )

        total_invested += (
            monthly_sip
        )

        current_value = (
            units * price
        )

        history.append({

            "Month": month,

            "Value": round(
                current_value,
                2
            )

        })

        month += 1

    final_value = (
        units
        *
        monthly_prices.iloc[-1]
    )

    return {

    "Ticker": ticker,

    "Invested":
    float(
        round(
            total_invested,
            2
        )
    ),

    "Final Value":
    float(
        round(
            final_value,
            2
        )
    ),

    "Profit":
    float(
        round(
            final_value
            -
            total_invested,
            2
        )
    ),

    "History":
    history

}
