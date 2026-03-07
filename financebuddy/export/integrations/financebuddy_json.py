import json

from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExportReport
from financebuddy.exporterconfig.integrations.json import JSONExporterSettings


class FinanceBuddyJSONExporter(Exporter):
    def dump_report(self, export_report: ExportReport) -> str:
        path = self.build_export_report_path()
        settings = self.config.settings or JSONExporterSettings()

        with open(path, "w") as fp:
            data = json.loads(export_report.model_dump_json())
            json.dump(data, fp, indent=settings.indent)
        return path
