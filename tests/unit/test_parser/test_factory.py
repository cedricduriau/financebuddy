# third party
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parser import factory
from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.csv import CSVParser
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


@pytest.mark.parametrize(
    ["extension", "ParserType"],
    [
        (ParserExtension.CSV, CSVParser),
    ],
)
def test_get_parser_type(
    extension: ParserExtension,
    ParserType: type[Parser],
):
    assert factory.get_parser_type(extension) == ParserType


def test_get_parser_type_raise_FinanceBuddyException():
    with pytest.raises(FinanceBuddyException):
        factory.get_parser_type("?")


def test_get_parser(fix_parser_config: ParserConfig):
    fix_parser_config.extension = ParserExtension.CSV
    parser = factory.get_parser(fix_parser_config)
    assert isinstance(parser, CSVParser)
