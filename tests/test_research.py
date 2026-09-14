from unittest.mock import patch

import pytest

from tools.research import research


def test_research_returns_results():
    mock_response = {
        "results": [
            {
                "title": "AI Research",
                "url": "https://example.edu/ai",
                "content": "Research about artificial intelligence.",
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
    assert results[0]["content"] == (
        "Research about artificial intelligence."
    )


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