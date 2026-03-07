from financebuddy.export import factory
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExporterConfig
from financebuddy.logging import get_logger
from financebuddy.report.models import Report

logger = get_logger(__name__)


def get_exporters() -> list[type[Exporter]]:
    return factory.get_exporters()


def export_report(report: Report, config: ExporterConfig) -> str:
    logger.debug(f"Exporting report: format={config.format}, extension={config.extension}")
    exporter = factory.get_exporter(config)
    path = exporter.export_report(report)
    logger.info(f"Report exported to: {path}")
    return path
