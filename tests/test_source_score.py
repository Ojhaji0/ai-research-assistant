from tools.research import source_score


def test_edu_source_gets_quality_bonus():
    result = {
        "url": "https://example.edu/research",
        "score": 0.8,
    }

    assert source_score(result) == 3.8


def test_gov_source_gets_quality_bonus():
    result = {
        "url": "https://example.gov/research",
        "score": 0.8,
    }

    assert source_score(result) == 3.8


def test_authoritative_tech_source_gets_bonus():
    result = {
        "url": "https://www.microsoft.com/research",
        "score": 0.8,
    }

    assert source_score(result) == 2.8


def test_medium_source_gets_penalty():
    result = {
        "url": "https://medium.com/example-article",
        "score": 0.8,
    }

    assert source_score(result) == -0.2


def test_linkedin_source_gets_penalty():
    result = {
        "url": "https://linkedin.com/posts/example",
        "score": 0.8,
    }

    assert source_score(result) == -0.2


def test_normal_source_keeps_base_score():
    result = {
        "url": "https://example.com/research",
        "score": 0.8,
    }

    assert source_score(result) == 0.8


def test_missing_score_defaults_to_zero():
    result = {
        "url": "https://example.com/research",
    }

    assert source_score(result) == 0


def test_edu_in_path_does_not_get_edu_bonus():
    result = {
        "url": "https://example.com/articles/.edu/research",
        "score": 0.8,
    }

    assert source_score(result) == 0.8


def test_www_trusted_domain_gets_bonus():
    result = {
        "url": "https://www.openai.com/research",
        "score": 0.8,
    }

    assert source_score(result) == 2.8