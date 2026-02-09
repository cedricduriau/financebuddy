from financebuddy.exceptions import UnsupportedFormatError
from financebuddy.export.integrations.base import Exporter
from financebuddy.export.integrations.financebuddy_csv import FinanceBuddyCSVExporter
from financebuddy.export.integrations.financebuddy_json import FinanceBuddyJSONExporter
from financebuddy.export.models import ExporterConfig, ExporterExtension, ExporterFormat
from financebuddy.logging import get_logger

logger = get_logger(__name__)

EXPORTERS = {
    (ExporterFormat.FINANCEBUDDY, ExporterExtension.CSV): FinanceBuddyCSVExporter,
    (ExporterFormat.FINANCEBUDDY, ExporterExtension.JSON): FinanceBuddyJSONExporter,
}


def get_exporter_type(config: ExporterConfig) -> type[Exporter]:
    key = (config.format, config.extension)
    logger.debug(f"Looking up exporter for: {config.format}/{config.extension}")
    try:
        ExporterType = EXPORTERS[key]
    except KeyError:
        msg = f"no exporter found for format/extension: {config.format}/{config.extension}"
        logger.error(msg)
        raise UnsupportedFormatError(msg)
    logger.debug(f"Found exporter: {ExporterType.__name__}")
    return ExporterType


def get_exporter(config: ExporterConfig) -> Exporter:
    ExporterType = get_exporter_type(config)
    exporter = ExporterType(config)
    return exporter


def get_exporters() -> list[type[Exporter]]:
    exporter_types = list(EXPORTERS.values())
    return exporter_types
