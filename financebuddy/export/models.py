from pydantic import BaseModel

from financebuddy.exporterconfig.models import (
    ExporterConfig,
    ExporterConfigSettings,
    ExporterExtension,
    ExporterFormat,
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
    "ExportTransaction",
    "ExportReport",
]
