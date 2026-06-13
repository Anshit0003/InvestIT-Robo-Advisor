from advisor.monte_carlo_engine import monte_carlo_goal_probability
from advisor.goal_engine import calculate_required_sip, goal_feasibility
from advisor.fund_engine import get_top_funds
from advisor.portfolio_engine import build_portfolio


def generate_advice(
    risk_profile,
    goal_amount,
    years,
    planned_sip
):

    sip_needed = calculate_required_sip(
        goal_amount,
        years
    )
    

    future_value, probability = goal_feasibility(
        goal_amount,
        years,
        planned_sip
    )

    mc_probability, mc_values = monte_carlo_goal_probability(
        monthly_sip=planned_sip,
        goal_amount=goal_amount,
        years=years
    )

    if risk_profile == "Aggressive":
        categories = [
            "Large Cap Mutual Funds",
            "Mid Cap Mutual Funds",
            "Flexi Cap Funds"
        ]
    elif risk_profile == "Moderate":
        categories = [
            "Large Cap Mutual Funds",
            "Flexi Cap Funds",
            "Aggressive Hybrid Mutual Funds"
        ]
    else:
        categories = [
            "Corporate Bond Mutual Funds",
            "Liquid Mutual Funds"
        ]

    recommendations = {}

    for category in categories:

        recommendations[category] = get_top_funds(
            category
        )

    portfolio = build_portfolio(
        risk_profile
    )

    return {

        "Required SIP": sip_needed,

        "Future Value": future_value,

        "Probability": probability,

        "Monte Carlo Probability": mc_probability,

        "Funds": recommendations,

        "Portfolio": portfolio
    }