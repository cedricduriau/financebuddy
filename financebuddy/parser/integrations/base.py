# package
from financebuddy.parserconfig.models import ParserConfig, ParserExtension
from financebuddy.report.models import Report


class Parser:
    extension: ParserExtension = ParserExtension.UNKNOWN

    def __init__(self, config: ParserConfig) -> None:
        self.config = config

    def generate_report(self, path: str) -> Report:
        raise NotImplementedError()
