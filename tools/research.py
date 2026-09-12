import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in .env file")

tavily = TavilyClient(api_key=api_key)


def research(topic: str):
    """Search the web and return ranked research sources."""

    print(f"\n[TOOL CALLED] research(topic='{topic}')")

    response = tavily.search(
        query=topic,
        search_depth="advanced",
        max_results=10
    )

    results = response.get("results", [])

    def source_score(result):
        url = result.get("url", "").lower()
        score = result.get("score", 0)

        total = score

        if ".edu" in url:
            total += 3
        elif ".gov" in url:
            total += 3
        elif any(domain in url for domain in [
            "google.com",
            "microsoft.com",
            "ibm.com",
            "salesforce.com",
            "anthropic.com",
            "openai.com"
        ]):
            total += 2
        elif "linkedin.com" in url or "medium.com" in url:
            total -= 1

        return total

    ranked_results = sorted(
        results,
        key=source_score,
        reverse=True
    )

    selected = ranked_results[:5]

    sources = []

    for result in selected:
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": round(source_score(result), 2)
        })

    print(f"[TOOL RESULT] Selected {len(sources)} quality sources")

    for i, source in enumerate(sources, 1):
        print(f"\n[{i}] {source['title']}")
        print(f"Score: {source['score']}")
        print(source["url"])

    return sources
