import pandas as pd
import requests

COMAFI_URL = "https://www.comafi.com.ar/custodiaglobal/programasaspx-2483.note.aspx"

def fetch_comafi_cedears():
    print("Fetching CEDEAR data from Banco Comafi...")
    try:
        # Pandas usa lxml por debajo para parsear las tablas directamente
        dfs = pd.read_html(COMAFI_URL)
        if dfs:
            # Retornamos la primera tabla encontrada
            return dfs[0]
    except Exception as e:
        print(f"Failed to fetch Comafi table: {e}")
        return pd.DataFrame()

def process_cedear_ratios(df):
    if df.empty:
        return df
    
    # Limpieza o procesamiento rápido de la tabla si es necesario
    return df