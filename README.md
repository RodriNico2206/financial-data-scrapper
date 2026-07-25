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
The CEDEAR Valuation Pipeline consists of several modules:
* `config.py`: Handles configuration loading from JSON files.
* `exporters/excel.py`: Exports valuation results to Excel reports.
* `models/valuation.py`: Calculates Graham intrinsic value and margin of safety.
* `scrapers/comafi.py`, `scrapers/fred.py`, `scrapers/market.py`: Fetch data from COMAFI, FRED, and stock market financials, respectively.
* `main.py`: Orchestrates the pipeline execution, from data fetching to report export and upload.

## Prerequisites and Environment Setup
To run the CEDEAR Valuation Pipeline, ensure you have:
* Python 3.8 or later installed
* A compatible operating system (Windows, macOS, or Linux)
* The `uv` package manager installed (for environment management)

Create and activate a virtual environment using `uv`:
```bash
uv sync
uv run python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```
### Configuration
The pipeline uses a JSON configuration file (`config.json` by default). You can specify the following parameters:
* `fred_api_key`: Your FRED API key
* `google_drive`: Google Drive configuration (optional)
	+ `enabled`: Whether to upload reports to Google Drive (default: `false`)
	+ `remote_name`: The remote name for rclone (default: `gdrive`)
	+ `folder_name`: The folder name for uploaded reports (default: `CEDEAR_Reports`)
* `sectors`: A dictionary of sectors with tickers (e.g., `{"General": ["AAPL", "GOOG"]}`)

## Installation
To install the required dependencies, run:
```bash
uv sync
```
This will synchronize the environment using the `uv.lock` file.

## Usage Example
To execute the pipeline, run:
```bash
financial-data-scrapper --config path/to/config.json
```

## ☁️ Google Drive Setup with `rclone`

Follow these steps to configure `rclone` for automatically uploading generated report files to your Google Drive.

### 1. Install `rclone` (Linux / WSL)

If you haven't installed `rclone` yet, run the following command in your terminal:

```bash
sudo apt update && sudo apt install -y rclone
```

### 2. Configure the Remote Access
Run the interactive configuration wizard:
```bash
rclone config
```

Follow the step-by-step interactive prompt:

- `New Remote`: Type n and press Enter.

- `Name`: Type inverg (or the remote_name specified in your config.json) and press Enter.

- `Storage Type`: Select Google Drive by entering 18 (or typing drive) and press Enter.

- `Client ID`: Leave blank, press Enter.

- `Client Secret`: Leave blank, press Enter.

- `Scope`: Type 1 (Full access) and press Enter.

- `Service Account File`: Leave blank, press Enter.

- `Advanced Config`: Type n and press Enter.

- `Auto Config`: Type y and press Enter.


If using WSL or a remote terminal: Copy the generated `http://127.0.0.1:53682/auth...` URL into your web browser, sign in with your Google account, grant the required permissions, and copy the authorization code back if prompted.

- `Shared Drive`: Type n and press Enter.

- `Confirm`: Type y to accept the configuration.

- `Quit`: Type q to exit the setup wizard.

### 3. Verify the Connection
You can verify that your Google Drive remote is properly linked by listing the root directories:

```bash
rclone lsd inverg
```

### 4. Update config.json
Ensure your config.json includes the correct google_drive parameters matching your rclone remote name and target folder path:

```json
{
  "google_drive": {
    "enabled": true,
    "remote_name": "remote_name",
    "folder_name": "path_folder"
  }
}
```

## Usage Restrictions
The pipeline requires a stable internet connection for data fetching. Additionally, the FRED API key and Google Drive configuration (if used) must be valid and properly set up.

## Workflow Diagram
```mermaid
graph LR
    A[Start] -->|Load Configuration| B
    B -->|Fetch COMAFI Data| C
    B -->|Fetch FRED AAA Yield| D
    C -->|Process COMAFI Data| E
    D -->|Calculate Intrinsic Value| F
    E -->|Analyze Stock Financials| G
    F -->|Calculate Margin of Safety| H
    G -->|Export Valuation Results| I
    H -->|Export Valuation Results| I
    I -->|Upload to Google Drive if enabled| J
    J -->|Finish| K
```
Note: This diagram illustrates the main workflow of the pipeline, from loading configuration to uploading reports to Google Drive (if enabled).
