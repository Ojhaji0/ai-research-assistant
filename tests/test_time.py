from datetime import datetime

from tools.time import get_current_time


def test_get_current_time_returns_string():
    result = get_current_time()

    assert isinstance(result, str)
    assert result


def test_get_current_time_format():
    result = get_current_time()

    parsed = datetime.strptime(
        result,
        "%Y-%m-%d %H:%M:%S",
    )

    assert isinstance(parsed, datetime)