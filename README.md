# CEDEAR Valuation System
The CEDEAR Valuation System is a Python-based application designed to fetch and analyze financial data for CEDEARs (Certificado de Depósito Argentino), providing valuation metrics such as intrinsic value and margin of safety. This system utilizes various data sources, including COMAFI, FRED, and market financials, to generate comprehensive reports.

## Key Features
* Fetches CEDEAR data from COMAFI and processes ratios
* Retrieves AAA yield from FRED for intrinsic value calculation
* Analyzes stock financials for tickers and sectors
* Calculates Graham intrinsic value and margin of safety
* Exports reports to Excel and optionally uploads to Google Drive

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
The CEDEAR Valuation System consists of several modules, each responsible for a specific function:
* `config.py`: Loads configuration from a JSON file
* `exporters/excel.py`: Exports data to Excel
* `models/valuation.py`: Calculates intrinsic value and margin of safety
* `scrapers/comafi.py`, `scrapers/fred.py`, `scrapers/market.py`: Fetch data from COMAFI, FRED, and market sources
* `main.py`: Orchestrates the entire valuation pipeline

## Prerequisites and Environment Setup
To run the CEDEAR Valuation System, you will need:
* Python 3.8 or later
* `uv` package manager (due to the presence of `uv.lock`)
* `rclone` installed on the system (for Google Drive uploads)

To set up the environment:
1. Install `uv` using the official installation instructions.
2. Run `uv sync` to synchronize the environment.
3. Create a `config.json` file based on the `template_config.json` template, filling in the required parameters (e.g., FRED API key, Google Drive configuration).

### Configuration
The system uses a `config.json` file for configuration. The following parameters are required:
* `fred_api_key`: FRED API key
* `google_drive`: Google Drive configuration (optional)
	+ `enabled`: Whether to upload reports to Google Drive
	+ `remote_name`: Remote name for Google Drive (default: `gdrive`)
	+ `folder_name`: Folder name for reports on Google Drive (default: `CEDEAR_Reports`)

## Installation
To install the CEDEAR Valuation System:
1. Run `uv sync` to synchronize the environment.
2. Ensure `rclone` is installed on the system.

## Usage Example
To run the CEDEAR Valuation System:
```bash
uv run python src/cedear_valuation/main.py
```
This will execute the valuation pipeline, fetching data, calculating metrics, and exporting reports to Excel. If Google Drive upload is enabled, the report will be uploaded to the specified folder.

## Usage Restrictions
The system requires a valid FRED API key and may be subject to rate limits. Additionally, Google Drive uploads require `rclone` to be installed and configured.

## Workflow Diagram
```mermaid
graph LR
    A[Load Configuration] -->|Load config.json| B[Fetch COMAFI Data]
    B -->|Process CEDEAR Ratios| C[Fetch FRED AAA Yield]
    C -->|Calculate Intrinsic Value| D[Analyze Stock Financials]
    D -->|Calculate Margin of Safety| E[Export Report to Excel]
    E -->|Upload to Google Drive (if enabled)| F[Finish Pipeline]
```
Note: This diagram illustrates the main workflow of the CEDEAR Valuation System.