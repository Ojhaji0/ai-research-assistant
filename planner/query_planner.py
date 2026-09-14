def generate_queries(topic: str):
    """Generate focused research queries from a topic."""

    topic = topic.strip()

    if not topic:
        raise ValueError("Research topic cannot be empty")

    return [
        f"{topic} overview and fundamentals",
        f"{topic} latest developments and trends",
        f"{topic} benefits and advantages",
        f"{topic} limitations and challenges",
        f"{topic} real world applications",
    ]