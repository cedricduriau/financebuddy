# package
from financebuddy.parserconfig.integrations.dataframe import DataframeParserConfig, DataframeParserConfigSettings
from financebuddy.parserconfig.models import ParserExtension


class CSVParserConfigSettings(DataframeParserConfigSettings):
    delimiter: str | None = ","


class CSVParserConfig(DataframeParserConfig):
    type: ParserExtension = ParserExtension.CSV
    settings: CSVParserConfigSettings
