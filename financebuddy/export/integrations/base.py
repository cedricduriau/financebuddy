# package
from financebuddy.export.models import ExporterExtension, ExporterFormat, ExportReport, ExportTransaction
from financebuddy.report.models import Report


class Exporter:
    format: ExporterFormat = ExporterFormat.UNKNOWN
    extension: ExporterExtension = ExporterExtension.UNKNOWN

    @staticmethod
    def report_to_export_report(report: Report) -> ExportReport:
        export_transactions: list[ExportTransaction] = []
        for item in report.items:
            if model := item.model:
                export_transaction = ExportTransaction.model_validate(model.model_dump())
                export_transactions.append(export_transaction)
        export_report = ExportReport(transactions=export_transactions)
        return export_report

    def dump_report(self, export_report: ExportReport) -> str:
        raise NotImplementedError()

    def export_report(self, report: Report) -> str:
        export_report = self.report_to_export_report(report)
        path = self.dump_report(export_report)
        return path
