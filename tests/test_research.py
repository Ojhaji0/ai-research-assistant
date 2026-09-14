from unittest.mock import patch

import pytest

from tools.research import (
    research,
    research_multiple_queries,
    planned_research,
    planned_research_with_evidence,
)


def test_research_returns_results():
    mock_response = {
        "results": [
            {
                "title": "AI Research",
                "url": "https://example.edu/ai",
                "content": (
                    "Research about artificial intelligence in modern "
                    "technology and enterprise workflows."
                ),
                "score": 0.9,
            }
        ]
    }

    with patch(
        "tools.research.tavily.search",
        return_value=mock_response,
    ):
        results = research("AI")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["title"] == "AI Research"
    assert results[0]["url"] == "https://example.edu/ai"
    assert "artificial intelligence" in results[0]["content"]


def test_research_empty_results():
    mock_response = {
        "results": []
    }

    with patch(
        "tools.research.tavily.search",
        return_value=mock_response,
    ):
        results = research("unknown topic")

    assert results == []


def test_research_api_error():
    with patch(
        "tools.research.tavily.search",
        side_effect=RuntimeError("Tavily API unavailable"),
    ):
        with pytest.raises(
            RuntimeError,
            match="Tavily API unavailable",
        ):
            research("AI")


def test_research_deduplicates_urls():
    mock_response = {
        "results": [
            {
                "title": "First Result",
                "url": "https://example.com/article",
                "content": (
                    "First content with sufficiently long text "
                    "to pass quality filter."
                ),
                "score": 0.9,
            },
            {
                "title": "Duplicate Result",
                "url": "https://example.com/article/",
                "content": (
                    "Duplicate content with sufficiently long text "
                    "to pass quality filter."
                ),
                "score": 0.8,
            },
            {
                "title": "Unique Result",
                "url": "https://example.com/other",
                "content": (
                    "Unique content with sufficiently long text "
                    "to pass quality filter."
                ),
                "score": 0.7,
            },
        ]
    }

    with patch(
        "tools.research.tavily.search",
        return_value=mock_response,
    ):
        results = research("AI")

    assert len(results) == 2
    assert results[0]["title"] == "First Result"
    assert results[1]["title"] == "Unique Result"


def test_research_filters_low_quality_sources():
    mock_response = {
        "results": [
            {
                "title": "Good Source",
                "url": "https://example.com/good",
                "content": (
                    "This is sufficiently detailed content "
                    "that should pass the quality filter."
                ),
                "score": 0.9,
            },
            {
                "title": "Short Source",
                "url": "https://example.com/short",
                "content": "Too short",
                "score": 0.99,
            },
            {
                "title": "",
                "url": "https://example.com/no-title",
                "content": (
                    "This content is long enough but has no title."
                ),
                "score": 0.99,
            },
        ]
    }

    with patch(
        "tools.research.tavily.search",
        return_value=mock_response,
    ):
        results = research("AI")

    assert len(results) == 1
    assert results[0]["title"] == "Good Source"


def test_research_ranks_sources_and_limits_to_top_five():
    mock_response = {
        "results": [
            {
                "title": "Normal Source",
                "url": "https://example.com/normal",
                "content": (
                    "A sufficiently detailed research source "
                    "with useful information for analysis."
                ),
                "score": 0.9,
            },
            {
                "title": "Academic Source",
                "url": "https://research.edu/academic",
                "content": (
                    "A sufficiently detailed academic research source "
                    "with useful information for analysis."
                ),
                "score": 0.5,
            },
            {
                "title": "Government Source",
                "url": "https://agency.gov/report",
                "content": (
                    "A sufficiently detailed government research source "
                    "with useful information for analysis."
                ),
                "score": 0.6,
            },
            {
                "title": "Microsoft Source",
                "url": "https://microsoft.com/research",
                "content": (
                    "A sufficiently detailed technology research source "
                    "with useful information for analysis."
                ),
                "score": 0.7,
            },
            {
                "title": "OpenAI Source",
                "url": "https://openai.com/research",
                "content": (
                    "A sufficiently detailed AI research source "
                    "with useful information for analysis."
                ),
                "score": 0.8,
            },
            {
                "title": "Extra Source 1",
                "url": "https://extra1.com/research",
                "content": (
                    "A sufficiently detailed extra research source "
                    "with useful information for analysis."
                ),
                "score": 0.4,
            },
            {
                "title": "Extra Source 2",
                "url": "https://extra2.com/research",
                "content": (
                    "A sufficiently detailed extra research source "
                    "with useful information for analysis."
                ),
                "score": 0.3,
            },
        ]
    }

    with patch(
        "tools.research.tavily.search",
        return_value=mock_response,
    ):
        results = research("AI")

    assert len(results) == 5

    scores = [source["score"] for source in results]

    assert scores == sorted(scores, reverse=True)

    titles = [source["title"] for source in results]

    assert "Academic Source" in titles
    assert "Government Source" in titles
    assert "Microsoft Source" in titles
    assert "OpenAI Source" in titles

    assert "Extra Source 1" not in titles
    assert "Extra Source 2" not in titles


def test_research_multiple_queries_aggregates_results():
    responses = [
        {
            "results": [
                {
                    "title": "Source One",
                    "url": "https://example.com/one",
                    "content": (
                        "This is sufficiently detailed content "
                        "for the first research query."
                    ),
                    "score": 0.9,
                }
            ]
        },
        {
            "results": [
                {
                    "title": "Source Two",
                    "url": "https://example.com/two",
                    "content": (
                        "This is sufficiently detailed content "
                        "for the second research query."
                    ),
                    "score": 0.8,
                }
            ]
        },
    ]

    with patch(
        "tools.research.tavily.search",
        side_effect=responses,
    ):
        results = research_multiple_queries(
            [
                "AI agents overview",
                "AI agents latest developments",
            ]
        )

    assert len(results) == 2
    assert results[0]["title"] == "Source One"
    assert results[1]["title"] == "Source Two"


def test_planned_research_runs_full_pipeline():
    raw_results = [
        {
            "title": "Normal Source",
            "url": "https://example.com/normal",
            "content": (
                "This is sufficiently detailed research content "
                "that should pass the quality filter."
            ),
            "score": 0.9,
        },
        {
            "title": "Academic Source",
            "url": "https://research.edu/academic",
            "content": (
                "This is sufficiently detailed academic research "
                "content that should receive a quality bonus."
            ),
            "score": 0.5,
        },
        {
            "title": "Duplicate Source",
            "url": "https://example.com/normal/",
            "content": (
                "This duplicate source should be removed by "
                "the URL deduplication step."
            ),
            "score": 0.8,
        },
    ]

    with patch(
        "tools.research.research_multiple_queries",
        return_value=raw_results,
    ):
        results = planned_research("AI agents")

    assert len(results) == 2
    assert results[0]["title"] == "Academic Source"
    assert results[1]["title"] == "Normal Source"
    assert results[0]["score"] > results[1]["score"]


def test_planned_research_with_evidence(monkeypatch):
    sources = [
        {
            "title": "AI Agents Report",
            "url": "https://example.com/report",
            "content": "AI agents can plan and use tools.",
            "score": 4.5,
        }
    ]

    monkeypatch.setattr(
        "tools.research.planned_research",
        lambda topic: sources,
    )

    result = planned_research_with_evidence("AI agents")

    assert result["sources"] == sources
    assert len(result["evidence"]) == 1
    assert result["evidence"][0]["title"] == "AI Agents Report"
    assert result["evidence"][0]["url"] == "https://example.com/report"
    assert result["evidence"][0]["snippet"] == sources[0]["content"]
