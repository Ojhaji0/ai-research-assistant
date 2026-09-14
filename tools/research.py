import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in .env file")

tavily = TavilyClient(api_key=api_key)


def source_score(result):
    """Calculate a quality score for a research source."""

    url = result.get("url", "").lower()
    score = result.get("score", 0)

    domain = urlparse(url).netloc
    domain = domain.removeprefix("www.")

    total = score

    if domain.endswith(".edu"):
        total += 3
    elif domain.endswith(".gov"):
        total += 3
    elif any(domain == trusted_domain for trusted_domain in [
        "google.com",
        "microsoft.com",
        "ibm.com",
        "salesforce.com",
        "anthropic.com",
        "openai.com",
    ]):
        total += 2
    elif domain in ["linkedin.com", "medium.com"]:
        total -= 1

    return round(total, 2)


def deduplicate_sources(results):
    """Remove duplicate sources based on normalized URLs."""

    seen_urls = set()
    unique_results = []

    for result in results:
        url = result.get("url", "").strip().lower()

        if not url:
            continue

        normalized_url = url.rstrip("/")

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_results.append(result)

    return unique_results


def filter_quality_sources(results):
    """Remove sources with missing titles or insufficient content."""

    filtered = []

    for result in results:
        title = result.get("title", "").strip()
        content = result.get("content", "").strip()

        if not title:
            continue

        if len(content) < 50:
            continue

        filtered.append(result)

    return filtered


def research_multiple_queries(queries: list[str]):
    """Run multiple research queries and aggregate their raw results."""

    if not queries:
        return []

    all_results = []

    for query in queries:
        print(f"\n[SUB-QUERY] {query}")

        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=10,
        )

        results = response.get("results", [])
        all_results.extend(results)

    return all_results


def planned_research(topic: str):
    """Run a complete multi-query research pipeline."""

    from planner.query_planner import generate_queries

    queries = generate_queries(topic)

    raw_results = research_multiple_queries(queries)

    results = deduplicate_sources(raw_results)
    results = filter_quality_sources(results)

    ranked_results = sorted(
        results,
        key=source_score,
        reverse=True,
    )

    selected = ranked_results[:5]

    sources = []

    for result in selected:
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": round(source_score(result), 2),
        })

    print(f"\n[PLANNED RESEARCH] Selected {len(sources)} quality sources")

    return sources


def research(topic: str):
    """Search the web and return ranked research sources."""

    print(f"\n[TOOL CALLED] research(topic='{topic}')")

    response = tavily.search(
        query=topic,
        search_depth="advanced",
        max_results=10,
    )

    results = response.get("results", [])

    results = deduplicate_sources(results)
    results = filter_quality_sources(results)

    ranked_results = sorted(
        results,
        key=source_score,
        reverse=True,
    )

    selected = ranked_results[:5]

    sources = []

    for result in selected:
        sources.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": round(source_score(result), 2),
        })

    print(f"[TOOL RESULT] Selected {len(sources)} quality sources")

    for i, source in enumerate(sources, 1):
        print(f"\n[{i}] {source['title']}")
        print(f"Score: {source['score']}")
        print(source["url"])

    return sources