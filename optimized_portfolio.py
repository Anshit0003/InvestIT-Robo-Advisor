from advisor.asset_ranker import rank_assets
from advisor.portfolio_optimizer import optimize_portfolio


def build_optimized_portfolio():

    assets = rank_assets()

    portfolio = optimize_portfolio(
        assets.head(10)
    )

    return portfolio