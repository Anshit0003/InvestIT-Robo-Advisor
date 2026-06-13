def calculate_required_sip(
    goal_amount,
    years,
    expected_return=12
):
    
    monthly_rate = expected_return / 100 / 12
    
    months = years * 12
    
    sip = (
        goal_amount *
        monthly_rate
    ) / (
        (1 + monthly_rate)**months - 1
    )
    
    return round(sip, 2)


def goal_feasibility(
    goal_amount,
    years,
    planned_sip,
    expected_return=12
):
    
    r = expected_return/100/12
    
    n = years*12
    
    future_value = (
        planned_sip *
        (((1+r)**n)-1)
    ) / r
    
    probability = (
        future_value /
        goal_amount
    ) * 100
    
    probability = min(probability,100)
    
    return round(future_value,2), round(probability,2)