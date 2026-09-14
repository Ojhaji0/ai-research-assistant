from tools.research import deduplicate_sources


def test_duplicate_urls_are_removed():
    results = [
        {
            "title": "First",
            "url": "https://example.com/article",
        },
        {
            "title": "Duplicate",
            "url": "https://example.com/article",
        },
        {
            "title": "Second",
            "url": "https://example.com/other",
        },
    ]

    unique = deduplicate_sources(results)

    assert len(unique) == 2
    assert unique[0]["title"] == "First"
    assert unique[1]["title"] == "Second"


def test_trailing_slash_is_normalized():
    results = [
        {
            "title": "First",
            "url": "https://example.com/article",
        },
        {
            "title": "Duplicate",
            "url": "https://example.com/article/",
        },
    ]

    unique = deduplicate_sources(results)

    assert len(unique) == 1


def test_url_matching_is_case_insensitive():
    results = [
        {
            "title": "First",
            "url": "https://EXAMPLE.COM/article",
        },
        {
            "title": "Duplicate",
            "url": "https://example.com/article",
        },
    ]

    unique = deduplicate_sources(results)

    assert len(unique) == 1


def test_empty_urls_are_removed():
    results = [
        {
            "title": "No URL",
            "url": "",
        },
        {
            "title": "Valid",
            "url": "https://example.com/article",
        },
    ]

    unique = deduplicate_sources(results)

    assert len(unique) == 1
    assert unique[0]["title"] == "Valid"


def test_empty_input_returns_empty_list():
    assert deduplicate_sources([]) == []