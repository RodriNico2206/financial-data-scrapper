# CEDEAR Valuation Pipeline
The CEDEAR Valuation Pipeline is a Python-based system designed to fetch and process financial data for CEDEAR valuation. It utilizes various scrapers to gather data from different sources, calculates the intrinsic value using the Graham formula, and exports the results to an Excel report.

## Key Features
* Fetches CEDEAR data from Comafi and financial data from the market
* Calculates the intrinsic value using the Graham formula
* Calculates the margin of safety
* Exports the results to an Excel report
* Optionally uploads the report to Google Drive using rclone

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
* `config.py`: Handles the loading of the configuration file
* `exporters/excel.py`: Exports the results to an Excel report
* `models/valuation.py`: Calculates the intrinsic value using the Graham formula and the margin of safety
* `scrapers/comafi.py`, `scrapers/fred.py`, `scrapers/market.py`: Fetch data from Comafi, FRED, and the market, respectively
* `main.py`: The main entry point of the pipeline, responsible for orchestrating the entire process

## Prerequisites and Environment Setup
To run the CEDEAR Valuation Pipeline, you need:
* Python 3.8 or later
* pip
* A compatible operating system (Windows, Linux, or macOS)
* rclone (for uploading reports to Google Drive)

To set up the environment:
1. Create a virtual environment using `poetry` by running `poetry install` in the project root directory.
2. Activate the virtual environment using `poetry shell`.

### Configuration
The pipeline uses a JSON configuration file (`config.json`) to store settings such as the FRED API key, Google Drive remote name, and folder path. You can customize these settings by editing the `config.json` file. The configuration file should have the following structure:
```json
{
  "fred_api_key": "YOUR_FRED_API_KEY",
  "google_drive": {
    "enabled": true,
    "remote_name": "your_remote_name",
    "folder_name": "your_folder_path"
  },
  "sectors": {
    "sector_name": ["ticker1", "ticker2"]
  }
}
```
Replace the placeholder values with your actual settings.

## Installation
To install the required dependencies, run:
```bash
poetry install
```
This will install all the necessary packages, including `pandas`, `rclone`, and `argparse`.

## Usage Example
To run the pipeline, execute the following command:
```bash
poetry run python src/cedear_valuation/main.py --config config.json
```
This will start the pipeline, fetch the data, calculate the intrinsic values, and export the results to an Excel report. If you have configured Google Drive upload, the report will be uploaded to your specified remote folder.

## Usage Restrictions
The pipeline assumes that you have the necessary dependencies installed and configured. Additionally, the pipeline uses the `rclone` command to upload reports to Google Drive, so you need to have `rclone` installed and configured on your system.

## Workflow Diagram
```mermaid
graph LR
    A[Start] -->|Load Config| B[Load Configuration]
    B -->|Fetch Comafi Data| C[Fetch Comafi Data]
    C -->|Process Comafi Data| D[Process Comafi Data]
    D -->|Fetch FRED Data| E[Fetch FRED Data]
    E -->|Calculate Intrinsic Value| F[Calculate Intrinsic Value]
    F -->|Calculate Margin of Safety| G[Calculate Margin of Safety]
    G -->|Export to Excel| H[Export to Excel]
    H -->|Upload to Google Drive| I[Upload to Google Drive]
    I -->|Finish| J[Finish]
```
Note: This diagram illustrates the main workflow of the pipeline, but it may not include all the details and conditional logic.