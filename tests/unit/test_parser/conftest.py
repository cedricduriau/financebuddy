# third party
import pytest

# package
from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.dataframe import DataframeParser
from financebuddy.parserconfig.integrations.dataframe import DataframeParserConfig, DataframeParserConfigSettings
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


@pytest.fixture
def fix_parser_config() -> ParserConfig:
    config = ParserConfig(
        path="/tmp/foo.json",
        format="foo",
        extension=ParserExtension.UNKNOWN,
    )
    return config


@pytest.fixture
def fix_parser(fix_parser_config: ParserConfig) -> Parser:
    parser = Parser(fix_parser_config)
    return parser


@pytest.fixture
def fix_parser_config_dataframe() -> DataframeParserConfig:
    config = DataframeParserConfig(
        path="/tmp/foo.json",
        format="foo",
        extension=ParserExtension.UNKNOWN,
        settings=DataframeParserConfigSettings(field_map={}),
    )
    return config


@pytest.fixture
def fix_parser_dataframe(fix_parser_config_dataframe: DataframeParserConfig) -> DataframeParser:
    parser = DataframeParser(fix_parser_config_dataframe)
    return parser
