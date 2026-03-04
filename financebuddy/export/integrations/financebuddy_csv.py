import csv
import json
from typing import Any

from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExportReport
from financebuddy.exporterconfig.integrations.csv import CSVExporterSettings


class FinanceBuddyCSVExporter(Exporter):
    def dump_report(self, export_report: ExportReport) -> str:
        path = self.build_export_report_path()
        settings = self.config.settings or CSVExporterSettings()

        raw_report: dict = json.loads(export_report.model_dump_json())
        raw_transactions: list[dict[str, Any]] = raw_report.get("transactions", [dict()])
        headers = list(raw_transactions[0].keys())

        with open(path, "w", newline="") as fp:
            writer = csv.DictWriter(
                fp,
                headers,
                delimiter=settings.delimiter,
                lineterminator=settings.lineterminator,
            )
            writer.writeheader()
            writer.writerows(raw_transactions)

        return path
