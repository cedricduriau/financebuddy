# stdlib
import csv
import datetime
import json
import os
import tempfile
from typing import Any

# package
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.models import ExporterExtension, ExporterFormat, ExportReport


class FinanceBuddyCSVExporter(Exporter):
    format: ExporterFormat = ExporterFormat.FINANCEBUDDY
    extension: ExporterExtension = ExporterExtension.CSV

    def dump_report(self, export_report: ExportReport) -> str:
        directory = tempfile.gettempdir()
        timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
        filename = f"financebuddy_export_{timestamp}.csv"
        path = os.path.join(directory, filename)

        raw_report: dict = json.loads(export_report.model_dump_json())
        raw_transactions: list[dict[str, Any]] = raw_report.get("transactions", [dict()])
        headers = list(raw_transactions[0].keys())

        with open(path, "w") as fp:
            writer = csv.DictWriter(fp, headers)
            writer.writeheader()
            writer.writerows(raw_transactions)

        return path
