import os


def generate_research_report(
    topic: str,
    sources: list,
    evidence: list = None,
    output_path: str = "reports/research_report.md",
):
    """Generate a Markdown research report from research sources and evidence."""

    if isinstance(evidence, str):
        output_path = evidence
        evidence = None

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    report = f"# Research Report: {topic}\n\n"

    if evidence:
        report += "## Evidence\n\n"

        for i, item in enumerate(evidence, 1):
            report += f"### Evidence {i}\n"
            report += f"**Source:** {item.get('title', 'Untitled Source')}\n"
            report += f"**URL:** {item.get('url', 'N/A')}\n"
            report += f"**Source Score:** {item.get('source_score', 'N/A')}\n\n"
            report += f"{item.get('snippet', '')}\n\n"

    report += "## Sources\n\n"

    for i, source in enumerate(sources, 1):
        report += f"### {i}. {source.get('title', 'Untitled Source')}\n"
        report += f"URL: {source.get('url', 'N/A')}\n"
        report += f"Score: {source.get('score', 'N/A')}\n\n"
        report += f"{source.get('content', '')}\n\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path