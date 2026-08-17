import yfinance as yf


def fetch_yahoo_price(symbol: str) -> float | None:
    """Extracts the closing price or current price directly from Yahoo Finance."""
    clean_symbol = symbol.strip().upper()

    # Specific normalization for the local Berkshire Hathaway CEDEAR
    if clean_symbol == "BRK-B.BA":
        clean_symbol = "BRKB.BA"

    try:
        ticker_obj = yf.Ticker(clean_symbol)
        price = getattr(ticker_obj.fast_info, "last_price", None)

        if not price or price <= 0:
            hist = ticker_obj.history(period="1d")
            if not hist.empty and "Close" in hist.columns:
                price = float(hist["Close"].iloc[-1])

        if price and price > 0:
            return float(price)

    except Exception as e:
        print(f"Error fetching {clean_symbol} via yfinance: {e}")

    return None


def calculate_ccl_from_yahoo_jina(
    ticker: str, ratio: float
) -> dict[str, float | None]:
    """Calcula el Dólar CCL implícito consultando los precios en USD y ARS.

    Fórmula: CCL = (Precio_ARS / Precio_USD) * Ratio
    """
    symbol_usd = ticker.upper().strip()
    symbol_ars = "BRKB.BA" if symbol_usd == "BRK-B" else f"{symbol_usd}.BA"

    price_usd = fetch_yahoo_price(symbol_usd)
    price_ars = fetch_yahoo_price(symbol_ars)

    ccl = None
    if price_usd and price_ars and price_usd > 0:
        # Multiplicación directa por el ratio entero (ej. 20)
        ccl = round((price_ars / price_usd) * ratio, 2)

    return {
        "price_usd": price_usd,
        "price_ars": price_ars,
        "ccl": ccl,
    }