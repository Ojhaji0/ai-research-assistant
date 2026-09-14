from tools.research import filter_quality_sources


def test_valid_source_is_kept():
    results = [
        {
            "title": "Valid AI Source",
            "url": "https://example.com/ai",
            "content": (
                "Artificial intelligence is transforming "
                "many industries through advanced automation."
            ),
        }
    ]

    filtered = filter_quality_sources(results)

    assert len(filtered) == 1
    assert filtered[0]["title"] == "Valid AI Source"


def test_missing_title_is_removed():
    results = [
        {
            "title": "",
            "url": "https://example.com/ai",
            "content": (
                "Artificial intelligence is transforming "
                "many industries through advanced automation."
            ),
        }
    ]

    assert filter_quality_sources(results) == []


def test_missing_content_is_removed():
    results = [
        {
            "title": "AI Source",
            "url": "https://example.com/ai",
            "content": "",
        }
    ]

    assert filter_quality_sources(results) == []


def test_short_content_is_removed():
    results = [
        {
            "title": "Weak Source",
            "url": "https://example.com/ai",
            "content": "Too short",
        }
    ]

    assert filter_quality_sources(results) == []


def test_mixed_results_keep_only_quality_sources():
    results = [
        {
            "title": "Good Source",
            "url": "https://example.com/good",
            "content": (
                "This is sufficiently detailed content "
                "that should pass the quality filter."
            ),
        },
        {
            "title": "",
            "url": "https://example.com/no-title",
            "content": (
                "This content is long enough but has no title."
            ),
        },
        {
            "title": "Short Source",
            "url": "https://example.com/short",
            "content": "Too short",
        },
    ]

    filtered = filter_quality_sources(results)

    assert len(filtered) == 1
    assert filtered[0]["title"] == "Good Source"