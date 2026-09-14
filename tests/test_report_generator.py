from reports.report_generator import generate_research_report


sample_sources = [
    {
        "title": "AI in Healthcare Overview",
        "url": "https://example.edu/ai-health",
        "content": "AI is transforming diagnostics and drug discovery.",
        "score": 4.5,
    },
    {
        "title": "Clinical AI Applications",
        "url": "https://example.gov/clinical-ai",
        "content": "Regulatory guidelines on medical AI systems.",
        "score": 3.8,
    },
]


def test_generate_research_report_creates_file(tmp_path):
    output_path = tmp_path / "research_report.md"

    result = generate_research_report(
        "AI in Healthcare",
        sample_sources,
        str(output_path),
    )

    assert result == str(output_path)
    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "# Research Report: AI in Healthcare" in content

    assert "AI in Healthcare Overview" in content
    assert "https://example.edu/ai-health" in content
    assert "4.5" in content
    assert "AI is transforming diagnostics and drug discovery." in content

    assert "Clinical AI Applications" in content
    assert "https://example.gov/clinical-ai" in content
    assert "3.8" in content
    assert "Regulatory guidelines on medical AI systems." in content


def test_generate_research_report_empty_sources(tmp_path):
    output_path = tmp_path / "empty_report.md"

    result = generate_research_report(
        "Empty Research",
        [],
        str(output_path),
    )

    assert result == str(output_path)
    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "# Research Report: Empty Research" in content
    assert "## Sources" in content


def test_generate_research_report_custom_path(tmp_path):
    output_path = tmp_path / "custom" / "my_report.md"

    result = generate_research_report(
        "Custom Path Test",
        sample_sources,
        str(output_path),
    )

    assert result == str(output_path)
    assert output_path.exists()


def test_generate_research_report_includes_evidence(tmp_path):
    output_path = tmp_path / "evidence_report.md"

    sources = [
        {
            "title": "AI Agents Source",
            "url": "https://example.com/ai-agents",
            "content": "Full source content.",
            "score": 4.5,
        }
    ]

    evidence = [
        {
            "title": "AI Agents Source",
            "url": "https://example.com/ai-agents",
            "snippet": "AI agents can plan and use tools.",
            "source_score": 4.5,
        }
    ]

    result = generate_research_report(
        "AI Agents",
        sources,
        evidence=evidence,
        output_path=str(output_path),
    )

    content = output_path.read_text(encoding="utf-8")

    assert result == str(output_path)
    assert "## Evidence" in content
    assert "AI agents can plan and use tools." in content
    assert "https://example.com/ai-agents" in content


def test_generate_research_report_without_evidence_remains_compatible(
    tmp_path,
):
    output_path = tmp_path / "legacy_report.md"

    sources = [
        {
            "title": "Example Source",
            "url": "https://example.com",
            "content": "Example content.",
            "score": 3.0,
        }
    ]

    generate_research_report(
        "Example Topic",
        sources,
        output_path=str(output_path),
    )

    content = output_path.read_text(encoding="utf-8")

    assert "## Evidence" not in content
    assert "## Sources" in content
    assert "Example Source" in content