# NYC Safety & Traffic Insights

Data Engineering and Visualization — Milestone 1 (German International University, Winter 2026)

| | Link |
|---|---|
| Live website | https://data-engineering-project1.onrender.com |
| GitHub repository | https://github.com/MahaGad/Data-Engineering-Project1 |
| Notebook (Colab) | https://colab.research.google.com/drive/1A0Q5EmYWnGzYNXPEZNvVwqi2dWEivvB8?usp=sharing |
| Notebook (in this repo) | [`Data_Engineering_M1.ipynb`](Data_Engineering_M1.ipynb) |
| AI prompt log | [`AI_prompts.md`](AI_prompts.md) |

## Project Overview

This project investigates the relationship between **building safety violations** and **serious traffic incidents** across New York City.

**Main research question:** Do boroughs with more building safety violations also experience more serious traffic injury incidents?

Two NYC Open Data datasets were integrated:

1. **DOB Safety Violations — Housing & Development**
2. **SIRTA Data — Transportation**

The datasets were combined using **borough** and **year** as common attributes. The final integrated dataset contains aggregated information for the five NYC boroughs from **2022 to 2025**.

## Datasets

| Domain | Dataset | NYC Open Data ID | Link |
|---|---|---|---|
| Housing & Development | DOB Safety Violations | `855j-jady` | https://data.cityofnewyork.us/d/855j-jady |
| Transportation | SIRTA Data | `xeqp-qz8h` | https://data.cityofnewyork.us/d/xeqp-qz8h |

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

The full step-by-step work (EDA, pre-integration cleaning, integration, post-integration cleaning) is in the notebook.

The final dataset (`integrated.csv`) contains **20 rows**, representing:

- 5 boroughs
- 4 years (2022–2025)

## Integrated Dataset

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

The website adds two derived measures when it loads the file: `total_injuries` (non-severe + severe injuries) and `violations_per_building` (violation records ÷ unique buildings).

## Research Questions & Visualizations

The project contains **10 research questions and 10 visualizations**, all shown on the website. RQ7–RQ10 directly connect the two datasets.

| # | Research question | Chart |
|---|---|---|
| RQ1 | How did building violation records change from 2022 to 2025 across the five boroughs? | Line chart |
| RQ2 | How did the number of unique buildings represented in the safety data change across boroughs from 2022 to 2025? | Line chart |
| RQ3 | Which boroughs had the highest numbers of crash records in each year? | Line chart |
| RQ4 | How do severe injuries compare across NYC boroughs and years? | Grouped bar chart |
| RQ5 | How do non-severe injuries vary between boroughs and years? | Grouped bar chart |
| RQ6 | Which boroughs recorded the highest numbers of fatalities across the four-year period? | Grouped bar chart |
| RQ7 | Is there a relationship between building violation records and crash records at the borough-year level? | Scatter plot |
| RQ8 | Is there a relationship between the number of unique buildings and crash records? | Scatter plot |
| RQ9 | Do borough-year observations with higher violation intensity per building also show higher fatalities? | Scatter plot |
| RQ10 | How does the total injury burden compare with building violation records across borough-year observations? | Scatter plot |

## Interactive Website

The project includes an interactive **Dash/Plotly** website called **NYC Safety & Traffic Insights** (`app.py`).

The website allows users to:

- Filter by **borough** (dropdown) and **year** (dropdown)
- Use **search mode** — type a query such as `Brooklyn 2023` or `Staten Island 2025` and the matching borough/year filters are applied
- Click **Generate Report** to update the data table and **all 10 charts** with the selected filters/search
- Hover over, zoom into and filter the interactive Plotly charts
- Read the project story: research question, data, main findings, limitations and potential impact on NYC

When the page first opens it shows the full dataset and all charts. The filters are applied when **Generate Report** is clicked. If a combination of filters matches no data (for example, the dropdown says Queens but the search says Brooklyn), the page shows a message instead of an error.

Because the data is aggregated at the borough-year level, the analysis identifies relationships and patterns but does **not** establish causation.

## How to Run the Project Locally

You need Python 3.10 or newer.

```bash
# 1. Get the code
git clone https://github.com/MahaGad/Data-Engineering-Project1.git
cd Data-Engineering-Project1

# 2. (Recommended) create a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Start the website
python app.py
```

Then open **http://127.0.0.1:8050** in your browser.

To re-run the analysis, open `Data_Engineering_M1.ipynb` in Google Colab or Jupyter. It downloads both datasets from NYC Open Data and recreates `integrated.csv`.

## Deployment (Render)

The website is deployed as a free **Render** web service.

1. Push this repository to GitHub (it must contain `app.py`, `integrated.csv` and `requirements.txt`).
2. Sign in to [Render](https://render.com) with GitHub.
3. Click **New → Web Service** and select this repository.
4. Use these settings:

   | Setting | Value |
   |---|---|
   | Language / Runtime | Python 3 |
   | Branch | `main` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn app:server` |
   | Instance Type | Free |

5. Click **Create Web Service** and wait for the first deploy to finish. Render gives the site a public `https://….onrender.com` address.

Alternatively, **New → Blueprint** reads the included `render.yaml`, which contains the same settings.

Notes: `app.py` exposes `server = app.server`, which is what `gunicorn app:server` runs. Render's free instances go to sleep after about 15 minutes without visitors, so the first page load after a pause can take around a minute.

## Project Structure

```text
.
├── app.py                      # Dash/Plotly website
├── integrated.csv              # Final integrated dataset (borough x year)
├── Data_Engineering_M1.ipynb   # EDA, cleaning, integration, analysis
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment settings
├── AI_prompts.md               # Prompts used during the project
├── README.md
└── .gitignore
```

## Technologies Used

- Python
- Pandas
- Plotly
- Dash
- Gunicorn / Render (deployment)
- Jupyter Notebook / Google Colab
- Git & GitHub

## Team

This project was completed as a group project with **5 team members**.

| Member | Name | Role | Contribution | Research questions & visualizations |
|---|---|---|---|---|
| 1 | [add name] | Data analysis & overall coordination | Dataset selection and integration plan; the Colab notebook (EDA, cleaning, integration, analysis); data-cleaning documentation; review of findings and limitations; coordinating the final integration | RQ1 and RQ2 |
| 2 | Maha Gad | Website structure & filters | Dash page layout; borough and year dropdowns; search mode; Generate Report callback; reusable filtering function; connecting the site to `integrated.csv` | RQ3 and RQ4 |
| 3 | [add name] | Interactive visualizations | Built the interactive Plotly charts for the website (pull request #1) with titles, labels and hover information; the charts update with the filters | RQ5 and RQ6 |
| 4 | Sarah Ibrahim El Dahaby | Research questions, findings & story section | Research questions; the story section (research question, findings, limitations, impact on NYC); correct interpretation of correlations without claiming causation | RQ7 and RQ8 |
| 5 | Omar | GitHub, testing, README & deployment | GitHub repository organization; README; `requirements.txt` and `render.yaml`; production fixes in `app.py` (`server` for gunicorn, debug off, charts visible on first load, message when no records match); `AI_prompts.md`; deployment to Render; testing of the dropdowns, search, Generate Report button and charts; collecting the final files | RQ9 and RQ10 |

## Limitations

The analysis is based on aggregated borough-level data from 2022–2025. Aggregation may hide differences between individual neighborhoods. Missing values and differences in reporting between the two datasets may also affect the analysis. The DOB violation counts also vary strongly between years, with a peak in 2023 (see the notebook), so year-to-year changes in violations should be read with care.

Most importantly, **correlation does not imply causation**.

## AI Usage

AI assistants were used during the project. The prompts are listed in [`AI_prompts.md`](AI_prompts.md) and in the last section of the notebook.
