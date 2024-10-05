# stdlib
import json

# package
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExporterExtension, ExporterFormat, ExportReport


class FinanceBuddyJSONExporter(Exporter):
    format: ExporterFormat = ExporterFormat.FINANCEBUDDY
    extension: ExporterExtension = ExporterExtension.JSON

    def dump_report(self, export_report: ExportReport) -> str:
        path = self.build_export_report_path()
        with open(path, "w") as fp:
            data = json.loads(export_report.model_dump_json())
            json.dump(data, fp, indent=4)
        return path
