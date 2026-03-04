from financebuddy.exporterconfig.integrations.csv import CSVExporterConfig, CSVExporterSettings
from financebuddy.exporterconfig.integrations.json import JSONExporterConfig, JSONExporterSettings
from financebuddy.exporterconfig.models import ExporterExtension, ExporterFormat


def test_csv_exporter_config():
    config = CSVExporterConfig(
        format=ExporterFormat.FINANCEBUDDY,
        extension=ExporterExtension.CSV,
        settings=CSVExporterSettings(delimiter="|"),
    )
    assert config.format == ExporterFormat.FINANCEBUDDY
    assert config.extension == ExporterExtension.CSV
    assert config.settings.delimiter == "|"
    assert config.settings.lineterminator == "\n"


def test_csv_exporter_config_defaults():
    config = CSVExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.CSV)
    assert config.format == ExporterFormat.FINANCEBUDDY
    assert config.extension == ExporterExtension.CSV
    assert config.settings is None


def test_json_exporter_config():
    config = JSONExporterConfig(
        format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON, settings=JSONExporterSettings(indent=4)
    )
    assert config.format == ExporterFormat.FINANCEBUDDY
    assert config.extension == ExporterExtension.JSON
    assert config.settings.indent == 4


def test_json_exporter_config_defaults():
    config = JSONExporterConfig(format=ExporterFormat.FINANCEBUDDY, extension=ExporterExtension.JSON)
    assert config.format == ExporterFormat.FINANCEBUDDY
    assert config.extension == ExporterExtension.JSON
    assert config.settings is None
