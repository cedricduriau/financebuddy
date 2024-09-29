# package
from financebuddy.export import factory
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExporterExtension, ExporterFormat
from financebuddy.report.models import Report


def get_exporters() -> list[type[Exporter]]:
    return factory.get_exporters()


def export_report(report: Report, format: ExporterFormat, extension: ExporterExtension) -> str:
    exporter = factory.get_exporter(format, extension)
    path = exporter.export_report(report)
    return path
