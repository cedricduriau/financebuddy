# third party
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parserconfig import factory
from financebuddy.parserconfig.integrations.csv import CSVParserConfig
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


@pytest.mark.parametrize(
    ["format", "extension", "ParserConfigType"],
    [
        (None, ParserExtension.CSV, CSVParserConfig),
    ],
)
def test_get_parser_config_type(
    format: str | None,
    extension: ParserExtension,
    ParserConfigType: type[ParserConfig],
):
    assert factory.get_parser_config_type(format, extension) == ParserConfigType


def test_get_parser_config_type_raise_FinanceBuddyException():
    with pytest.raises(FinanceBuddyException):
        factory.get_parser_config_type("?", "?")


def test_get_parser_config():
    config = factory.get_parser_config(
        "/tmp/foo.json",
        None,
        ParserExtension.CSV,
        raw_content={
            "format": "foo",
            "extension": "csv",
            "settings": {"field_map": {}},
        },
    )
    assert isinstance(config, CSVParserConfig)
