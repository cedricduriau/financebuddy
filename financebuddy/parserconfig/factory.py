# stdlib
from typing import Any

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parserconfig.integrations.csv import CSVParserConfig
from financebuddy.parserconfig.integrations.excel import ExcelParserConfig
from financebuddy.parserconfig.models import ParserConfig, ParserExtension

MAP_PARSER_CONFIGS_BY_EXT: dict[tuple[str | None, ParserExtension], type[ParserConfig]] = {
    (None, ParserExtension.CSV): CSVParserConfig,
    (None, ParserExtension.XLSX): ExcelParserConfig,
}


def get_parser_config_type(format: str | None, extension: ParserExtension) -> type[ParserConfig]:
    key = (format, extension)
    try:
        ParserConfigType = MAP_PARSER_CONFIGS_BY_EXT[key]
    except KeyError:
        msg = f"parser config not supported for format/extension: {format}/{extension}"
        raise FinanceBuddyException(msg)
    return ParserConfigType


def get_parser_config(
    path: str,
    format: str | None,
    extension: ParserExtension,
    raw_content: dict[str, Any],
) -> ParserConfig:
    ParserConfigType = get_parser_config_type(format, extension)
    parser_config = ParserConfigType(path=path, **raw_content)
    return parser_config
