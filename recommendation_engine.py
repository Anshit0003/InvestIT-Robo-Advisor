from advisor.fund_engine import (
    rank_funds
)


def get_categories_for_risk(
    risk_profile
):

    if risk_profile == "Aggressive":

        return [
            "Small Cap Mutual Funds",
            "Mid Cap Mutual Funds",
            "Flexi Cap Funds",
            "Sectoral / Thematic Mutual Funds"
        ]

    elif risk_profile == "Moderate":

        return [
            "Large Cap Mutual Funds",
            "Flexi Cap Funds",
            "Large & Mid Cap Funds",
            "Aggressive Hybrid Mutual Funds"
        ]

    else:

        return [
            "Corporate Bond Mutual Funds",
            "Banking and PSU Mutual Funds",
            "Liquid Mutual Funds",
            "Money Market Funds"
        ]


def recommend_funds(
    risk_profile
):

    df = rank_funds()

    categories = get_categories_for_risk(
        risk_profile
    )

    recommendations = {}

    for category in categories:

        recommendations[category] = (

            df[
                df["sub_category"] == category
            ]

            .head(5)

        )

    return recommendations