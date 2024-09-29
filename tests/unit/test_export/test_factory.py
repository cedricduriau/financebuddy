# third party
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.export import factory
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.integrations.financebuddy_csv import FinanceBuddyCSVExporter
from financebuddy.export.integrations.financebuddy_json import FinanceBuddyJSONExporter
from financebuddy.export.models import ExporterExtension, ExporterFormat


@pytest.mark.parametrize(
    ["format", "extension", "ExporterType"],
    [
        (ExporterFormat.FINANCEBUDDY, ExporterExtension.JSON, FinanceBuddyJSONExporter),
        (ExporterFormat.FINANCEBUDDY, ExporterExtension.CSV, FinanceBuddyCSVExporter),
    ],
)
def test_get_exporter_type(
    format: ExporterFormat,
    extension: ExporterExtension,
    ExporterType: type[Exporter],
):
    assert factory.get_exporter_type(format, extension) == ExporterType


def test_get_exporter_type_raise_FinanceBuddyException():
    with pytest.raises(FinanceBuddyException):
        factory.get_exporter_type("?", "?")


def test_get_exporter():
    exporter = factory.get_exporter(ExporterFormat.FINANCEBUDDY, ExporterExtension.JSON)
    assert isinstance(exporter, FinanceBuddyJSONExporter)


def test_get_exporters():
    assert len(factory.get_exporters()) == 2
