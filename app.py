import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table

# Load the integrated dataset
df = pd.read_csv("integrated.csv")

# Create the Dash app
app = Dash(__name__)
app.title = "NYC Safety & Traffic Insights"


# Website layout
app.layout = html.Div(
    [
        html.H1("NYC Safety & Traffic Insights"),

        html.P(
            "Explore the relationship between building safety "
            "violations and serious traffic incidents across "
            "New York City boroughs."
        ),

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
                {"label": str(year), "value": year}
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
            style={"width": "100%"}
        ),

        html.Br(),
        html.Br(),

        # Generate Report button
        html.Button(
            "Generate Report",
            id="generate-button",
            n_clicks=0
        ),

        html.Br(),
        html.Br(),

        # Summary
        html.Div(id="filter-summary"),

        html.Br(),

        # Filtered data table
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
                "padding": "8px"
            },
                    page_size=10
        ),

        # MEMBER 4 - PROJECT STORY SECTION

        # ==================================
        # MEMBER 4 - PROJECT STORY SECTION
        # ==================================

        html.Hr(),

        html.H2(
            "The Story Behind NYC's Safety Data",
            style={"textAlign": "center"}
        ),

        html.P(
            "Understanding the relationship between building "
            "safety violations and traffic incidents across "
            "New York City's five boroughs."
        ),

        html.H3("1. Our Research"),

        html.P(
            "Our project investigates the relationship between "
            "DOB building safety violations and SIRTA traffic "
            "crashes and injuries across NYC boroughs."
        ),

        html.H3("2. The Data"),

        html.P(
            "We combined the DOB and SIRTA datasets using "
            "borough and year to investigate patterns in "
            "building safety and transportation safety."
        ),

        html.H3("3. Main Findings"),

        html.P(
            "Our analysis examines the relationships between "
            "building violations, traffic crashes and injuries. "
            "The charts above present the results of these comparisons."
        ),

        html.P(
            "Final findings and correlation values should be "
            "added here after reviewing the completed analysis."
        ),

        html.H3("4. Limitations"),

        html.P(
            "The analysis uses aggregated borough-level data, "
            "which may hide differences between individual "
            "neighborhoods. Missing values, repeated records "
            "and unusual reporting patterns may also affect "
            "the results. Correlation does not imply causation."
        ),

        html.H3("5. Potential Impact on NYC"),

        html.P(
            "The findings could help city planners, building "
            "safety authorities and transportation agencies "
            "identify areas that deserve further investigation "
            "and support better-informed urban safety planning."
        )

    ]
)


# Reusable filtering function
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

# Generate Report callback
@app.callback(
    [
        Output("filter-summary", "children"),
        Output("data-table", "data")
    ],
    Input("generate-button", "n_clicks"),
    State("borough-dropdown", "value"),
    State("year-dropdown", "value"),
    State("search-input", "value")
)
def generate_report(n_clicks, borough, year, search):

    if n_clicks == 0:
        return "", []

    filtered = filter_data(borough, year, search)

    # Convert filtered data to a format Dash can display
    table_data = filtered.to_dict("records")

    return (
        f"Report generated! Showing {len(filtered)} records.",
        table_data
    )


# Run the website
if __name__ == "__main__":
    app.run(debug=True) 
