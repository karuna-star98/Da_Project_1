"""
Standard Interactive Dashboard Template (Plotly Dash)

Install:
    python -m pip install dash pandas numpy plotly

Run:
    python dash_dashboard.py

Open:
    http://127.0.0.1:8050
"""

import numpy as np
import pandas as pd
import plotly.express as px

from dash import Dash, Input, Output, dcc, html


# ---------------------------------------------------------------
# 1. DATA LAYER (replace with your own data source)
# ---------------------------------------------------------------

rng = np.random.default_rng(42)

n = 5000

df = pd.DataFrame(
    {
        "date": pd.to_datetime("2025-01-01")
        + pd.to_timedelta(
            rng.integers(0, 365, n),
            unit="D"
        ),

        "region": rng.choice(
            ["North", "South", "East", "West"],
            n
        ),

        "category": rng.choice(
            ["Electronics", "Clothing", "Home", "Sports"],
            n
        ),

        "units": rng.integers(1, 10, n),

        "unit_price": rng.uniform(10, 200, n).round(2),
    }
)

df["revenue"] = df["units"] * df["unit_price"]


# ---------------------------------------------------------------
# 2. DASH APP AND LAYOUT
# ---------------------------------------------------------------

app = Dash(__name__)

app.title = "Interactive Sales Dashboard"


# Style for KPI cards

CARD = {
    "backgroundColor": "#f8f9fa",
    "padding": "18px",
    "borderRadius": "10px",
    "border": "1px solid #dee2e6",
    "boxShadow": "0 2px 5px rgba(0,0,0,0.08)",
    "flex": "1",
    "minWidth": "150px",
}


# Dashboard layout

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "25px",
        "maxWidth": "1400px",
        "margin": "auto",
        "backgroundColor": "#ffffff",
    },

    children=[
        # Dashboard heading

        html.H1(
            "Interactive Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#243447",
            },
        ),

        html.P(
            "Explore sales revenue using interactive filters.",
            style={
                "textAlign": "center",
                "color": "#666666",
                "marginBottom": "30px",
            },
        ),


        # -------------------------------------------------------
        # FILTERS
        # -------------------------------------------------------

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginBottom": "25px",
                "alignItems": "flex-end",
            },

            children=[
                # Region filter

                html.Div(
                    style={"flex": "1", "minWidth": "200px"},

                    children=[
                        html.Label("Region"),

                        dcc.Dropdown(
                            id="region-filter",

                            options=[
                                {
                                    "label": region,
                                    "value": region,
                                }
                                for region in sorted(
                                    df["region"].unique()
                                )
                            ],

                            value=sorted(
                                df["region"].unique()
                            ),

                            multi=True,

                            placeholder="Select regions",
                        ),
                    ],
                ),


                # Category filter

                html.Div(
                    style={"flex": "1", "minWidth": "200px"},

                    children=[
                        html.Label("Category"),

                        dcc.Dropdown(
                            id="category-filter",

                            options=[
                                {
                                    "label": category,
                                    "value": category,
                                }
                                for category in sorted(
                                    df["category"].unique()
                                )
                            ],

                            value=sorted(
                                df["category"].unique()
                            ),

                            multi=True,

                            placeholder="Select categories",
                        ),
                    ],
                ),


                # Date range filter

                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "280px",
                    },

                    children=[
                        html.Label("Date Range"),

                        html.Br(),

                        dcc.DatePickerRange(
                            id="date-filter",

                            min_date_allowed=(
                                df["date"].min().date()
                            ),

                            max_date_allowed=(
                                df["date"].max().date()
                            ),

                            start_date=(
                                df["date"].min().date()
                            ),

                            end_date=(
                                df["date"].max().date()
                            ),

                            display_format="DD-MM-YYYY",
                        ),
                    ],
                ),
            ],
        ),


        # -------------------------------------------------------
        # KPI CARDS
        # -------------------------------------------------------

        html.Div(
            id="kpi-row",

            style={
                "display": "flex",
                "gap": "16px",
                "flexWrap": "wrap",
                "marginBottom": "25px",
            },
        ),


        # -------------------------------------------------------
        # MONTHLY REVENUE TREND
        # -------------------------------------------------------

        dcc.Graph(
            id="trend-chart",
        ),


        # -------------------------------------------------------
        # CATEGORY AND REGION CHARTS
        # -------------------------------------------------------

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },

            children=[
                dcc.Graph(
                    id="category-chart",
                    style={
                        "flex": "1",
                        "minWidth": "300px",
                    },
                ),

                dcc.Graph(
                    id="region-chart",
                    style={
                        "flex": "1",
                        "minWidth": "300px",
                    },
                ),
            ],
        ),
    ],
)


# ---------------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------------

def filter_data(
    regions,
    categories,
    start,
    end
) -> pd.DataFrame:

    regions = regions or []
    categories = categories or []

    # Return an empty dataset if required filters are missing

    if not regions or not categories or not start or not end:
        return df.iloc[0:0]

    # Apply region, category and date filters

    filtered_df = df[
        df["region"].isin(regions)
        & df["category"].isin(categories)
        & df["date"].between(
            pd.Timestamp(start),
            pd.Timestamp(end)
        )
    ]

    return filtered_df


def kpi_card(title: str, value: str) -> html.Div:

    return html.Div(
        style=CARD,

        children=[
            html.Div(
                title,
                style={"color": "#666666"},
            ),

            html.H2(
                value,
                style={"margin": "4px 0 0"},
            ),
        ],
    )


# ---------------------------------------------------------------
# 4. CALLBACKS
# One callback updates all outputs from the filters
# ---------------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),

    Output("trend-chart", "figure"),

    Output("category-chart", "figure"),

    Output("region-chart", "figure"),

    Input("region-filter", "value"),

    Input("category-filter", "value"),

    Input("date-filter", "start_date"),

    Input("date-filter", "end_date"),
)


def update_dashboard(
    regions,
    categories,
    start,
    end
):

    # Filter the dataset

    d = filter_data(
        regions,
        categories,
        start,
        end
    )


    # -----------------------------------------------------------
    # Handle empty selection
    # -----------------------------------------------------------

    if d.empty:

        kpis = [
            kpi_card("Total Revenue", "$0"),

            kpi_card("Orders", "0"),

            kpi_card("Avg Order Value", "$0.00"),

            kpi_card("Units Sold", "0"),
        ]

        empty_trend = px.scatter(
            title="No data for the selected filters"
        )

        empty_category = px.scatter(
            title="No category data available"
        )

        empty_region = px.scatter(
            title="No region data available"
        )

        return (
            kpis,
            empty_trend,
            empty_category,
            empty_region,
        )


    # -----------------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------------

    kpis = [
        kpi_card(
            "Total Revenue",
            f"${d['revenue'].sum():,.0f}"
        ),

        kpi_card(
            "Orders",
            f"{len(d):,}"
        ),

        kpi_card(
            "Avg Order Value",
            f"${d['revenue'].mean():,.2f}"
        ),

        kpi_card(
            "Units Sold",
            f"{d['units'].sum():,}"
        ),
    ]


    # -----------------------------------------------------------
    # CHART 1: MONTHLY REVENUE TREND
    # -----------------------------------------------------------

    monthly = (
        d.set_index("date")
        .resample("MS")["revenue"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        monthly,

        x="date",

        y="revenue",

        markers=True,

        title="Monthly Revenue Trend",

        labels={
            "date": "Month",
            "revenue": "Revenue ($)",
        },
    )

    fig_trend.update_layout(
        template="plotly_white",
        hovermode="x unified",
    )


    # -----------------------------------------------------------
    # CHART 2: REVENUE BY CATEGORY
    # -----------------------------------------------------------

    by_cat = (
        d.groupby(
            "category",
            as_index=False
        )["revenue"]
        .sum()
        .sort_values("revenue")
    )

    fig_cat = px.bar(
        by_cat,

        x="revenue",

        y="category",

        orientation="h",

        title="Revenue by Category",

        labels={
            "category": "Category",
            "revenue": "Revenue ($)",
        },
    )

    fig_cat.update_layout(
        template="plotly_white",
    )


    # -----------------------------------------------------------
    # CHART 3: REVENUE BY REGION
    # -----------------------------------------------------------

    by_reg = (
        d.groupby(
            "region",
            as_index=False
        )["revenue"]
        .sum()
    )

    fig_reg = px.bar(
        by_reg,

        x="region",

        y="revenue",

        title="Revenue by Region",

        labels={
            "region": "Region",
            "revenue": "Revenue ($)",
        },
    )

    fig_reg.update_layout(
        template="plotly_white",
    )


    # Return all dashboard components

    return (
        kpis,
        fig_trend,
        fig_cat,
        fig_reg,
    )


# ---------------------------------------------------------------
# 5. RUN THE DASH APPLICATION
# ---------------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)