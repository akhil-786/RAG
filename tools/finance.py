import os
import finnhub
from dotenv import load_dotenv

load_dotenv()

finnhub_client = finnhub.Client(
    api_key=os.getenv("FIN_HUB_API")
)

def get_stock_price(symbol):
    try:
        quote = finnhub_client.quote(symbol)

        return {
            "symbol": symbol,
            "current_price": quote["c"],
            "high": quote["h"],
            "low": quote["l"],
            "open": quote["o"],
            "previous_close": quote["pc"]
        }

    except Exception as e:
        return f"Finance tool failed: {str(e)}"