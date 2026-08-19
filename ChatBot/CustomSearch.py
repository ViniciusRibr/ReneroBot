"""
CustomSearch.py - Google Custom Search API Client for ReneroBot.

Provides functionality to perform web searches using Google Custom Search API.
"""

import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class CustomSearchClient:
    """Helper client for interacting with Google Custom Search API."""

    def __init__(self, api_key: Optional[str] = None, search_engine_id: Optional[str] = None) -> None:
        self.api_key = api_key or os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = search_engine_id or os.getenv("GOOGLE_SEARCH_CX")
        self.endpoint = 'https://www.googleapis.com/customsearch/v1'

    def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Executes a Google Custom Search query.

        :param query: Search query string.
        :param num_results: Number of search results to return (max 10).
        :return: JSON response dictionary from API.
        """
        if not self.api_key or not self.search_engine_id:
            raise ValueError(
                "GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_CX environment variables must be set."
            )

        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'num': num_results
        }

        response = requests.get(self.endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # Quick standalone test/example execution
    try:
        client = CustomSearchClient()
        results = client.search("Python programming")
        print("Search results fetched successfully:", len(results.get("items", [])))
    except Exception as e:
        print(f"Custom search failed: {e}")
