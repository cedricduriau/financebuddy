import datetime
import os
import tempfile
from abc import ABC, abstractmethod

from financebuddy.export.models import ExporterConfig, ExportReport, ExportTransaction
from financebuddy.report.models import Report


class Exporter(ABC):
    def __init__(self, config: ExporterConfig) -> None:
        self.config = config

    @staticmethod
    def report_to_export_report(report: Report) -> ExportReport:
        export_transactions: list[ExportTransaction] = []
        for item in report.items:
            if transaction := item.transaction:
                export_transaction = ExportTransaction.model_validate(transaction.model_dump())
                export_transactions.append(export_transaction)
        export_report = ExportReport(transactions=export_transactions)
        return export_report

    def build_export_report_path(self) -> str:
        directory = tempfile.gettempdir()
        timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
        basename = f"financebuddy_export_{self.config.format}_{timestamp}.{self.config.extension}"
        path = os.path.join(directory, basename)
        return path

    @abstractmethod
    def dump_report(self, export_report: ExportReport) -> str:
        pass

    def export_report(self, report: Report) -> str:
        export_report = self.report_to_export_report(report)
        path = self.dump_report(export_report)
        return path
