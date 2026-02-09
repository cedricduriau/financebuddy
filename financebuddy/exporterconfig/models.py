from enum import StrEnum

from pydantic import BaseModel

from financebuddy.report.models import ReportTransaction


class ExporterFormat(StrEnum):
    UNKNOWN = "unknown"
    FINANCEBUDDY = "financebuddy"


class ExporterExtension(StrEnum):
    UNKNOWN = "unknown"
    JSON = "json"
    CSV = "csv"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ExporterConfigSettings(BaseModel):
    pass


class JSONExporterSettings(ExporterConfigSettings):
    indent: int | None = 2


class CSVExporterSettings(ExporterConfigSettings):
    delimiter: str = ","
    lineterminator: str = "\n"


class ExporterConfig(BaseModel):
    format: ExporterFormat
    extension: ExporterExtension
    settings: ExporterConfigSettings | None = None


class ExportTransaction(ReportTransaction):
    pass


class ExportReport(BaseModel):
    transactions: list[ExportTransaction]
