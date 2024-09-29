# package
from financebuddy.parserconfig.models import ParserExtension


def test_missing():
    assert ParserExtension("?") == ParserExtension.UNKNOWN
