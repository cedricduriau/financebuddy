# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.csv import CSVParser
from financebuddy.parser.integrations.excel import ExcelParser
from financebuddy.parserconfig.models import ParserConfig, ParserExtension

MAP_PARSER_BY_EXT: dict[ParserExtension, type[Parser]] = {
    ParserExtension.CSV: CSVParser,
    ParserExtension.XLSX: ExcelParser,
}


def get_parser_type(extension: ParserExtension) -> type[Parser]:
    try:
        ParserType = MAP_PARSER_BY_EXT[extension]
    except KeyError:
        raise FinanceBuddyException(f"no parser found for extension: {extension}")
    return ParserType


def get_parser(config: ParserConfig) -> Parser:
    ParserType = get_parser_type(config.extension)
    parser = ParserType(config)
    return parser
