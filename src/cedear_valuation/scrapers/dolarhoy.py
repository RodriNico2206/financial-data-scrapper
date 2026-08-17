import re
import requests


def fetch_dolar_ccl_venta() -> float | None:
    """Extrae la cotización del Dólar CCL Venta desde DolarHoy usando r.jina.ai."""
    jina_url = "https://r.jina.ai/https://dolarhoy.com/"
    print("Fetching CCL Dollar quote from DolarHoy via Jina AI...")

    try:
        response = requests.get(jina_url, timeout=15)
        response.raise_for_status()
        text = response.text

        # Buscar en el texto procesado por Jina la sección del Contado con Liquidación
        # Regex que busca 'Contado con Liqui' o 'CCL' seguido del bloque de Compra / Venta
        match = re.search(
            r"Contado con Liqui.*?Venta\s*\$?\s*([\d\.\,]+)", text, re.IGNORECASE | re.DOTALL
        )

        if match:
            raw_price = match.group(1).replace(".", "").replace(",", ".")
            ccl_price = float(raw_price)
            print(f"Retrieved Benchmark CCL (Venta): ${ccl_price:.2f} ARS")
            return ccl_price

        print("Warning: Could not extract CCL Venta price from Jina response.")
        return None

    except Exception as e:
        print(f"Error fetching CCL from DolarHoy: {e}")
        return None