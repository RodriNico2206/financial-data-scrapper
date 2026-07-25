import yfinance as yf


def fetch_stock_financials(
    ticker_symbol: str, sector: str = "Unassigned"
) -> dict:
    """Fetches fundamental financial metrics for a given stock ticker using yfinance.

    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL').
        sector (str): Sector category name assigned in configuration.

    Returns:
        dict: Extracted financial metrics including assigned sector.
    """
    print(f"Fetching market data for ticker: {ticker_symbol}...")
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        return {
            "ticker": ticker_symbol,
            "sector": sector,
            "company_name": info.get("shortName", ticker_symbol),
            "current_price": info.get("currentPrice")
            or info.get("regularMarketPrice"),
            "trailing_eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "earnings_growth": info.get("earningsGrowth", 0.08),  # Default 8%
            "book_value": info.get("bookValue"),
            "free_cash_flow": info.get("freeCashflow"),
            "shares_outstanding": info.get("sharesOutstanding"),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return {}