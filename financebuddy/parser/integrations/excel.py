# stdlib
import warnings

# third party
import pandas as pd

# package
from financebuddy.parser.integrations.dataframe import DataframeParser
from financebuddy.parserconfig.integrations.excel import ExcelParserConfig
from financebuddy.parserconfig.models import ParserExtension


class ExcelParser(DataframeParser):
    extension: ParserExtension = ParserExtension.XLSX

    def __init__(self, config: ExcelParserConfig) -> None:
        super().__init__(config)
        self.config = config

    def read_file(self, path: str) -> pd.DataFrame:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.read_excel(path, engine="openpyxl")
        return df
