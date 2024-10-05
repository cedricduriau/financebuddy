# stdlib
import datetime
import os
import tempfile

# third party
import pytest

# package
from financebuddy.export.integrations.base import Exporter
from financebuddy.report.models import Report


def test_init():
    assert Exporter.format == "unknown"
    assert Exporter.extension == "unknown"
    Exporter()


def test_report_to_export_report(fix_report: Report):
    export_report = Exporter.report_to_export_report(fix_report)
    assert len(export_report.transactions) == 1


def test_build_export_report_path(freezer, tmpdir, monkeypatch):
    monkeypatch.setattr(tempfile, "gettempdir", lambda: str(tmpdir))
    datetime_str = "1970-01-01T00:00:00.000Z"
    freezer.move_to(datetime_str)
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

    exported = Exporter()
    path = exported.build_export_report_path()
    dirname, basename = os.path.split(path)
    assert dirname == str(tmpdir)
    assert basename == f"financebuddy_export_unknown_{timestamp}.unknown"


def test_dump_report():
    exporter = Exporter()
    with pytest.raises(NotImplementedError):
        exporter.dump_report(object())
