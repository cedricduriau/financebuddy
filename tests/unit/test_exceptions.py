# third party
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException


def test_init():
    with pytest.raises(FinanceBuddyException):
        raise FinanceBuddyException("hjelp")
