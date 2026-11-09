import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("integrated.csv")

# Keep borough names consistent with the notebook
df["borough"] = df["borough"].str.title()

# Make sure year is numeric
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Derived measures used by RQ9 and RQ10
df["total_injuries"] = (
    df["non_severe_injuries"] + df["severe_injuries"]
)

df["violations_per_building"] = (
    df["violation_records"] / df["unique_buildings"]
)


# ============================================================
# APP
# ============================================================

app = Dash(__name__)
app.title = "NYC Safety & Traffic Insights"


# ============================================================
# LAYOUT
# ============================================================

app.layout = html.Div(
    [
        html.H1(
            "NYC Safety & Traffic Insights",
            style={"textAlign": "center"}
        ),

        html.P(
            "Explore the relationship between building safety "
            "violations and serious traffic incidents across "
            "New York City boroughs.",
            style={"textAlign": "center"}
        ),

        html.Hr(),

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        html.H2("Filters"),

        html.Label("Select a borough:"),

        dcc.Dropdown(
            id="borough-dropdown",
            options=[
                {"label": "All Boroughs", "value": "ALL"}
            ]
            + [
                {"label": borough, "value": borough}
                for borough in sorted(df["borough"].dropna().unique())
            ],
            value="ALL",
            clearable=False
        ),

        html.Br(),

        html.Label("Select a year:"),

        dcc.Dropdown(
            id="year-dropdown",
            options=[
                {"label": "All Years", "value": "ALL"}
            ]
            + [
                {"label": str(int(year)), "value": int(year)}
                for year in sorted(df["year"].dropna().unique())
            ],
            value="ALL",
            clearable=False
        ),

        html.Br(),

        html.Label("Search:"),

        dcc.Input(
            id="search-input",
            type="text",
            placeholder="Example: Brooklyn 2023",
            style={"width": "100%", "padding": "8px"}
        ),

        html.Br(),
        html.Br(),

        html.Button(
            "Generate Report",
            id="generate-button",
            n_clicks=0,
            style={"padding": "10px 20px"}
        ),

        html.Br(),
        html.Br(),

        html.Div(
            id="filter-summary",
            style={"fontWeight": "bold"}
        ),

        html.Br(),

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        html.H2("Filtered Data"),

        dash_table.DataTable(
            id="data-table",
            columns=[
                {"name": column, "id": column}
                for column in [
                    "borough",
                    "year",
                    "violation_records",
                    "unique_buildings",
                    "crash_records",
                    "non_severe_injuries",
                    "severe_injuries",
                    "fatalities"
                ]
            ],
            data=[],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left",
                "padding": "8px"
            }
        ),

        html.Hr(),

        # ----------------------------------------------------
        # VISUALIZATIONS
        # ----------------------------------------------------

        html.H2(
            "Research Questions & Visualizations",
            style={"textAlign": "center"}
        ),

        html.H3(
            "RQ1 — How did building violation records change "
            "from 2022 to 2025 across the five boroughs?"
        ),

        dcc.Graph(id="chart-1"),

        html.H3(
            "RQ2 — How did the number of unique buildings "
            "represented in the safety data change across "
            "boroughs from 2022 to 2025?"
        ),

        dcc.Graph(id="chart-2"),

        html.H3(
            "RQ3 — Which boroughs had the highest numbers "
            "of crash records in each year?"
        ),

        dcc.Graph(id="chart-3"),

        html.H3(
            "RQ4 — How do severe injuries compare across "
            "NYC boroughs and years?"
        ),

        dcc.Graph(id="chart-4"),

        html.H3(
            "RQ5 — How do non-severe injuries vary between "
            "boroughs and years?"
        ),

        dcc.Graph(id="chart-5"),

        html.H3(
            "RQ6 — Which boroughs recorded the highest "
            "numbers of fatalities across the four-year period?"
        ),

        dcc.Graph(id="chart-6"),

        html.H3(
            "RQ7 — Is there a relationship between building "
            "violation records and crash records at the "
            "borough-year level?"
        ),

        dcc.Graph(id="chart-7"),

        html.H3(
            "RQ8 — Is there a relationship between the number "
            "of unique buildings and crash records?"
        ),

        dcc.Graph(id="chart-8"),

        html.H3(
            "RQ9 — Do borough-year observations with higher "
            "violation intensity per building also show "
            "higher fatalities?"
        ),

        dcc.Graph(id="chart-9"),

        html.H3(
            "RQ10 — How does the total injury burden compare "
            "with building violation records across "
            "borough-year observations?"
        ),

        dcc.Graph(id="chart-10"),

        html.Hr(),

        # ----------------------------------------------------
        # STORY
        # ----------------------------------------------------

        html.H2(
            "The Story Behind NYC's Safety Data",
            style={"textAlign": "center"}
        ),

        html.H3("1. Our Research"),

        html.P(
            "Our project investigates the relationship between "
            "DOB building safety violations and SIRTA traffic "
            "crashes and injuries across New York City's "
            "boroughs from 2022 to 2025."
        ),

        html.H3("2. The Data"),

        html.P(
            "The analysis combines two domains: building safety "
            "and transportation safety. The datasets are "
            "integrated using borough and year, producing "
            "borough-year observations containing violation "
            "records, unique buildings, crash records, injuries, "
            "and fatalities."
        ),

        html.H3("3. Main Findings"),

        html.P(
            "The visualizations examine changes over time, "
            "differences between boroughs, and relationships "
            "between building-safety measures and transportation-"
            "safety outcomes. The cross-domain charts are "
            "descriptive and identify associations in the "
            "aggregated borough-year data."
        ),

        html.P(
            "These relationships should not be interpreted as "
            "evidence that building violations cause crashes, "
            "injuries, or fatalities."
        ),

        html.H3("4. Limitations"),

        html.P(
            "The analysis uses aggregated borough-level data, "
            "which may hide differences between individual "
            "neighborhoods or locations. The datasets also "
            "contain missing values and may reflect differences "
            "in reporting or coverage. In addition, the analysis "
            "covers 2022–2025 and uses borough-year aggregation."
        ),

        html.H3("5. Potential Impact on NYC"),

        html.P(
            "The findings could help city planners, building "
            "safety authorities, and transportation agencies "
            "identify boroughs and periods that deserve further "
            "investigation and support better-informed urban "
            "safety planning."
        )
    ],
    style={
        "maxWidth": "1200px",
        "margin": "auto",
        "padding": "20px"
    }
)


# ============================================================
# FILTER FUNCTION
# ============================================================

def filter_data(borough, year, search):

    filtered = df.copy()

    # Borough dropdown
    if borough != "ALL":
        filtered = filtered[
            filtered["borough"] == borough
        ]

    # Year dropdown
    if year != "ALL":
        filtered = filtered[
            filtered["year"] == int(year)
        ]

    # Search
    if search:
        search = search.strip().lower()

        for borough_name in df["borough"].dropna().unique():
            if borough_name.lower() in search:
                filtered = filtered[
                    filtered["borough"].str.lower()
                    == borough_name.lower()
                ]

        for year_value in df["year"].dropna().unique():
            if str(int(year_value)) in search:
                filtered = filtered[
                    filtered["year"] == int(year_value)
                ]

    return filtered


# ============================================================
# CREATE THE 10 CHARTS
# ============================================================

def create_charts(data):

    # RQ1
    chart1 = px.line(
        data,
        x="year",
        y="violation_records",
        color="borough",
        markers=True,
        title="RQ1 — Building Violation Records Over Time",
        labels={
            "year": "Year",
            "violation_records": "Violation Records",
            "borough": "Borough"
        },
        hover_data=["unique_buildings"]
    )

    # RQ2
    chart2 = px.line(
        data,
        x="year",
        y="unique_buildings",
        color="borough",
        markers=True,
        title="RQ2 — Unique Buildings Over Time",
        labels={
            "year": "Year",
            "unique_buildings": "Unique Buildings",
            "borough": "Borough"
        },
        hover_data=["violation_records"]
    )

    # RQ3
    chart3 = px.line(
        data,
        x="year",
        y="crash_records",
        color="borough",
        markers=True,
        title="RQ3 — Crash Records by Borough and Year",
        labels={
            "year": "Year",
            "crash_records": "Crash Records",
            "borough": "Borough"
        },
        hover_data=["fatalities", "severe_injuries"]
    )

    # RQ4
    chart4 = px.bar(
        data,
        x="year",
        y="severe_injuries",
        color="borough",
        barmode="group",
        title="RQ4 — Severe Injuries by Borough and Year",
        labels={
            "year": "Year",
            "severe_injuries": "Severe Injuries",
            "borough": "Borough"
        },
        hover_data=["crash_records", "fatalities"]
    )

    # RQ5
    chart5 = px.bar(
        data,
        x="year",
        y="non_severe_injuries",
        color="borough",
        barmode="group",
        title="RQ5 — Non-Severe Injuries by Borough and Year",
        labels={
            "year": "Year",
            "non_severe_injuries": "Non-Severe Injuries",
            "borough": "Borough"
        },
        hover_data=["crash_records", "severe_injuries"]
    )

    # RQ6
    chart6 = px.bar(
        data,
        x="borough",
        y="fatalities",
        color="year",
        barmode="group",
        title="RQ6 — Fatalities by Borough and Year",
        labels={
            "borough": "Borough",
            "fatalities": "Fatalities",
            "year": "Year"
        },
        hover_data=["crash_records", "severe_injuries"]
    )

    # RQ7
    chart7 = px.scatter(
        data,
        x="violation_records",
        y="crash_records",
        color="borough",
        size="unique_buildings",
        hover_name="borough",
        hover_data=[
            "year",
            "fatalities",
            "severe_injuries"
        ],
        title="RQ7 — Building Violations vs. Crash Records",
        labels={
            "violation_records": "Violation Records",
            "crash_records": "Crash Records",
            "borough": "Borough"
        }
    )

    # RQ8
    chart8 = px.scatter(
        data,
        x="unique_buildings",
        y="crash_records",
        color="borough",
        size="violation_records",
        hover_name="borough",
        hover_data=[
            "year",
            "fatalities",
            "total_injuries"
        ],
        title="RQ8 — Unique Buildings vs. Crash Records",
        labels={
            "unique_buildings": "Unique Buildings",
            "crash_records": "Crash Records",
            "borough": "Borough"
        }
    )

    # RQ9
    chart9 = px.scatter(
        data,
        x="violations_per_building",
        y="fatalities",
        color="borough",
        size="crash_records",
        hover_name="borough",
        hover_data=[
            "year",
            "violation_records",
            "unique_buildings",
            "crash_records"
        ],
        title="RQ9 — Violation Intensity vs. Fatalities",
        labels={
            "violations_per_building":
                "Violation Records per Unique Building",
            "fatalities": "Fatalities",
            "borough": "Borough"
        }
    )

    # RQ10
    chart10 = px.scatter(
        data,
        x="violation_records",
        y="total_injuries",
        color="borough",
        size="crash_records",
        symbol="year",
        hover_name="borough",
        hover_data=[
            "year",
            "unique_buildings",
            "crash_records",
            "severe_injuries",
            "fatalities"
        ],
        title="RQ10 — Building Violations vs. Total Injuries",
        labels={
            "violation_records": "Violation Records",
            "total_injuries": "Total Injuries",
            "borough": "Borough",
            "year": "Year"
        }
    )

    return [
        chart1,
        chart2,
        chart3,
        chart4,
        chart5,
        chart6,
        chart7,
        chart8,
        chart9,
        chart10
    ]


# ============================================================
# CALLBACK
# ============================================================

@app.callback(
    [
        Output("filter-summary", "children"),
        Output("data-table", "data"),
        Output("chart-1", "figure"),
        Output("chart-2", "figure"),
        Output("chart-3", "figure"),
        Output("chart-4", "figure"),
        Output("chart-5", "figure"),
        Output("chart-6", "figure"),
        Output("chart-7", "figure"),
        Output("chart-8", "figure"),
        Output("chart-9", "figure"),
        Output("chart-10", "figure")
    ],
    Input("generate-button", "n_clicks"),
    State("borough-dropdown", "value"),
    State("year-dropdown", "value"),
    State("search-input", "value")
)
def generate_report(
    n_clicks,
    borough,
    year,
    search
):

    # Before Generate Report is clicked
    if n_clicks == 0:
        empty = px.scatter(
            title="Click 'Generate Report' to display the analysis."
        )

        return (
            "",
            [],
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty,
            empty
        )

    filtered = filter_data(
        borough,
        year,
        search
    )

    # Table should only contain original 8 dataset columns
    table_columns = [
        "borough",
        "year",
        "violation_records",
        "unique_buildings",
        "crash_records",
        "non_severe_injuries",
        "severe_injuries",
        "fatalities"
    ]

    table_data = filtered[table_columns].to_dict("records")

    # Create charts from exactly the same filtered data
    charts = create_charts(filtered)

    summary = (
        f"Report generated! Showing "
        f"{len(filtered)} borough-year record(s)."
    )

    return (
        summary,
        table_data,
        *charts
    )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    app.run(debug=True) 