import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
def research(topic: str):
    print(f"\n[TOOL CALLED] research(topic='{topic}')")

    response = tavily.search(
        query=topic,
        search_depth="advanced",
        max_results=5
    )

    sources = []

    for result in response["results"]:
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", "")
        })

    print(f"[TOOL RESULT] Found {len(sources)} sources")

    return sources