# CEDEAR Valuation Pipeline
The CEDEAR Valuation Pipeline is a Python-based system designed to fetch and process financial data for CEDEAR (Certificado de Depósito Argentino) valuation. It utilizes various data sources, including COMAFI, FRED, and stock market financials, to calculate intrinsic values and margins of safety for specified tickers and sectors.

## Key Features
* Fetches COMAFI CEDEAR data and processes ratios
* Retrieves FRED AAA yield for intrinsic value calculation
* Analyzes stock financials for specified tickers and sectors
* Calculates Graham intrinsic value and margin of safety
* Exports valuation results to Excel reports
* Optionally uploads reports to Google Drive using rclone

## Directory Hierarchy
```bash
.
├── .gitignore
├── README.md
├── pyproject.toml
├── src
│   ├── cedear_valuation
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exporters
│   │   │   ├── __init__.py
│   │   │   └── excel.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── valuation.py
│   │   └── scrapers
│   │       ├── __init__.py
│   │       ├── comafi.py
│   │       ├── fred.py
│   │       └── market.py
├── template_config.json
└── uv.lock
```

## Module Functionality
The CEDEAR Valuation Pipeline consists of several modules:
* `config.py`: Handles configuration loading from a JSON file.
* `exporters/excel.py`: Exports data to Excel reports.
* `models/valuation.py`: Calculates intrinsic values and margins of safety.
* `scrapers/comafi.py`, `scrapers/fred.py`, `scrapers/market.py`: Fetch data from COMAFI, FRED, and stock market sources, respectively.
* `main.py`: Orchestrates the pipeline execution, from data fetching to report generation and upload.

## Prerequisites and Environment Setup
To run the CEDEAR Valuation Pipeline, ensure you have:
* Python 3.8 or later installed
* A compatible operating system (Windows, macOS, or Linux)
* The `uv` package manager installed (due to the presence of `uv.lock`)

Create and activate a virtual environment using `uv`:
```bash
uv sync
uv run python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```
### Configuration
The pipeline uses a JSON configuration file (`config.json` by default). The configuration file should contain the following parameters:
* `fred_api_key`: Your FRED API key
* `google_drive` (optional): Google Drive configuration
	+ `enabled`: Whether to upload reports to Google Drive (boolean)
	+ `remote_name`: The remote name for rclone (string, default: "gdrive")
	+ `folder_name`: The folder name for uploaded reports (string, default: "CEDEAR_Reports")
* `sectors` (optional): A dictionary of sectors with tickers (e.g., `{"General": ["AAPL", "GOOG"]}`)

## Installation
To install the required dependencies, run:
```bash
uv sync
```
This will synchronize the environment using the `uv.lock` file.

## Usage Example
To execute the pipeline, run:
```bash
uv run python src/cedear_valuation/main.py
```
You can optionally specify a custom configuration file using the `--config` argument:
```bash
uv run python src/cedear_valuation/main.py --config path/to/custom_config.json
```

## Usage Restrictions
The pipeline assumes you have the necessary dependencies installed, including `rclone` for Google Drive uploads. Ensure you have the required API keys and configuration settings in place.

## Workflow Diagram
```mermaid
graph LR
    A[Load Configuration] -->|Load config.json| B[Fetch COMAFI Data]
    B -->|Process COMAFI ratios| C[Fetch FRED AAA Yield]
    C -->|Calculate intrinsic value| D[Analyze Stock Financials]
    D -->|Calculate margin of safety| E[Export to Excel]
    E -->|Upload to Google Drive (if enabled)| F[Finish Pipeline]
```
Note: This diagram illustrates the main workflow of the CEDEAR Valuation Pipeline.