def extract_evidence(source: dict, max_length: int = 500):
    """Extract a concise evidence snippet from a research source."""

    title = source.get("title", "").strip()
    url = source.get("url", "").strip()
    content = source.get("content", "").strip()

    if not title:
        raise ValueError("Source title is required")

    if not url:
        raise ValueError("Source URL is required")

    if not content:
        raise ValueError("Source content is required")

    snippet = content[:max_length].strip()

    return {
        "title": title,
        "url": url,
        "snippet": snippet,
        "source_score": source.get("score", 0),
    }


def extract_evidence_from_sources(sources: list[dict]):
    """Extract structured evidence from multiple research sources."""

    return [
        extract_evidence(source)
        for source in sources
    ]