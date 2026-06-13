def portfolio_projection(
    sip,
    years,
    annual_return=12
):

    monthly_rate = annual_return / 100 / 12

    values = []
    year_list = []

    for year in range(1, years + 1):

        months = year * 12

        corpus = (
            sip *
            (((1 + monthly_rate) ** months) - 1)
        ) / monthly_rate

        values.append(round(corpus, 2))
        year_list.append(year)

    return year_list, values