import numpy as np


def monte_carlo_goal_probability(
    monthly_sip,
    goal_amount,
    years,
    simulations=1000,
    mean_return=12,
    volatility=15
):

    successes = 0

    final_values = []

    for _ in range(simulations):

        corpus = 0

        for year in range(years):

            annual_return = np.random.normal(
                mean_return,
                volatility
            )

            monthly_return = (
                annual_return / 100
            ) / 12

            for month in range(12):

                corpus = (
                    corpus + monthly_sip
                ) * (
                    1 + monthly_return
                )

        final_values.append(corpus)

        if corpus >= goal_amount:
            successes += 1

    probability = (
        successes / simulations
    ) * 100

    return round(probability, 2), final_values