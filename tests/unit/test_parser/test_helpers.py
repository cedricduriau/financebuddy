# third party
import pytest

# package
from financebuddy.parser import helpers


@pytest.mark.parametrize(
    ["inp", "out"],
    [
        # single digit
        ("0", "0"),
        ("1", "1"),
        # single decimal
        ("1,0", "1.0"),
        # multiple decimal
        ("1,00", "1.00"),
        # financial notation
        ("1,000.00", "1000.00"),
        ("1,000,000.00", "1000000.00"),
    ],
)
def test_fix_value_string(inp: str, out: str):
    assert helpers.fix_value_string(inp) == out


def test_hash_string():
    assert helpers.hash_string("0") == "cfcd208495d565ef66e7dff9f98764da"
