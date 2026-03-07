import pytest

from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.csv import CSVParser
from financebuddy.parserconfig.integrations.dataframe import DataframeParserConfig, DataframeParserConfigSettings
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


@pytest.fixture
def fix_parser_config() -> ParserConfig:
    config = ParserConfig(
        path="/tmp/foo.json",
        format="foo",
        extension=ParserExtension.CSV,
    )
    return config


@pytest.fixture
def fix_parser(fix_parser_config: ParserConfig) -> Parser:
    parser = CSVParser(fix_parser_config)
    return parser


@pytest.fixture
def fix_parser_config_dataframe() -> DataframeParserConfig:
    config = DataframeParserConfig(
        path="/tmp/foo.json",
        format="foo",
        extension=ParserExtension.CSV,
        settings=DataframeParserConfigSettings(field_map={}),
    )
    return config


@pytest.fixture
def fix_parser_dataframe(fix_parser_config_dataframe: DataframeParserConfig):
    parser = CSVParser(fix_parser_config_dataframe)
    return parser
