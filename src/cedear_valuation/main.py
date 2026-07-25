import argparse
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


def main():
    # Configurar el analizador de argumentos por línea de comandos
    parser = argparse.ArgumentParser(description="CEDEAR Valuation Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Ruta al archivo JSON de configuración (default: config.json)",
    )
    args = parser.parse_args()

    print("=== Starting CEDEAR Valuation Pipeline ===")

    # 1. Cargar parámetros desde el archivo JSON de configuración
    config_path = Path(args.config)
    config = load_config(config_path)

    fred_api_key = config["fred_api_key"]
    
    # Compatibilidad para estructura por sectores o lista simple
    sectors = config.get("sectors", {})
    if not sectors and "tickers" in config:
        sectors = {"General": config["tickers"]}

    # 2. Obtener tabla de CEDEARs desde Banco Comafi
    raw_comafi_df = fetch_comafi_cedears()
    processed_comafi_df = process_cedear_ratios(raw_comafi_df)

    # 3. Obtener la tasa de bonos AAA desde la API de FRED
    aaa_rate = fetch_fred_aaa_yield(api_key=fred_api_key)

    # 4. Analizar los sectores y tickers definidos en el JSON
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

    # Convertir a DataFrame y ordenar de mayor a menor por Margen de Seguridad
    if valuation_results:
        valuation_df = pd.DataFrame(valuation_results)
        valuation_df = valuation_df.sort_values(
            by="margin_of_safety_%", ascending=False
        ).reset_index(drop=True)
    else:
        valuation_df = pd.DataFrame()

    # 5. Exportar resultados al reporte Excel con formato y glosario
    export_to_excel(processed_comafi_df, valuation_df)
    print("=== Pipeline Execution Finished ===")


if __name__ == "__main__":
    main()