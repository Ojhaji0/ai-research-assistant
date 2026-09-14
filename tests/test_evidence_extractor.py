import pytest

from evidence.extractor import (
    extract_evidence,
    extract_evidence_from_sources,
)


def test_extract_evidence_returns_structured_evidence():
    source = {
        "title": "AI Agents Report",
        "url": "https://example.com/report",
        "content": "AI agents can plan, use tools, and execute multi-step tasks.",
        "score": 4.5,
    }

    result = extract_evidence(source)

    assert result["title"] == "AI Agents Report"
    assert result["url"] == "https://example.com/report"
    assert result["snippet"] == source["content"]
    assert result["source_score"] == 4.5


def test_extract_evidence_limits_snippet_length():
    source = {
        "title": "Long Report",
        "url": "https://example.com/report",
        "content": "A" * 1000,
        "score": 3.0,
    }

    result = extract_evidence(source, max_length=100)

    assert len(result["snippet"]) == 100


def test_extract_evidence_requires_title():
    source = {
        "url": "https://example.com",
        "content": "Some content",
    }

    with pytest.raises(ValueError, match="Source title is required"):
        extract_evidence(source)


def test_extract_evidence_requires_url():
    source = {
        "title": "Example",
        "content": "Some content",
    }

    with pytest.raises(ValueError, match="Source URL is required"):
        extract_evidence(source)


def test_extract_evidence_requires_content():
    source = {
        "title": "Example",
        "url": "https://example.com",
    }

    with pytest.raises(ValueError, match="Source content is required"):
        extract_evidence(source)


def test_extract_evidence_from_sources():
    sources = [
        {
            "title": "Source One",
            "url": "https://example.com/one",
            "content": "Evidence from source one.",
            "score": 4.0,
        },
        {
            "title": "Source Two",
            "url": "https://example.com/two",
            "content": "Evidence from source two.",
            "score": 3.5,
        },
    ]

    result = extract_evidence_from_sources(sources)

    assert len(result) == 2
    assert result[0]["title"] == "Source One"
    assert result[1]["title"] == "Source Two"


def test_extract_evidence_from_empty_sources():
    assert extract_evidence_from_sources([]) == []