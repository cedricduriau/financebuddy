# stdlib
from copy import deepcopy

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.integrations.financebuddy_csv import FinanceBuddyCSVExporter
from financebuddy.export.integrations.financebuddy_json import FinanceBuddyJSONExporter
from financebuddy.export.models import ExporterExtension, ExporterFormat

EXPORTERS = {
    (ExporterFormat.FINANCEBUDDY, ExporterExtension.CSV): FinanceBuddyCSVExporter,
    (ExporterFormat.FINANCEBUDDY, ExporterExtension.JSON): FinanceBuddyJSONExporter,
}


def get_exporter_type(format: ExporterFormat, extension: ExporterExtension) -> type[Exporter]:
    key = (format, extension)
    try:
        ExporterType = EXPORTERS[key]
    except KeyError:
        msg = f"no exporter found for format/extension: {format}/{extension}"
        raise FinanceBuddyException(msg)
    return ExporterType


def get_exporter(format: ExporterFormat, extension: ExporterExtension) -> Exporter:
    ExporterType = get_exporter_type(format, extension)
    exporter = ExporterType()
    return exporter


def get_exporters() -> list[type[Exporter]]:
    exporter_types = list(EXPORTERS.values())
    return deepcopy(exporter_types)
