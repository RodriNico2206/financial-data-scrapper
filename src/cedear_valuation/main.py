import argparse
import subprocess
import sys
from pathlib import Path
import pandas as pd

# Add 'src' directory to Python module search path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cedear_valuation.config import load_config
from cedear_valuation.exporters.excel import export_to_excel
from cedear_valuation.models.valuation import (
    calculate_graham_intrinsic_value,
    calculate_margin_of_safety,
)
from cedear_valuation.scrapers.comafi import (
    fetch_comafi_cedears,
    process_cedear_ratios,
)
from cedear_valuation.scrapers.fred import fetch_fred_aaa_yield
from cedear_valuation.scrapers.market import fetch_stock_financials


def upload_via_rclone(file_path: Path, remote_name: str, folder_name: str):
    """Sincroniza el archivo local con Google Drive usando rclone."""
    destination = f"{remote_name}:{folder_name}"
    command = ["rclone", "copy", str(file_path), destination]

    print(f"Uploading '{file_path.name}' to Google Drive at '{destination}'...")
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("File successfully uploaded to Google Drive!")
        else:
            print(f"Error uploading via rclone: {result.stderr.strip()}")
    except FileNotFoundError:
        print(
            "Error: 'rclone' is not installed on the system or is not in PATH."
        )


def main():
    parser = argparse.ArgumentParser(description="CEDEAR Valuation Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Ruta al archivo JSON de configuración (default: config.json)",
    )
    args = parser.parse_args()

    print("=== Starting CEDEAR Valuation Pipeline ===")

    # 1. Cargar configuración
    config_path = Path(args.config)
    config = load_config(config_path)

    fred_api_key = config["fred_api_key"]
    drive_config = config.get("google_drive", {})

    sectors = config.get("sectors", {})
    if not sectors and "tickers" in config:
        sectors = {"General": config["tickers"]}

    # 2. Scrapers
    raw_comafi_df = fetch_comafi_cedears()
    processed_comafi_df = process_cedear_ratios(raw_comafi_df)

    # 3. Tasa FRED
    aaa_rate = fetch_fred_aaa_yield(api_key=fred_api_key)

    # 4. Analizar tickers y sectores
    valuation_results = []
    for sector_name, tickers in sectors.items():
        for ticker in tickers:
            fin_data = fetch_stock_financials(ticker, sector=sector_name)
            if fin_data:
                eps = fin_data.get("trailing_eps")
                growth = fin_data.get("earnings_growth")
                price = fin_data.get("current_price")

                intrinsic_val = calculate_graham_intrinsic_value(
                    eps, growth, aaa_rate
                )
                margin = calculate_margin_of_safety(price, intrinsic_val)

                fin_data["intrinsic_value_graham"] = intrinsic_val
                fin_data["margin_of_safety_%"] = margin
                fin_data["aaa_rate_used"] = aaa_rate

                valuation_results.append(fin_data)

    if valuation_results:
        valuation_df = pd.DataFrame(valuation_results)
        valuation_df = valuation_df.sort_values(
            by="margin_of_safety_%", ascending=False
        ).reset_index(drop=True)
    else:
        valuation_df = pd.DataFrame()

    # 5. Exportar reporte localmente
    report_file = export_to_excel(processed_comafi_df, valuation_df)

    # 6. Subir a Google Drive (si está habilitado en config.json)
    if drive_config.get("enabled", False):
        remote_name = drive_config.get("remote_name", "gdrive")
        folder_name = drive_config.get("folder_name", "CEDEAR_Reports")
        upload_via_rclone(report_file, remote_name, folder_name)

    print("=== Pipeline Execution Finished ===")


if __name__ == "__main__":
    main()