# third party
import pandas as pd

# package
from financebuddy.parser.integrations.dataframe import DataframeParser
from financebuddy.parserconfig.integrations.csv import CSVParserConfig
from financebuddy.parserconfig.models import ParserExtension


class CSVParser(DataframeParser):
    extension: ParserExtension = ParserExtension.CSV

    def __init__(self, config: CSVParserConfig) -> None:
        super().__init__(config)
        self.config = config

    def read_file(self, path: str) -> pd.DataFrame:
        df = pd.read_csv(path, sep=self.config.settings.delimiter)
        return df
