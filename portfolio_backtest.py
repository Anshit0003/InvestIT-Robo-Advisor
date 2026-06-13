from advisor.backtest_engine import (
    backtest_asset
)


def backtest_portfolio(
    portfolio,
    monthly_sip=10000,
    years=5
):

    results = []

    total_invested = 0

    total_value = 0

    combined_history = {}

    for asset in portfolio:

        asset_sip = (
            monthly_sip
            *
            asset["Weight"]
            / 100
        )

        try:

            result = backtest_asset(
                asset["Ticker"],
                monthly_sip=asset_sip,
                years=years
            )

            results.append(
                result
            )

            total_invested += (
                result["Invested"]
            )

            total_value += (
                result["Final Value"]
            )

            # Combine history

            for point in result["History"]:

                month = point["Month"]

                value = point["Value"]

                if month not in combined_history:

                    combined_history[month] = 0

                combined_history[month] += value

        except Exception as e:

            print(
                f"Skipping {asset['Ticker']}: {e}"
            )

    portfolio_history = []

    for month in sorted(
        combined_history.keys()
    ):

        portfolio_history.append({

            "Month": month,

            "Value": round(
                combined_history[month],
                2
            )

        })

    return {

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
                total_value,
                2
            )
        ),

        "Profit":
        float(
            round(
                total_value
                -
                total_invested,
                2
            )
        ),

        "Assets":
        results,

        "History":
        portfolio_history

    }