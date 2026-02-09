from financebuddy.exceptions import UnsupportedFormatError
from financebuddy.logging import get_logger
from financebuddy.parser.integrations.base import Parser
from financebuddy.parser.integrations.csv import CSVParser
from financebuddy.parser.integrations.excel import ExcelParser
from financebuddy.parserconfig.models import ParserConfig, ParserExtension

logger = get_logger(__name__)

MAP_PARSER_BY_EXT: dict[ParserExtension, type[Parser]] = {
    ParserExtension.CSV: CSVParser,
    ParserExtension.XLSX: ExcelParser,
}


def get_parser_type(extension: ParserExtension) -> type[Parser]:
    logger.debug(f"Looking up parser for extension: {extension}")
    try:
        ParserType = MAP_PARSER_BY_EXT[extension]
    except KeyError:
        logger.error(f"No parser found for extension: {extension}")
        raise UnsupportedFormatError(f"no parser found for extension: {extension}")
    logger.debug(f"Found parser: {ParserType.__name__}")
    return ParserType


def get_parser(config: ParserConfig) -> Parser:
    ParserType = get_parser_type(config.extension)
    parser = ParserType(config)
    return parser


def get_parsers() -> list[type[Parser]]:
    parser_types = list(MAP_PARSER_BY_EXT.values())
    return parser_types
