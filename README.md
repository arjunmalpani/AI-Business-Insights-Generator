# AI Business Insights Generator

An AI-powered analytics workflow that transforms raw sales data into a cleaned dataset, KPI-driven insights, visualizations, and an executive-ready HTML report using Gemini.

## Project Description

This project showcases a complete business intelligence pipeline in Python. It starts with a raw sales CSV file, cleans and validates the data, stores it in SQLite for analysis, computes business KPIs, generates charts, and then uses an AI model to produce actionable business insights and recommendations.

The result is a polished report that can be shared with stakeholders who need a clear summary of performance without having to inspect the raw data directly.

## Features

- Automated CSV data loading and validation
- Data cleaning for duplicates, missing values, whitespace, and date normalization
- SQLite storage for structured analysis and auditing
- KPI generation for sales, profit, margin, orders, customers, and more
- Business segmentation analysis by category, region, segment, and product
- Chart generation for trends and performance breakdowns
- AI-generated executive summaries, insights, risks, and recommendations
- HTML report generation for presentation and sharing

## Tech Stack

- Python 3.10+
- pandas for data processing
- matplotlib for chart generation
- SQLite for local data storage
- google-genai for Gemini-powered insights
- python-dotenv for environment configuration
- Jinja2 for HTML report templating

## Architecture

The project follows a simple modular pipeline:

1. Data ingestion with [src/data_loader.py](src/data_loader.py)
2. Data cleaning and validation with [src/cleaner.py](src/cleaner.py)
3. SQLite persistence with [src/database.py](src/database.py)
4. KPI and aggregation logic with [src/analyzer.py](src/analyzer.py)
5. Visualization generation with [src/visulization.py](src/visulization.py)
6. AI insight generation with [src/ai_insights.py](src/ai_insights.py)
7. Report rendering with [src/report_generator.py](src/report_generator.py)

## Folder Structure

```text
AI-Business-Insights-Generator/
├── charts/                  # Generated charts
├── data/
│   ├── processed/           # Cleaned CSV output
│   └── raw/                 # Source sales CSV
├── notebooks/               # Exploratory analysis notebook
├── reports/                 # Generated HTML and AI report outputs
├── src/                     # Core application modules
├── templates/               # HTML report template
├── demo.py                  # Simple demo entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd AI-Business-Insights-Generator
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the main analysis pipeline:

```bash
python src/main.py
```

This will:

- load the raw sales data
- clean and store it
- generate KPIs and charts
- create AI-driven insights
- write the final HTML report to [reports/report.html](reports/report.html)

## Project Workflow

The workflow is organized as follows:

1. Load the source CSV from [data/raw/sales.csv](data/raw/sales.csv)
2. Clean and standardize the dataset
3. Save the cleaned version to [data/processed/cleaned_sales.csv](data/processed/cleaned_sales.csv)
4. Persist data into a local SQLite database
5. Calculate metrics and produce charts
6. Send the KPI summary to Gemini for analysis
7. Generate the final executive report

## Screenshots and Outputs

Generated outputs are stored in the following locations:

- Charts: [charts](charts)
- HTML report: [reports/report.html](reports/report.html)
- Cleaned dataset: [data/processed/cleaned_sales.csv](data/processed/cleaned_sales.csv)

You can open the HTML report in a browser to review the generated executive summary and charts.

## Future Improvements

Potential enhancements for the project include:

- Add a command-line interface for configurable inputs
- Support multiple file formats beyond CSV
- Add dashboard-style interactivity with Streamlit or Dash
- Introduce automated testing for the cleaning and analytics pipeline
- Expand AI prompts for deeper forecasting and anomaly detection
- Add deployment support for web-based reporting

## Author

This project is intended as a practical example of combining Python, data analytics, and AI-generated reporting for business intelligence.
