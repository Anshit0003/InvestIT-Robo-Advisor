from advisor.fund_engine import get_top_funds


def build_portfolio(risk_profile):

    if risk_profile == "Aggressive":

        allocation = {
            "Large Cap Mutual Funds": 30,
            "Mid Cap Mutual Funds": 25,
            "Flexi Cap Funds": 25,
            "Corporate Bond Mutual Funds": 10,
            "Gold": 10
        }

    elif risk_profile == "Moderate":

        allocation = {
            "Large Cap Mutual Funds": 35,
            "Flexi Cap Funds": 25,
            "Corporate Bond Mutual Funds": 25,
            "Gold": 15
        }

    else:

        allocation = {
            "Corporate Bond Mutual Funds": 50,
            "Liquid Mutual Funds": 30,
            "Gold": 20
        }

    portfolio = []

    for category, weight in allocation.items():

        if category == "Gold":

            portfolio.append({
                "Fund": "Gold ETF",
                "Category": "Gold",
                "Allocation": weight
            })

        else:

            funds = get_top_funds(category)

            if len(funds) == 0:
                continue

            top_fund = funds.iloc[0]

            portfolio.append({
                "Fund": top_fund["scheme_name"],
                "Category": category,
                "Allocation": weight
            })

    return portfolio