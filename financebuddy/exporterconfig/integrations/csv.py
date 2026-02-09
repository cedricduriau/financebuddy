from financebuddy.exporterconfig.models import ExporterConfig, ExporterConfigSettings


class CSVExporterSettings(ExporterConfigSettings):
    delimiter: str = ","
    lineterminator: str = "\n"


class CSVExporterConfig(ExporterConfig):
    settings: CSVExporterSettings | None = None
