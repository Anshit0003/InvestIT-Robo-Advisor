def portfolio_rebalance_check(
    current_equity,
    current_debt,
    current_gold,
    target_equity,
    target_debt,
    target_gold
):

    equity_drift = abs(
        current_equity - target_equity
    )

    debt_drift = abs(
        current_debt - target_debt
    )

    gold_drift = abs(
        current_gold - target_gold
    )

    max_drift = max(
        equity_drift,
        debt_drift,
        gold_drift
    )

    rebalance_required = (
        max_drift > 5
    )

    return {

        "Equity Drift": round(
            equity_drift, 2
        ),

        "Debt Drift": round(
            debt_drift, 2
        ),

        "Gold Drift": round(
            gold_drift, 2
        ),

        "Rebalance Required":
        rebalance_required
    }