from io import StringIO
import re
import pandas as pd
import requests

COMAFI_URL = "https://www.comafi.com.ar/custodiaglobal/programas.aspx"
JINA_URL = f"https://r.jina.ai/{COMAFI_URL}"


def fetch_comafi_cedears() -> pd.DataFrame:
    """Extracts CEDEAR table from Banco Comafi via Jina AI and returns a clean DataFrame."""
    print("Fetching CEDEAR data from Banco Comafi via Jina AI...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(JINA_URL, headers=headers, timeout=25)
        response.raise_for_status()

        # 1. Filter only lines belonging to the Markdown table
        lines = [
            line.strip()
            for line in response.text.split("\n")
            if line.strip().startswith("|")
        ]

        if not lines:
            print("[WARN] No table lines found in Jina AI response.")
            return pd.DataFrame()

        # 2. Convert Markdown table to DataFrame using '|' as separator
        df = pd.read_csv(
            StringIO("\n".join(lines)),
            sep="|",
            engine="python",
            skipinitialspace=True,
        )

        # 3. Remove empty columns created by '|' borders
        df = df.dropna(how="all", axis=1)

        # 4. Normalize column names
        df.columns = df.columns.str.strip()

        # 5. Clean cells (remove bold asterisks and spaces)
        for col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"\*\*", "", regex=True)
                .str.strip()
            )

        # 6. Create auxiliary column with normalized tickers (removes '/' and '-') to facilitate search in main.py
        ticker_col = df.columns[0]
        df["normalized_ticker"] = (
            df[ticker_col]
            .astype(str)
            .str.upper()
            .str.replace(r"[\/\-]", "", regex=True)
        )

        return df

    except Exception as e:
        print(f"[ERROR] Error querying or parsing data from Banco Comafi: {e}")
        return pd.DataFrame()


def process_cedear_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Intermediate step to validate or process additional transformations in the table."""
    if df.empty:
        return df
    return df