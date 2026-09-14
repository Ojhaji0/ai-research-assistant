import os


def generate_research_report(
    topic: str,
    sources: list,
    output_path: str = "reports/research_report.md",
):
    """Generate a Markdown research report from research sources."""

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    report = f"# Research Report: {topic}\n\n"
    report += "## Sources\n\n"

    for i, source in enumerate(sources, 1):
        report += f"### {i}. {source.get('title', 'Untitled Source')}\n"
        report += f"URL: {source.get('url', 'N/A')}\n"
        report += f"Score: {source.get('score', 'N/A')}\n\n"
        report += f"{source.get('content', '')}\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path