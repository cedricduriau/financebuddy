import pytest

from financebuddy.exceptions import UnsupportedFormatError
from financebuddy.exporterconfig.factory import get_exporter_config, get_exporter_config_type
from financebuddy.exporterconfig.integrations.csv import CSVExporterConfig
from financebuddy.exporterconfig.integrations.json import JSONExporterConfig
from financebuddy.exporterconfig.models import ExporterExtension


def test_get_exporter_config_type_csv():
    config_type = get_exporter_config_type("financebuddy", ExporterExtension.CSV)
    assert config_type == CSVExporterConfig


def test_get_exporter_config_type_json():
    config_type = get_exporter_config_type("financebuddy", ExporterExtension.JSON)
    assert config_type == JSONExporterConfig


def test_get_exporter_config_type_raise_unsupported():
    with pytest.raises(UnsupportedFormatError):
        get_exporter_config_type("unknown", ExporterExtension.CSV)


def test_get_exporter_config():
    raw_content = {
        "format": "financebuddy",
        "extension": "csv",
        "settings": {"delimiter": "\t", "lineterminator": "\r\n"},
    }
    config = get_exporter_config("financebuddy", ExporterExtension.CSV, raw_content)
    assert isinstance(config, CSVExporterConfig)
    assert config.format == "financebuddy"
    assert config.extension == ExporterExtension.CSV
    assert config.settings.delimiter == "\t"
    assert config.settings.lineterminator == "\r\n"


def test_get_exporter_config_with_defaults():
    raw_content = {"format": "financebuddy", "extension": "json"}
    config = get_exporter_config("financebuddy", ExporterExtension.JSON, raw_content)
    assert isinstance(config, JSONExporterConfig)
    assert config.settings is None
