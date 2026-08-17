import argparse
import re
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
from cedear_valuation.scrapers.dolarhoy import fetch_dolar_ccl_venta
from cedear_valuation.scrapers.fred import fetch_fred_aaa_yield
from cedear_valuation.scrapers.market import fetch_stock_financials
from cedear_valuation.scrapers.yahoo_jina import calculate_ccl_from_yahoo_jina

# Fallback/Overrides manuales solo si un ticker no existe en Comafi
MANUAL_RATIOS = {
    "BRK-B": 22.0,
    "BRKB": 22.0,
}


def upload_via_rclone(file_path: Path, remote_name: str, folder_name: str):
    """Synchronizes the local file with Google Drive using rclone."""
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

    # 1. Load configuration
    config_path = Path(args.config)
    config = load_config(config_path)

    fred_api_key = config["fred_api_key"]
    drive_config = config.get("google_drive", {})

    sectors = config.get("sectors", {})
    if not sectors and "tickers" in config:
        sectors = {"General": config["tickers"]}

    # 2. Base scrapers (Comafi for ratios)
    raw_comafi_df = fetch_comafi_cedears()
    processed_comafi_df = process_cedear_ratios(raw_comafi_df)

    # Identificar la columna de Ratio una sola vez fuera del loop
    ratio_col = None
    if not processed_comafi_df.empty:
        ratio_col = next(
            (c for c in processed_comafi_df.columns if "ratio" in c.lower()),
            None,
        )

    # 3. FRED Rate and CCL Benchmark Dollar from DolarHoy
    aaa_rate = fetch_fred_aaa_yield(api_key=fred_api_key)
    ccl_benchmark = fetch_dolar_ccl_venta()

    # 4. Parse tickers and sectors
    valuation_results = []
    for sector_name, tickers in sectors.items():
        for ticker in tickers:
            lookup_ticker = ticker.upper().strip()

            # Normalizar ticker buscado (remover '/' y '-') para hacer matching tolerante
            norm_lookup = re.sub(r"[\/\-]", "", lookup_ticker)

            ratio_val = 1.0
            found_ratio = False

            # Intento 1: Buscar en el DataFrame procesado de Comafi usando normalized_ticker
            if (
                not processed_comafi_df.empty
                and "normalized_ticker" in processed_comafi_df.columns
                and ratio_col
            ):
                match = processed_comafi_df[
                    processed_comafi_df["normalized_ticker"] == norm_lookup
                ]
                if not match.empty:
                    try:
                        raw_ratio = str(match.iloc[0][ratio_col]).strip()
                        if ":" in raw_ratio:
                            num, denom = raw_ratio.split(":")
                            ratio_val = float(num) / float(denom)
                        elif "/" in raw_ratio:
                            num, denom = raw_ratio.split("/")
                            ratio_val = float(num) / float(denom)
                        else:
                            ratio_val = float(raw_ratio)
                        found_ratio = True
                    except (ValueError, ZeroDivisionError):
                        ratio_val = 1.0

            # Intento 2: Fallback a MANUAL_RATIOS si no se encontró en Comafi
            if not found_ratio and lookup_ticker in MANUAL_RATIOS:
                ratio_val = MANUAL_RATIOS[lookup_ticker]

            # Get price in USD, ARS and CCL using yfinance
            yahoo_data = calculate_ccl_from_yahoo_jina(
                lookup_ticker, ratio=ratio_val
            )
            ccl_val = yahoo_data.get("ccl")

            # Get financial metrics (EPS, Growth, etc.)
            fin_data = fetch_stock_financials(
                lookup_ticker, sector=sector_name
            )
            if fin_data:
                eps = fin_data.get("trailing_eps")
                growth = fin_data.get("earnings_growth")
                price = yahoo_data.get("price_usd") or fin_data.get(
                    "current_price"
                )

                intrinsic_val = calculate_graham_intrinsic_value(
                    eps, growth, aaa_rate
                )
                margin = calculate_margin_of_safety(price, intrinsic_val)

                print(
                    f"[{lookup_ticker}] USD: {price:.2f} | "
                    f"Ratio: {ratio_val} | "
                    f"Intrinsic Val: {intrinsic_val:.2f} | "
                    f"CCL (Yahoo): {ccl_val}"
                )

                # Assignment of final data
                fin_data["current_price"] = price
                fin_data["intrinsic_value_graham"] = intrinsic_val
                fin_data["margin_of_safety_%"] = margin
                fin_data["ccl"] = ccl_val
                fin_data["aaa_rate_used"] = aaa_rate

                valuation_results.append(fin_data)

    if valuation_results:
        valuation_df = pd.DataFrame(valuation_results)
        valuation_df = valuation_df.sort_values(
            by="margin_of_safety_%", ascending=False
        ).reset_index(drop=True)
    else:
        valuation_df = pd.DataFrame()

    # 5. Export report locally
    report_file = export_to_excel(
        comafi_df=processed_comafi_df,
        valuation_df=valuation_df,
        ccl_benchmark=ccl_benchmark,
    )

    # 6. Upload to Google Drive (if enabled in config.json)
    if drive_config.get("enabled", False):
        remote_name = drive_config.get("remote_name", "gdrive")
        folder_name = drive_config.get("folder_name", "CEDEAR_Reports")
        upload_via_rclone(report_file, remote_name, folder_name)

    print("=== Pipeline Execution Finished ===")


if __name__ == "__main__":
    main()