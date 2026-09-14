import pytest

from planner.query_planner import generate_queries


def test_generate_queries_returns_five_queries():
    queries = generate_queries("AI agents")

    assert len(queries) == 5


def test_generate_queries_contains_topic():
    queries = generate_queries("AI agents")

    for query in queries:
        assert "AI agents" in query


def test_generate_queries_has_different_research_angles():
    queries = generate_queries("AI agents")

    assert "overview" in queries[0]
    assert "latest developments" in queries[1]
    assert "benefits" in queries[2]
    assert "limitations" in queries[3]
    assert "applications" in queries[4]


def test_generate_queries_rejects_empty_topic():
    with pytest.raises(ValueError, match="Research topic cannot be empty"):
        generate_queries("")


def test_generate_queries_strips_whitespace():
    queries = generate_queries("  AI agents  ")

    assert all("AI agents" in query for query in queries)