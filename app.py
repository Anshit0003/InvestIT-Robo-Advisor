import pandas as pd
import traceback

from advisor.portfolio_backtest import backtest_portfolio
from advisor.multi_asset_portfolio import build_multi_asset_portfolio
from advisor.charts import (
    create_allocation_chart,
    create_profit_chart
)

from advisor.projection_engine import (
    portfolio_projection
)
from advisor.charts import (
    create_allocation_chart,
    create_profit_chart
)
from advisor.investors_db import save_investor
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

from advisor.master_advisor import generate_advice
from advisor.risk_engine import (
calculate_risk_profile,
financial_health_score,
recommend_asset_allocation
)
from advisor.projection_engine import (
portfolio_projection
)

app = Dash(__name__)

app.title = "InvestIT Robo Advisor"

app.layout = html.Div([


html.H1("InvestIT Robo Advisor"),

html.Hr(),

html.H2("Investor Profile"),

html.Label("Age"),
dcc.Input(
    id="age",
    type="number",
    value=25
),

html.Br(),
html.Br(),

html.Label("Annual Income (₹)"),
dcc.Input(
    id="income",
    type="number",
    value=1200000
),

html.Br(),
html.Br(),

html.Label("Assets (₹)"),
dcc.Input(
    id="assets",
    type="number",
    value=1500000
),

html.Br(),
html.Br(),

html.Label("Liabilities (₹)"),
dcc.Input(
    id="liabilities",
    type="number",
    value=300000
),

html.Br(),
html.Br(),

html.Label("Investment Horizon (Years)"),
dcc.Input(
    id="years",
    type="number",
    value=20
),

html.Br(),
html.Br(),

html.Label("Market falls 30%. What do you do?"),

dcc.Dropdown(
    id="crash_tolerance",
    options=[
        {"label": "Sell Everything", "value": 1},
        {"label": "Wait and Hold", "value": 2},
        {"label": "Buy More", "value": 3}
    ],
    value=2
),

html.Br(),

html.H2("Goal Details"),

html.Label("Goal Amount (₹)"),
dcc.Input(
    id="goal_amount",
    type="number",
    value=10000000
),

html.Br(),
html.Br(),

html.Label("Monthly SIP (₹)"),
dcc.Input(
    id="sip",
    type="number",
    value=10000
),

html.Br(),
html.Br(),

html.Button(
    "Generate Advice",
    id="generate_btn",
    n_clicks=0
),

html.Hr(),

html.Div(id="advisor_output")

])

@app.callback(
Output("advisor_output", "children"),


Input("generate_btn", "n_clicks"),

Input("age", "value"),
Input("income", "value"),
Input("assets", "value"),
Input("liabilities", "value"),
Input("years", "value"),
Input("crash_tolerance", "value"),
Input("goal_amount", "value"),
Input("sip", "value")


)
def update_output(
    n_clicks,
    age,
    income,
    assets,
    liabilities,
    years,
    crash_tolerance,
    goal_amount,
    sip
):

    try:
        if n_clicks == 0:
            return ""

        risk_profile = calculate_risk_profile(
            age,
            income,
            years,
            crash_tolerance
        )

        portfolio = build_multi_asset_portfolio(risk_profile)
        backtest_result = backtest_portfolio(
            portfolio,
            monthly_sip=sip,
            years=min(years, 5)
        )

        save_investor(
            age,
            income,
            assets,
            liabilities,
            goal_amount,
            sip,
            risk_profile
        )

        financial_health = financial_health_score(
            income,
            assets,
            liabilities
        )

        allocation = recommend_asset_allocation(
            risk_profile
        )

        result = generate_advice(
            risk_profile=risk_profile,
            goal_amount=goal_amount,
            years=years,
            planned_sip=sip
        )

        years_list, values_list = portfolio_projection(
            sip=sip,
            years=years
        )

        projection_df = pd.DataFrame({
            "Year": years_list,
            "Projected Corpus": values_list
        })

        # compute projected corpus and goal gap for display
        projected_corpus = values_list[-1] if len(values_list) > 0 else 0
        goal_gap = goal_amount - projected_corpus

        growth_chart = px.line(
            projection_df,
            x="Year",
            y="Projected Corpus",
            title="Goal Progress Tracker"
        )

        growth_chart.add_hline(
            y=goal_amount,
            annotation_text="Goal Amount"
        )

        growth_chart.update_layout(
            xaxis_title="Years",
            yaxis_title="Portfolio Value (₹)",
            hovermode="x unified"
        )

        recommended_portfolio_table = html.Table([
            html.Tr([
                html.Th("Fund"),
                html.Th("Category"),
                html.Th("Allocation %")
            ])
        ] + [
            html.Tr([
                html.Td(item["Fund"]),
                html.Td(item["Category"]),
                html.Td(item["Allocation"])
            ])
            for item in result["Portfolio"]
        ])

        
        top_funds_rows = []
        for category, funds in result["Funds"].items():
            for fund in funds.itertuples():
                top_funds_rows.append(html.Tr([
                    html.Td(fund.scheme_name),
                    html.Td(category)
                ]))

        top_funds_table = html.Table(
            top_funds_rows,
            style={
                "width": "100%",
                "border": "1px solid black",
                "textAlign": "left"
            }
        )

        return html.Div([
            html.H2("Investor Analysis"),
            html.H3(f"Risk Profile: {risk_profile}"),
            html.H3(f"Financial Health: {financial_health}"),
            html.Hr(),
            html.H2("Goal Analysis"),
            html.H3(f"Monte Carlo Success Probability: {result['Monte Carlo Probability']}%"),
            html.H3(f"Required SIP: ₹{result['Required SIP']:,.2f}"),
            html.H3(f"Expected Corpus: ₹{result['Future Value']:,.2f}"),
            html.H3(f"Goal Success Probability: {result['Probability']}%"),
            html.Hr(),
            html.H2("Recommended Asset Allocation"),
            html.Hr(),
            html.H2("Goal Progress Tracker"),
            html.H3(
    f"Goal Amount: ₹{goal_amount:,.0f}"
),

html.H3(
    f"Projected Corpus: ₹{projected_corpus:,.0f}"
),

html.H3(
    f"Goal Gap: ₹{goal_gap:,.0f}"
),
            dcc.Graph(figure=growth_chart),
            html.Hr(),
            html.H2("Recommended Portfolio"),
            recommended_portfolio_table,
            html.Hr(),
            html.H2("Top Recommended Funds"),
            top_funds_table,
            html.Hr(),
            html.H2("Multi Asset Portfolio"),
            html.Table(
                [
                    html.Tr([
                        html.Th("Asset"),
                        html.Th("Ticker"),
                        html.Th("Asset Class"),
                        html.Th("Weight (%)")
                    ])
                ] + [
                    html.Tr([
                        html.Td(asset["Asset"]),
                        html.Td(asset["Ticker"]),
                        html.Td(asset["Class"]),
                        html.Td(asset["Weight"])
                    ])
                    for asset in portfolio
                ],
                style={"border": "1px solid black", "width": "100%", "textAlign": "center"}
            ),
            html.Hr(),
            html.H2("Historical Portfolio Backtest"),
            html.H3(f"Total Invested: ₹{backtest_result['Invested']:,.0f}"),
            html.H3(f"Final Portfolio Value: ₹{backtest_result['Final Value']:,.0f}"),
            html.H3(f"Profit Earned: ₹{backtest_result['Profit']:,.0f}"),
            html.Hr(),
            html.H3("Asset Performance"),
            html.Table(
                [
                    html.Tr([
                        html.Th("Ticker"),
                        html.Th("Invested"),
                        html.Th("Final Value"),
                        html.Th("Profit")
                    ])
                ] + [
                    html.Tr([
                        html.Td(asset["Ticker"]),
                        html.Td(f"₹{asset['Invested']:,.0f}"),
                        html.Td(f"₹{asset['Final Value']:,.0f}"),
                        html.Td(f"₹{asset['Profit']:,.0f}")
                    ])
                    for asset in backtest_result["Assets"]
                ]
            ),
            html.Hr(),
        
            html.H2("Profit Contribution"),
            dcc.Graph(figure=create_profit_chart(backtest_result))
        ])
    except Exception:
        print("\n\nERROR OCCURRED:\n")
        print(traceback.format_exc())
        return html.Div([
            html.H2("ERROR"),
            html.Pre(traceback.format_exc())
        ])
    html.Hr(),

html.P(
    "InvestIT Robo Advisor | Built by Anshit Jindal"
)


if __name__ == "__main__":
    app.run(debug=True)
