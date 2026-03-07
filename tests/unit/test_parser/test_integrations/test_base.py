from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.csv import CSVParser
from financebuddy.parserconfig.models import ParserConfig


def test_init(fix_parser_config: ParserConfig):
    fix_parser_config.extension = "csv"
    parser = CSVParser(fix_parser_config)
    assert parser.config.format == "foo"
    assert parser.config.extension == "csv"


def test_generate_report(fix_parser: Parser):
    # fix_parser is now a concrete implementation
    # Just verify it has the method
    assert hasattr(fix_parser, "generate_report")
    assert callable(fix_parser.generate_report)
