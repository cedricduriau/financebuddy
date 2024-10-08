# package
from financebuddy.parserconfig.integrations.dataframe import DataframeParserConfig, DataframeParserConfigSettings
from financebuddy.parserconfig.models import ParserExtension


class ExcelParserConfigSettings(DataframeParserConfigSettings):
    pass


class ExcelParserConfig(DataframeParserConfig):
    type: ParserExtension = ParserExtension.XLSX
    settings: ExcelParserConfigSettings
