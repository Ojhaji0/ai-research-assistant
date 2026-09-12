from tools.research import research


def test_research_returns_results():
    results = research("AI")
    assert isinstance(results, list)
    assert len(results) >= 1
    assert "title" in results[0]
    assert "url" in results[0]
    assert "content" in results[0]
