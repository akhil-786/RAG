import os
import requests
from dotenv import load_dotenv

load_dotenv()

def web_search(query):
    try:
        response = requests.post(
            "https://search-router.com/api/search",
            headers={
                "X-API-Key": os.getenv("SEARCH_API_KEY")
            },
            json={
                "query": query,
                "num_results": 5
            },
            timeout=10
        )

        return response.json()

    except Exception as e:
        return f"Search failed: {str(e)}"