import datetime
import os
import tempfile

from financebuddy.export.integrations.financebuddy_json import FinanceBuddyJSONExporter
from financebuddy.export.models import ExporterConfig, ExporterExtension, ExporterFormat
from financebuddy.report.models import Report


def test_init():
    config = ExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON)
    exporter = FinanceBuddyJSONExporter(config)
    assert exporter.config == config


def test_report_to_export_report(fix_report: Report):
    export_report = FinanceBuddyJSONExporter.report_to_export_report(fix_report)
    assert len(export_report.transactions) == 1


def test_build_export_report_path(freezer, tmpdir, monkeypatch):
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(tmpdir))
    datetime_str = "1970-01-01T00:00:00.000Z"
    freezer.move_to(datetime_str)
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

    config = ExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON)
    exporter = FinanceBuddyJSONExporter(config)
    path = exporter.build_export_report_path()
    dirname, basename = os.path.split(path)
    assert dirname == str(tmpdir)
    assert basename == f"financebuddy_export_financebuddy_{timestamp}.json"


def test_dump_report():
    config = ExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON)
    exporter = FinanceBuddyJSONExporter(config)
    # Verify it has the method
    assert hasattr(exporter, "dump_report")
    assert callable(exporter.dump_report)
