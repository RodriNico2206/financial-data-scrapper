import requests

FRED_SERIES_ID = "AAA"

def fetch_fred_aaa_yield(api_key: str) -> float:
    """
    Obtiene la tasa de rendimientos de bonos AAA de Moody's a través de la API oficial de FRED.
    Si falla la conexión, retorna un valor por defecto de 5.0%.
    """
    print("Fetching AAA Corporate Bond Yield from FRED API...")
    
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id={FRED_SERIES_ID}"
        f"&api_key={api_key}"
        f"&file_type=json"
        f"&sort_order=desc"
        f"&limit=10"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        for obs in data.get("observations", []):
            val_str = obs.get("value", "").strip()
            date_str = obs.get("date", "")
            try:
                rate = float(val_str)
                print(f"Retrieved FRED AAA Yield ({date_str}): {rate}%")
                return rate
            except ValueError:
                continue

        raise ValueError("No valid numerical observation found in FRED API response.")

    except Exception as e:
        print(f"Warning: Failed to fetch FRED rate ({e}). Using default fallback 5.0%")
        return 5.0