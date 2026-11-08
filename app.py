
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table


# =========================================================
# 1. LOAD THE INTEGRATED DATASET
# =========================================================

df = pd.read_csv("integrated.csv")

# Standardize data types
df["year"] = pd.to_numeric(df["year"], errors="coerce")

numeric_columns = [
    "violation_records",
    "unique_buildings",
    "crash_records",
    "non_severe_injuries",
    "severe_injuries",
    "fatalities"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["borough"] = df["borough"].astype(str).str.upper().str.strip()

df = df.dropna(
    subset=[
        "borough",
        "year",
        "violation_records",
        "crash_records"
    ]
)

df["year"] = df["year"].astype(int)

# Check that each borough-year combination is unique
if df.duplicated(subset=["borough", "year"]).any():
    raise ValueError(
        "The integrated dataset contains duplicate borough-year rows."
    )

# Required columns
required_columns = [
    "borough",
    "year",
    "violation_records",
    "unique_buildings",
    "crash_records",
    "non_severe_injuries",
    "severe_injuries",
    "fatalities"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns in integrated.csv: {missing_columns}"
    )


# =========================================================
# 2. CREATE THE DASH APP
# =========================================================

app = Dash(__name__)

app.title = "NYC Safety & Traffic Insights"


# =========================================================
# 3. REUSABLE STYLING
# =========================================================

PAGE_STYLE = {
    "maxWidth": "1250px",
    "margin": "auto",
    "padding": "25px",
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "#F8FAFC",
    "color": "#1E293B"
}

SECTION_STYLE = {
    "backgroundColor": "white",
    "padding": "20px",
    "marginBottom": "25px",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
}

CHART_STYLE = {
    "width": "100%"
}


# =========================================================
# 4. WEBSITE LAYOUT
# =========================================================

app.layout = html.Div(

    [

        # Website heading
        html.H1(
            "NYC Safety & Traffic Insights",
            style={
                "textAlign": "center",
                "color": "#17365D",
                "fontSize": "34px"
            }
        ),

        html.P(
            "Explore the relationship between building safety "
            "violations and serious traffic incidents across "
            "New York City boroughs.",
            style={
                "textAlign": "center",
                "fontSize": "17px"
            }
        ),

        html.Hr(),

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        html.Div(

            [

                html.H2("Explore the Data"),

                html.Label("Select a borough:"),

                dcc.Dropdown(
                    id="borough-dropdown",

                    options=[
                        {
                            "label": "All Boroughs",
                            "value": "ALL"
                        }
                    ] + [
                        {
                            "label": borough,
                            "value": borough
                        }
                        for borough in sorted(
                            df["borough"].unique()
                        )
                    ],

                    value="ALL",
                    clearable=False
                ),

                html.Br(),

                html.Label("Select a year:"),

                dcc.Dropdown(
                    id="year-dropdown",

                    options=[
                        {
                            "label": "All Years",
                            "value": "ALL"
                        }
                    ] + [
                        {
                            "label": str(year),
                            "value": int(year)
                        }
                        for year in sorted(
                            df["year"].unique()
                        )
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
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "boxSizing": "border-box"
                    }
                ),

                html.Br(),
                html.Br(),

                html.Button(
                    "Generate Report",
                    id="generate-button",
                    n_clicks=0,

                    style={
                        "padding": "12px 25px",
                        "backgroundColor": "#17365D",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                        "fontSize": "16px"
                    }
                ),

                html.Br(),
                html.Br(),

                html.Div(
                    id="filter-summary",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "18px",
                        "color": "#17365D"
                    }
                )

            ],

            style=SECTION_STYLE

        ),


        # =================================================
        # VISUALIZATION 1
        # =================================================

        html.Div(

            [

                html.H2("Data Visualizations"),

                html.H3(
                    "1. DOB Safety Violations Over Time"
                ),

                dcc.Graph(
                    id="dob-trend-chart",
                    style=CHART_STYLE
                ),

                html.P(
                    "This line chart compares annual building "
                    "safety violation records across NYC boroughs "
                    "from 2022 to 2025. It helps identify changes "
                    "and unusual increases in recorded violations."
                )

            ],

            style=SECTION_STYLE

        ),


        # =================================================
        # VISUALIZATION 2
        # =================================================

        html.Div(

            [

                html.H3(
                    "2. SIRTA Traffic Crash Records Over Time"
                ),

                dcc.Graph(
                    id="sirta-trend-chart",
                    style=CHART_STYLE
                ),

                html.P(
                    "This chart displays annual traffic crash "
                    "records across the five boroughs. Hover over "
                    "the points to explore severe injuries and "
                    "fatalities."
                )

            ],

            style=SECTION_STYLE

        ),


        # =================================================
        # VISUALIZATION 3 - RQ1
        # =================================================

        html.Div(

            [

                html.H3(
                    "3. Building Violations vs. Traffic Crashes"
                ),

                html.P(
                    "RQ1: Is the number of DOB safety violation "
                    "records associated with the number of SIRTA "
                    "traffic crash records across NYC boroughs "
                    "and years?"
                ),

                dcc.Graph(
                    id="relationship-chart",
                    style=CHART_STYLE
                ),

                html.P(
                    "The scatterplot examines the association "
                    "between building safety violation records "
                    "and traffic crash records. Each point "
                    "represents one borough-year combination."
                ),

                html.P(
                    "Limitation: A positive correlation does not "
                    "establish causation. Borough size, population, "
                    "building stock, and other factors may influence "
                    "both measurements. The analysis includes only "
                    "20 borough-year observations."
                )

            ],

            style=SECTION_STYLE

        ),


        # =================================================
        # VISUALIZATION 4 - RQ2
        # =================================================

        html.Div(

            [

                html.H3(
                    "4. Indexed Trends: DOB Violations vs. "
                    "SIRTA Crashes"
                ),

                html.P(
                    "RQ2: Do building safety violations and "
                    "traffic crash records show similar patterns "
                    "of change over time across NYC boroughs?"
                ),

                dcc.Graph(
                    id="indexed-trend-chart",
                    style=CHART_STYLE
                ),

                html.P(
                    "Both measurements are indexed to 2022 = 100. "
                    "Values above 100 indicate an increase compared "
                    "with 2022, while values below 100 indicate "
                    "a decrease."
                ),

                html.P(
                    "Limitation: This visualization compares "
                    "relative changes in recorded counts. It does "
                    "not measure actual safety levels or establish "
                    "a causal relationship between violations "
                    "and traffic crashes."
                )

            ],

            style=SECTION_STYLE

        ),


        # =================================================
        # DATA TABLE
        # =================================================

        html.Div(

            [

                html.H2("Filtered Integrated Dataset"),

                dash_table.DataTable(

                    id="data-table",

                    columns=[
                        {
                            "name": column,
                            "id": column
                        }
                        for column in df.columns
                    ],

                    data=[],

                    style_table={
                        "overflowX": "auto"
                    },

                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "minWidth": "110px",
                        "fontFamily": "Arial"
                    },

                    style_header={
                        "fontWeight": "bold",
                        "backgroundColor": "#E2E8F0"
                    },

                    style_data={
                        "backgroundColor": "white"
                    },

                    page_size=10

                )

            ],

            style=SECTION_STYLE

        )

    ],

    style=PAGE_STYLE

)


# =========================================================
# 5. REUSABLE FILTERING FUNCTION
# =========================================================

def filter_data(borough, year, search):

    filtered = df.copy()

    # Apply borough dropdown
    if borough and borough != "ALL":

        filtered = filtered[
            filtered["borough"] == borough
        ]

    # Apply year dropdown
    if year and year != "ALL":

        filtered = filtered[
            filtered["year"] == int(year)
        ]

    # Apply search
    if search and search.strip():

        search_text = search.strip().upper()

        # Find borough names included in the search
        matching_boroughs = [
            name for name in df["borough"].unique()
            if name in search_text
        ]

        # Find years included in the search
        matching_years = re.findall(
            r"\b(?:2022|2023|2024|2025)\b",
            search_text
        )

        # If a borough is specified, filter by it
        if matching_boroughs:

            filtered = filtered[
                filtered["borough"].isin(matching_boroughs)
            ]

        # If a year is specified, filter by it
        if matching_years:

            filtered = filtered[
                filtered["year"].isin(
                    [int(value) for value in matching_years]
                )
            ]

        # Unrecognized search terms should not silently
        # return the unfiltered dataset
        if not matching_boroughs and not matching_years:

            filtered = filtered.iloc[0:0]

    return filtered


# =========================================================
# 6. EMPTY CHART FUNCTION
# =========================================================

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


# =========================================================
# 7. GENERATE REPORT CALLBACK
# =========================================================

@app.callback(

    [

        Output("filter-summary", "children"),

        Output("data-table", "data"),

        Output("dob-trend-chart", "figure"),

        Output("sirta-trend-chart", "figure"),

        Output("relationship-chart", "figure"),

        Output("indexed-trend-chart", "figure")

    ],

    Input("generate-button", "n_clicks"),

    State("borough-dropdown", "value"),

    State("year-dropdown", "value"),

    State("search-input", "value")

)


def generate_report(n_clicks, borough, year, search):

    # -----------------------------------------------------
    # INITIAL WEBSITE STATE
    # -----------------------------------------------------

    if n_clicks == 0:

        message = "Select your filters and click Generate Report."

        empty = empty_chart(
            "Click Generate Report to display the chart."
        )

        return (
            message,
            [],
            empty,
            empty,
            empty,
            empty
        )


    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered = filter_data(
        borough,
        year,
        search
    )

    table_data = filtered.to_dict("records")


    # -----------------------------------------------------
    # HANDLE EMPTY RESULTS
    # -----------------------------------------------------

    if filtered.empty:

        message = (
            "No records found for the selected filters."
        )

        empty = empty_chart(
            "No data available for the selected filters."
        )

        return (
            message,
            [],
            empty,
            empty,
            empty,
            empty
        )


    # =====================================================
    # CHART 1: DOB VIOLATIONS OVER TIME
    # =====================================================

    dob_fig = px.line(

        filtered.sort_values("year"),

        x="year",

        y="violation_records",

        color="borough",

        markers=True,

        title="DOB Safety Violations Over Time",

        labels={

            "year": "Year",

            "violation_records":
                "Number of Violation Records",

            "borough": "Borough"

        },

        hover_data={
            "unique_buildings": True
        }

    )

    dob_fig.update_layout(

        template="plotly_white",

        height=480,

        hovermode="x unified",

        legend_title="Borough",

        legend={
            "orientation": "h",
            "y": -0.25,
            "x": 0.5,
            "xanchor": "center"
        },

        margin={
            "l": 75,
            "r": 30,
            "t": 80,
            "b": 110
        }

    )

    dob_fig.update_xaxes(

        tickmode="linear",

        tick0=2022,

        dtick=1,

        tickformat="d"

    )


    # =====================================================
    # CHART 2: SIRTA CRASH RECORDS OVER TIME
    # =====================================================

    sirta_fig = px.line(

        filtered.sort_values("year"),

        x="year",

        y="crash_records",

        color="borough",

        markers=True,

        title="SIRTA Traffic Crash Records Over Time",

        labels={

            "year": "Year",

            "crash_records":
                "Number of Crash Records",

            "borough": "Borough"

        },

        hover_data={

            "severe_injuries": True,

            "fatalities": True

        }

    )

    sirta_fig.update_layout(

        template="plotly_white",

        height=480,

        hovermode="x unified",

        legend_title="Borough",

        legend={
            "orientation": "h",
            "y": -0.25,
            "x": 0.5,
            "xanchor": "center"
        },

        margin={
            "l": 75,
            "r": 30,
            "t": 80,
            "b": 110
        }

    )

    sirta_fig.update_xaxes(

        tickmode="linear",

        tick0=2022,

        dtick=1,

        tickformat="d"

    )


    # =====================================================
    # CHART 3: VIOLATIONS VS. CRASH RECORDS - RQ1
    # =====================================================

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

        title=(
            "Building Safety Violations vs. Traffic Crashes"
        ),

        labels={

            "violation_records":
                "DOB Violation Records",

            "crash_records":
                "SIRTA Crash Records",

            "borough": "Borough"

        }

    )

    # Correlation for the currently filtered observations
    correlation = filtered[
        [
            "violation_records",
            "crash_records"
        ]
    ].corr().iloc[0, 1]

    if pd.notna(correlation):

        correlation_text = (
            f"Pearson correlation (r) = {correlation:.3f}"
        )

    else:

        correlation_text = (
            "Correlation cannot be calculated "
            "for this selection."
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

        legend_title="Borough",

        legend={
            "orientation": "h",
            "y": -0.2,
            "x": 0.5,
            "xanchor": "center"
        },

        margin={
            "l": 85,
            "r": 30,
            "t": 80,
            "b": 110
        }

    )


    # =====================================================
    # CHART 4: INDEXED TRENDS - RQ2
    # =====================================================

    # Use the filtered boroughs
    selected_boroughs = filtered["borough"].unique()

    # Retrieve the 2022 baseline for these boroughs
    baseline_data = df[

        (df["borough"].isin(selected_boroughs))

        &

        (df["year"] == 2022)

    ].copy()

    # Include the baseline even if the user selected
    # a later year from the year dropdown
    index_data = pd.concat(

        [
            filtered,
            baseline_data
        ],

        ignore_index=True

    )

    # Remove repeated borough-year rows
    index_data = index_data.drop_duplicates(

        subset=["borough", "year"]

    )

    # Sort observations so the baseline is first
    index_data = index_data.sort_values(

        ["borough", "year"]

    )

    # Calculate DOB index
    index_data["dob_index"] = (

        index_data.groupby("borough")["violation_records"]

        .transform(

            lambda values:

            values / values.iloc[0] * 100

        )

    )

    # Calculate SIRTA index
    index_data["sirta_index"] = (

        index_data.groupby("borough")["crash_records"]

        .transform(

            lambda values:

            values / values.iloc[0] * 100

        )

    )

    # Convert the data into long format for Plotly
    index_long = index_data.melt(

        id_vars=[
            "borough",
            "year"
        ],

        value_vars=[
            "dob_index",
            "sirta_index"
        ],

        var_name="dataset",

        value_name="index_value"

    )

    index_long["dataset"] = index_long["dataset"].replace({

        "dob_index": "DOB Violation Index",

        "sirta_index": "SIRTA Crash Index"

    })

    # Create indexed comparison chart
    indexed_fig = px.line(

        index_long,

        x="year",

        y="index_value",

        color="borough",

        line_dash="dataset",

        markers=True,

        title=(
            "Indexed Changes in DOB Violations "
            "and SIRTA Traffic Crashes"
        ),

        labels={

            "year": "Year",

            "index_value": "Index (2022 = 100)",

            "borough": "Borough",

            "dataset": "Measure"

        },

        hover_data={

            "dataset": True,

            "index_value": ":.2f"

        }

    )

    # Add horizontal reference line at 100
    indexed_fig.add_hline(

        y=100,

        line_dash="dash",

        annotation_text="2022 baseline = 100"

    )

    indexed_fig.update_layout(

        template="plotly_white",

        height=600,

        hovermode="x unified",

        legend_title="Borough / Measure",

        margin={
            "l": 85,
            "r": 40,
            "t": 90,
            "b": 100
        }

    )

    indexed_fig.update_xaxes(

        tickmode="linear",

        tick0=2022,

        dtick=1,

        tickformat="d"

    )


    # =====================================================
    # REPORT SUMMARY
    # =====================================================

    summary = (

        f"Report generated successfully! "

        f"Showing {len(filtered)} borough-year records."

    )

    return (

        summary,

        table_data,

        dob_fig,

        sirta_fig,

        relationship_fig,

        indexed_fig

    )


# =========================================================
# 8. RUN THE WEBSITE
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
