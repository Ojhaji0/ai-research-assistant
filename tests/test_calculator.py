import pytest

from tools.calculator import calculate


def test_addition():
    assert calculate(10, "+", 5) == 15


def test_subtraction():
    assert calculate(10, "-", 5) == 5


def test_multiplication():
    assert calculate(10, "*", 5) == 50


def test_division():
    assert calculate(10, "/", 5) == 2


def test_float_calculation():
    assert calculate(5.5, "+", 2.5) == 8.0


def test_division_by_zero():
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        calculate(10, "/", 0)


def test_invalid_operator():
    with pytest.raises(
        ValueError,
        match="Unsupported operator",
    ):
        calculate(10, "^", 2)