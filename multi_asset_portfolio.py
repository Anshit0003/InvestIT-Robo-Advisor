from advisor.asset_ranker import rank_assets


def build_multi_asset_portfolio(
    risk_profile
):

    assets = rank_assets()

    if risk_profile == "Aggressive":

        allocation = {

            "Equity": 50,
            "ETF": 20,
            "Gold ETF": 15,
            "REIT": 15

        }

    elif risk_profile == "Moderate":

        allocation = {

            "Equity": 40,
            "ETF": 20,
            "Gold ETF": 20,
            "REIT": 20

        }

    else:

        allocation = {

            "Equity": 25,
            "ETF": 25,
            "Gold ETF": 30,
            "REIT": 20

        }

    portfolio = []

    for asset_class, weight in allocation.items():

        asset = assets[
            assets["Asset_Class"] == asset_class
        ].head(1)

        if len(asset) > 0:

            portfolio.append({

                "Asset":
                asset.iloc[0]["Asset_Name"],

                "Ticker":
                asset.iloc[0]["Ticker"],

                "Class":
                asset_class,

                "Weight":
                weight,

                "Sharpe":
                asset.iloc[0]["Sharpe"]

            })

    print(portfolio)

    return portfolio