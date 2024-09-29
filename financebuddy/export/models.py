# stdlib
from enum import StrEnum

# third party
from pydantic import BaseModel

# package
from financebuddy.report.models import ReportTransaction


class ExporterFormat(StrEnum):
    UNKNOWN = "unknown"
    FINANCEBUDDY = "financebuddy"


class ExporterExtension(StrEnum):
    UNKNOWN = "unknown"
    JSON = "json"
    CSV = "csv"


class ExportTransaction(ReportTransaction):
    pass


class ExportReport(BaseModel):
    transactions: list[ExportTransaction]
