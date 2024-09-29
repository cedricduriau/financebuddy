# stdlib

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


def test_dump_report():
    exporter = Exporter()
    with pytest.raises(NotImplementedError):
        exporter.dump_report(object())
