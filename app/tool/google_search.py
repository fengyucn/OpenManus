import asyncio
import aiohttp
from typing import List
from app.config import TAVILY_API_KEY  # 假设配置文件已添加API密钥

from app.tool.base import BaseTool

class GoogleSearch(BaseTool):
    name: str = "tavily_search"
    description: str = """Perform a search using Tavily API and return a list of relevant links.
Use this tool when you need to find information on the web. The tool returns a list of URLs matching the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to Tavily.",
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 10.",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
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
                    raise Exception(f"Tavily API error: {response.status} - {await response.text()}")

                data = await response.json()
                return [result["url"] for result in data.get("results", [])][:num_results]
