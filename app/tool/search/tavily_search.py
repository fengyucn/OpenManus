import asyncio
import aiohttp
from typing import List
from app.schema import WebSearchEngine
from app.config import TAVILY_API_KEY

class TavilySearchEngine:
    """Search engine using Tavily API."""
    
    async def perform_search(self, query: str, num_results: int = 10) -> List[str]:
        """Perform a search using Tavily API and return URLs."""
        headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "topic": "general",
            "max_results": num_results,
            "search_depth": "basic",
        }
        url = "https://api.tavily.com/search"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Tavily API error: {response.status}")
                
                data = await response.json()
                return [result["url"] for result in data.get("results", [])][:num_results]
