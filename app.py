
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table


# ==========================================
# 1. LOAD THE INTEGRATED DATASET
# ==========================================

df = pd.read_csv("integrated.csv")

# Ensure year is numeric
df["year"] = pd.to_numeric(df["year"], errors="coerce")


# ==========================================
# 2. CREATE THE DASH APP
# ==========================================

app = Dash(__name__)
app.title = "NYC Safety & Traffic Insights"


# ==========================================
# 3. WEBSITE LAYOUT
# ==========================================

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

        html.H3("Explore the Data"),

        # Borough filter
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

        # Year filter
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

        # Search
        html.Label("Search:"),

        dcc.Input(
            id="search-input",
            type="text",
            placeholder="Example: Brooklyn 2023",
            style={"width": "100%", "padding": "10px"}
        ),

        html.Br(),
        html.Br(),

        # Generate Report button
        html.Button(
            "Generate Report",
            id="generate-button",
            n_clicks=0,
            style={
                "padding": "10px 20px",
                "cursor": "pointer"
            }
        ),

        html.Br(),
        html.Br(),

        # Summary
        html.Div(
            id="filter-summary",
            style={
                "fontWeight": "bold",
                "fontSize": "18px"
            }
        ),

        html.Hr(),

        # ==================================
        # 4. INTERACTIVE VISUALIZATIONS
        # ==================================

        html.H2("Data Visualizations"),

        html.H3("1. DOB Safety Violations Over Time"),

        dcc.Graph(id="dob-trend-chart"),

        html.P(
            "This chart shows how building safety violation "
            "records changed across NYC boroughs from 2022 to 2025."
        ),

        html.Hr(),

        html.H3("2. SIRTA Traffic Crash Records Over Time"),

        dcc.Graph(id="sirta-trend-chart"),

        html.P(
            "This chart compares the number of traffic crash "
            "records across NYC boroughs and years."
        ),

        html.Hr(),

        html.H3("3. Building Violations vs. Traffic Crashes"),

        dcc.Graph(id="relationship-chart"),

        html.P(
            "Each point represents one borough-year combination. "
            "The chart explores the association between building "
            "safety violation records and traffic crash records."
        ),

        html.Hr(),

        # ==================================
        # 5. FILTERED DATA TABLE
        # ==================================

        html.H2("Filtered Integrated Dataset"),

        dash_table.DataTable(
            id="data-table",

            columns=[
                {"name": column, "id": column}
                for column in df.columns
            ],

            data=[],

            style_table={
                "overflowX": "auto"
            },

            style_cell={
                "textAlign": "left",
                "padding": "8px",
                "minWidth": "100px"
            },

            style_header={
                "fontWeight": "bold"
            },

            page_size=10
        )
    ],

    style={
        "maxWidth": "1200px",
        "margin": "auto",
        "padding": "25px",
        "fontFamily": "Arial"
    }
)


# ==========================================
# 6. REUSABLE FILTERING FUNCTION
# ==========================================

def filter_data(borough, year, search):

    filtered = df.copy()

    # Filter by borough dropdown
    if borough != "ALL":
        filtered = filtered[
            filtered["borough"] == borough
        ]

    # Filter by year dropdown
    if year != "ALL":
        filtered = filtered[
            filtered["year"] == int(year)
        ]

    # Apply search
    if search:

        search = search.strip().lower()

        # Search for a borough
        for borough_name in df["borough"].dropna().unique():

            if borough_name.lower() in search:
                filtered = filtered[
                    filtered["borough"] == borough_name
                ]

        # Search for a year
        for year_value in df["year"].dropna().unique():

            if str(int(year_value)) in search:
                filtered = filtered[
                    filtered["year"] == int(year_value)
                ]

    return filtered


# ==========================================
# 7. EMPTY CHART FUNCTION
# ==========================================

def empty_chart(message):

    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font={"size": 16}
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ==========================================
# 8. GENERATE REPORT AND UPDATE CHARTS
# ==========================================

@app.callback(

    [
        Output("filter-summary", "children"),
        Output("data-table", "data"),
        Output("dob-trend-chart", "figure"),
        Output("sirta-trend-chart", "figure"),
        Output("relationship-chart", "figure")
    ],

    Input("generate-button", "n_clicks"),

    State("borough-dropdown", "value"),
    State("year-dropdown", "value"),
    State("search-input", "value")
)


def generate_report(n_clicks, borough, year, search):

    if n_clicks == 0:

        return (
            "Select your filters and click Generate Report.",
            [],
            empty_chart("Click Generate Report to display the chart."),
            empty_chart("Click Generate Report to display the chart."),
            empty_chart("Click Generate Report to display the chart.")
        )

    # Apply filters
    filtered = filter_data(borough, year, search)

    # Convert filtered data for the table
    table_data = filtered.to_dict("records")

    # If no data matches the filters
    if filtered.empty:

        message = "No records found for the selected filters."

        return (
            message,
            [],
            empty_chart("No data available for the selected filters."),
            empty_chart("No data available for the selected filters."),
            empty_chart("No data available for the selected filters.")
        )


    # ======================================
    # CHART 1: DOB VIOLATIONS OVER TIME
    # ======================================

    dob_fig = px.line(
        filtered.sort_values("year"),
        x="year",
        y="violation_records",
        color="borough",
        markers=True,
        title="DOB Safety Violations Over Time",
        labels={
            "year": "Year",
            "violation_records": "Number of Violation Records",
            "borough": "Borough"
        },
        hover_data={
            "unique_buildings": True
        }
    )

    dob_fig.update_layout(
        template="plotly_white",
        height=450,
        hovermode="x unified",
        legend_title="Borough"
    )


    # ======================================
    # CHART 2: SIRTA CRASH RECORDS OVER TIME
    # ======================================

    sirta_fig = px.line(
        filtered.sort_values("year"),
        x="year",
        y="crash_records",
        color="borough",
        markers=True,
        title="SIRTA Traffic Crash Records Over Time",
        labels={
            "year": "Year",
            "crash_records": "Number of Crash Records",
            "borough": "Borough"
        },
        hover_data={
            "severe_injuries": True,
            "fatalities": True
        }
    )

    sirta_fig.update_layout(
        template="plotly_white",
        height=450,
        hovermode="x unified",
        legend_title="Borough"
    )


    # ======================================
    # CHART 3: VIOLATIONS VS CRASH RECORDS
    # ======================================

    relationship_fig = px.scatter(
        filtered,
        x="violation_records",
        y="crash_records",
        color="borough",
        hover_name="borough",
        hover_data={
            "year": True,
            "unique_buildings": True,
            "severe_injuries": True,
            "fatalities": True
        },
        title="Building Safety Violations vs. Traffic Crashes",
        labels={
            "violation_records": "DOB Violation Records",
            "crash_records": "SIRTA Crash Records",
            "borough": "Borough"
        }
    )

    # Calculate correlation for the currently filtered data
    correlation = filtered[
        ["violation_records", "crash_records"]
    ].corr().iloc[0, 1]

    if pd.notna(correlation):

        correlation_text = (
            f"Pearson correlation (r) = {correlation:.3f}"
        )

    else:

        correlation_text = (
            "Correlation cannot be calculated for this selection."
        )

    relationship_fig.add_annotation(
        text=correlation_text,
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        bgcolor="white"
    )

    relationship_fig.update_layout(
        template="plotly_white",
        height=500,
        legend_title="Borough"
    )


    # ======================================
    # 9. REPORT SUMMARY
    # ======================================

    summary = (
        f"Report generated successfully! "
        f"Showing {len(filtered)} borough-year records."
    )

    return (
        summary,
        table_data,
        dob_fig,
        sirta_fig,
        relationship_fig
    )


# ==========================================
# 10. RUN THE WEBSITE
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
