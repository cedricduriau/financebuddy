from financebuddy.logging import get_logger
from financebuddy.parser import factory
from financebuddy.parser.integrations.base import Parser
from financebuddy.parserconfig.models import ParserConfig
from financebuddy.report.models import Report

logger = get_logger(__name__)


def get_parsers() -> list[type[Parser]]:
    return factory.get_parsers()


def generate_report(path: str, config: ParserConfig) -> Report:
    logger.debug(f"Starting report generation: path={path}, format={config.format}")
    parser = factory.get_parser(config)
    report = parser.generate_report(path)
    logger.info(
        f"Report generated: total={report.summary.total}, parsed={report.summary.parsed}, "
        f"failed={report.summary.failed}"
    )
    return report
