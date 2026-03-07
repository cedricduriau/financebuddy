from typing import Any

from financebuddy.exceptions import UnsupportedFormatError
from financebuddy.exporterconfig.integrations.csv import CSVExporterConfig
from financebuddy.exporterconfig.integrations.json import JSONExporterConfig
from financebuddy.exporterconfig.models import ExporterConfig, ExporterExtension

MAP_EXPORTER_CONFIGS_BY_EXT: dict[tuple[str, ExporterExtension], type[ExporterConfig]] = {
    ("financebuddy", ExporterExtension.CSV): CSVExporterConfig,
    ("financebuddy", ExporterExtension.JSON): JSONExporterConfig,
}


def get_exporter_config_type(format: str, extension: ExporterExtension) -> type[ExporterConfig]:
    key = (format, extension)
    try:
        ExporterConfigType = MAP_EXPORTER_CONFIGS_BY_EXT[key]
    except KeyError:
        msg = f"exporter config not supported for format/extension: {format}/{extension}"
        raise UnsupportedFormatError(msg)
    return ExporterConfigType


def get_exporter_config(
    format: str,
    extension: ExporterExtension,
    raw_content: dict[str, Any],
) -> ExporterConfig:
    ExporterConfigType = get_exporter_config_type(format, extension)
    exporter_config = ExporterConfigType(**raw_content)
    return exporter_config
