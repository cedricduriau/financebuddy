import pytest

from financebuddy.exceptions import UnsupportedFormatError
from financebuddy.export import factory
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.integrations.financebuddy_csv import FinanceBuddyCSVExporter
from financebuddy.export.integrations.financebuddy_json import FinanceBuddyJSONExporter
from financebuddy.export.models import ExporterConfig, ExporterExtension, ExporterFormat


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
    config = ExporterConfig(format=format, extension=extension)
    assert factory.get_exporter_type(config) == ExporterType


def test_get_exporter_type_raise_UnsupportedFormatError():
    with pytest.raises(UnsupportedFormatError):
        config = ExporterConfig(format=ExporterFormat.UNKNOWN, extension=ExporterExtension.UNKNOWN)
        factory.get_exporter_type(config)


def test_get_exporter():
    config = ExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON)
    exporter = factory.get_exporter(config)
    assert isinstance(exporter, FinanceBuddyJSONExporter)


def test_get_exporters():
    assert len(factory.get_exporters()) == 2
