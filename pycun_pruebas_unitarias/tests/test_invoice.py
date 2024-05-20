import pytest
from pycun_pruebas_unitarias.apps.invoice.views import is_greater_than, sum


def test_sum():
    assert sum(2, 5) == 7


def test_is_greater_than():
    assert is_greater_than(10, 2)


@pytest.mark.parametrize(
    "input_x, input_y, expected",
    [
        (5, 1, 6),
        (6, sum(4, 2), 12),
        (sum(19, 1), 15, 35),
        (-7, 10, sum(-7, 10))
    ]
)
def test_sum_params(input_x, input_y, expected):
    assert sum(input_x, input_y) == expected

