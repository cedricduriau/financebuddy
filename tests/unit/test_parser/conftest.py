# third party
import pytest

# package
from financebuddy.parser.integrations.base import Parser
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
