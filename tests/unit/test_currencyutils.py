# third party
import pytest

# package
from financebuddy import currencyutils


def test_validate_currency():
    assert currencyutils.validate_currency("eur") == "EUR"


def test_validate_currency_raise():
    with pytest.raises(ValueError):
        currencyutils.validate_currency("???")


@pytest.mark.parametrize(
    ["currency", "expected"],
    [
        ["EUR", 2],
        ["KWD", 3],
        ["YER", 0],
    ],
)
def test_get_currency_precision(currency: str, expected: int):
    assert currencyutils.get_currency_precision(currency) == expected


def test_calculate_smallest_value():
    assert currencyutils.calculate_smallest_value(10, "EUR") == 1000


def test_calculate_currency_value():
    assert currencyutils.calculate_currency_value(1000, "EUR") == 10.00


def test_format_value():
    assert currencyutils.format_value(1000, "EUR") == "10.00"


def test_list_currencies():
    assert len(currencyutils.list_currencies()) > 1
