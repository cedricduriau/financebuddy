from abc import ABC, abstractmethod

from financebuddy.parserconfig.models import ParserConfig, ParserExtension
from financebuddy.report.models import Report


class Parser(ABC):
    extension: ParserExtension = ParserExtension.UNKNOWN

    def __init__(self, config: ParserConfig) -> None:
        self.config = config

    @abstractmethod
    def generate_report(self, path: str) -> Report:
        pass
