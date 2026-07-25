import json
from pathlib import Path

# Ruta al archivo config.json en la raíz del proyecto
CONFIG_PATH = Path("config.json")


def load_config(config_file: Path = CONFIG_PATH) -> dict:
    """Carga los parámetros de configuración desde un archivo JSON.

    Soporta tanto la nueva estructura 'sectors' (diccionario) como la
    lista clásica de 'tickers'.
    """
    if not config_file.exists():
        raise FileNotFoundError(
            f"El archivo de configuración '{config_file}' no existe en la raíz del proyecto."
        )

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    if not config.get("fred_api_key"):
        raise ValueError(
            "Falta especificar 'fred_api_key' en el archivo config.json"
        )

    # Validar que exista al menos 'sectors' (diccionario) o 'tickers' (lista)
    has_sectors = isinstance(config.get("sectors"), dict) and len(
        config["sectors"]
    ) > 0
    has_tickers = isinstance(config.get("tickers"), list) and len(
        config["tickers"]
    ) > 0

    if not (has_sectors or has_tickers):
        raise ValueError(
            "El archivo config.json debe contener una estructura válida de 'sectors' o una lista de 'tickers'."
        )

    return config