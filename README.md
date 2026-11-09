# NYC Safety & Traffic Insights

## Project Overview

This project investigates the relationship between **building safety violations** and **serious traffic incidents** across New York City.

Two NYC datasets were integrated:

1. **DOB Safety Violations — Housing & Development**
2. **SIRTA Data — Transportation**

The datasets were combined using **borough** and **year** as common attributes. The final integrated dataset contains aggregated information for the five NYC boroughs from **2022 to 2025**.

## Datasets

### 1. DOB Safety Violations

The DOB Safety Violations dataset contains records of building safety violations in New York City.

The original dataset used for the project covers **2022–2025** and contains:

- 519,337 records
- 24 columns
- Borough information
- Violation issue dates
- Violation types and statuses
- Building and geographic information

### 2. SIRTA Data

The SIRTA dataset contains records of serious traffic incidents in New York City.

The project uses traffic crash information including:

- Crash date and time
- Borough
- Non-severe injuries
- Severe injuries
- Fatalities
- Geographic information

## Data Processing

The data processing pipeline included:

1. Loading the original datasets.
2. Exploring their structure, data types, missing values and duplicates.
3. Cleaning and standardizing relevant fields.
4. Extracting the year from date information.
5. Aggregating both datasets by **borough and year**.
6. Integrating the two datasets using **borough + year**.
7. Checking the integrated dataset for missing values and expected borough-year combinations.
8. Creating derived measures for analysis.

The final dataset contains **20 rows**, representing:

- 5 boroughs
- 4 years (2022–2025)

## Integrated Dataset

The final dataset contains the following columns:

| Column | Description |
|---|---|
| `borough` | NYC borough |
| `year` | Year of the records |
| `violation_records` | Number of building safety violation records |
| `unique_buildings` | Number of unique buildings represented |
| `crash_records` | Number of traffic crash records |
| `non_severe_injuries` | Number of non-severe injuries |
| `severe_injuries` | Number of severe injuries |
| `fatalities` | Number of fatalities |

## Research Questions & Visualizations

The project contains **10 research questions and 10 visualizations**.

The visualizations investigate patterns and relationships between building safety measures and transportation safety measures across NYC boroughs and years.

The analysis uses multiple visualization types, including:

- Line charts
- Bar charts
- Scatter plots
- Other comparative visualizations

The visualizations are implemented using **Plotly** and displayed through the interactive website.

## Interactive Website

The project includes an interactive **Dash/Plotly** website called:

**NYC Safety & Traffic Insights**

The website allows users to:

- Select a borough
- Select a year
- Search the integrated data
- Generate a filtered report
- View the filtered dataset
- Explore the project visualizations
- Read the project story, findings and limitations

## Project Story

The website explains:

- The research objective
- The two datasets
- The integration process
- Main findings
- Limitations
- Potential impact on NYC

Because the data is aggregated at the borough-year level, the analysis identifies relationships and patterns but does **not** establish causation.

## Project Structure

```text
project/
│
├── app.py
├── integrated.csv
├── Data Engineering M1.ipynb
├── README.md
└── other required project files
```

## Technologies Used

- Python
- Pandas
- Plotly
- Dash
- Jupyter Notebook / Google Colab
- Git & GitHub

## Team

This project was completed as a group project with **5 team members**.

Each member contributed research questions, visualizations, data processing and/or website components according to the project requirements.

## Limitations

The analysis is based on aggregated borough-level data from 2022–2025. Aggregation may hide differences between individual neighborhoods. Missing values and differences in reporting between the two datasets may also affect the analysis.

Most importantly, **correlation does not imply causation**.

## Repository

GitHub Repository: **[Add GitHub repository link]**

## Deployment

Deployed Website: **[Add deployment link]**
