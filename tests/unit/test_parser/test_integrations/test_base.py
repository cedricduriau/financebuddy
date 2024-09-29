# third party
import pytest

# package
from financebuddy.parser.integrations.base import Parser
from financebuddy.parserconfig.models import ParserConfig


def test_init(fix_parser_config: ParserConfig):
    Parser.extension == "unknown"
    parser = Parser(fix_parser_config)
    assert parser.config.format == "foo"
    assert parser.config.extension == "unknown"


def test_generate_report(fix_parser: Parser):
    with pytest.raises(NotImplementedError):
        fix_parser.generate_report("/tmp/foo.csv")
