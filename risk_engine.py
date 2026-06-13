# advisor/risk_engine.py

def calculate_risk_profile(
    age,
    income,
    horizon,
    crash_tolerance
):
    """
    Determines investor risk profile.

    crash_tolerance:
    1 = Sell Everything
    2 = Wait
    3 = Buy More
    """

    score = 0

    # Age Score
    if age < 35:
        score += 3
    elif age < 50:
        score += 2
    else:
        score += 1

    # Income Score
    if income > 2000000:
        score += 3
    elif income > 1000000:
        score += 2
    else:
        score += 1

    # Investment Horizon Score
    if horizon > 15:
        score += 3
    elif horizon > 7:
        score += 2
    else:
        score += 1

    # Market Crash Behaviour Score
    score += crash_tolerance

    # Final Classification
    if score >= 10:
        return "Aggressive"

    elif score >= 7:
        return "Moderate"

    else:
        return "Conservative"


def financial_health_score(
    income,
    assets,
    liabilities
):
    """
    Evaluates financial health.
    """

    ratio = assets / max(liabilities, 1)

    if ratio >= 3:
        return "Strong"

    elif ratio >= 1:
        return "Average"

    else:
        return "Weak"


def recommend_asset_allocation(
    risk_profile
):
    """
    Returns recommended portfolio allocation.
    """

    allocations = {
        "Aggressive": {
            "Equity": 70,
            "Debt": 20,
            "Gold": 10
        },

        "Moderate": {
            "Equity": 50,
            "Debt": 30,
            "Gold": 20
        },

        "Conservative": {
            "Equity": 30,
            "Debt": 50,
            "Gold": 20
        }
    }

    return allocations[risk_profile]