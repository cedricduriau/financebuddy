# package
from financebuddy.parser import factory
from financebuddy.parserconfig.models import ParserConfig
from financebuddy.report.models import Report


def generate_report(path: str, config: ParserConfig) -> Report:
    parser = factory.get_parser(config)
    report = parser.generate_report(path)
    return report
