from pydantic import BaseModel

from financebuddy.exporterconfig.models import (
    CSVExporterSettings,
    ExporterConfig,
    ExporterConfigSettings,
    ExporterExtension,
    ExporterFormat,
    JSONExporterSettings,
)
from financebuddy.report.models import ReportTransaction


class ExportTransaction(ReportTransaction):
    pass


class ExportReport(BaseModel):
    transactions: list[ExportTransaction]


__all__ = [
    "ExporterConfig",
    "ExporterConfigSettings",
    "ExporterExtension",
    "ExporterFormat",
    "CSVExporterSettings",
    "JSONExporterSettings",
    "ExportTransaction",
    "ExportReport",
]
