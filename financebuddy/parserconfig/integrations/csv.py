# package
from financebuddy.parserconfig.models import ParserConfig, ParserConfigSettings, ParserExtension
from financebuddy.report.models import ReportTransactionField


class CSVParserConfigSettings(ParserConfigSettings):
    skip_rows: list[int] = [0]
    delimiter: str = ","
    decimal: str = "."
    field_map: dict[ReportTransactionField, int]
    currency: str | None = None
    date_format: str | None = None


class CSVParserConfig(ParserConfig):
    type: ParserExtension = ParserExtension.CSV
    settings: CSVParserConfigSettings
