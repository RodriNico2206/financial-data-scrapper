# CEDEAR Valuation Pipeline
The CEDEAR Valuation Pipeline is a Python-based system designed to fetch, process, and analyze financial data related to CEDEARs (Certificado de Depósito Argentino), providing valuation insights and exporting reports in Excel format. This project utilizes various data sources, including COMAFI, FRED, and market financials, to calculate intrinsic values and margins of safety for specified tickers and sectors.

## Key Features
* Fetches CEDEAR data from COMAFI and processes ratios
* Retrieves FRED AAA yield for valuation calculations
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
│   │   ├── scrapers
│   │   │   ├── __init__.py
│   │   │   ├── comafi.py
│   │   │   ├── fred.py
│   │   │   └── market.py
│   └── template_config.json
└── uv.lock
```

## Module Functionality
The CEDEAR Valuation Pipeline is structured into several modules, each responsible for a specific aspect of the system:
* `config.py`: Handles configuration loading and management
* `exporters/excel.py`: Exports valuation results to Excel reports
* `models/valuation.py`: Calculates Graham intrinsic value and margin of safety
* `scrapers/comafi.py`, `scrapers/fred.py`, `scrapers/market.py`: Fetch data from COMAFI, FRED, and market financials, respectively
* `main.py`: Orchestrates the pipeline execution, from data fetching to report export and upload

## Prerequisites and Environment Setup
To run the CEDEAR Valuation Pipeline, ensure you have:
* Python 3.8 or later installed
* A compatible operating system (Windows, macOS, or Linux)
* The `uv` package manager installed (for environment management)
* The `rclone` command-line program installed (for Google Drive upload)

To set up the environment:
1. Install `uv` using the official installation instructions
2. Navigate to the project directory and run `uv sync` to synchronize the environment
3. Activate the environment using `uv shell`

### Configuration
The pipeline uses a JSON configuration file (`config.json`) to store settings, such as:
* `fred_api_key`: Your FRED API key
* `google_drive`: Google Drive configuration (optional)
	+ `enabled`: Whether to upload reports to Google Drive
	+ `remote_name`: The remote name for the Google Drive connection
	+ `folder_name`: The folder name for the uploaded reports
* `sectors`: A dictionary of sectors with corresponding tickers

Example `config.json`:
```json
{
    "fred_api_key": "YOUR_FRED_API_KEY",
    "google_drive": {
        "enabled": true,
        "remote_name": "gdrive",
        "folder_name": "CEDEAR_Reports"
    },
    "sectors": {
        "General": ["TICKER1", "TICKER2"]
    }
}
```

## Installation
To install the required dependencies, run:
```bash
uv sync
```
This will synchronize the environment and install the necessary packages.

## Usage Example
To execute the pipeline, run:
```bash
uv run python src/cedear_valuation/main.py --config config.json
```
Replace `config.json` with the path to your custom configuration file, if needed.

## Usage Restrictions
The pipeline assumes that the `rclone` command-line program is installed and configured for Google Drive upload. If you encounter issues with `rclone`, ensure it is properly installed and configured on your system.

## Workflow Diagram
```mermaid
graph LR
    A[Load Configuration] -->|Load config.json| B[Fetch COMAFI Data]
    B -->|Process CEDEAR Ratios| C[Fetch FRED AAA Yield]
    C -->|Calculate Intrinsic Value| D[Analyze Stock Financials]
    D -->|Calculate Margin of Safety| E[Export Valuation Results]
    E -->|Upload to Google Drive (if enabled)| F[Finish Pipeline Execution]
```
Note: This diagram illustrates the main workflow of the CEDEAR Valuation Pipeline, from loading configuration to finishing pipeline execution.