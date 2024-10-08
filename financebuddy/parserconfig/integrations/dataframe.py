# package
from financebuddy.parserconfig.models import ParserConfig, ParserConfigSettings
from financebuddy.report.models import ReportTransactionField


class DataframeParserConfigSettings(ParserConfigSettings):
    field_map: dict[ReportTransactionField, int]
    date_format: str | None = None
    currency: str | None = None


class DataframeParserConfig(ParserConfig):
    settings: DataframeParserConfigSettings
