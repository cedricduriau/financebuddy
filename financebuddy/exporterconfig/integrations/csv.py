from financebuddy.exporterconfig.models import CSVExporterSettings, ExporterConfig


class CSVExporterConfig(ExporterConfig):
    settings: CSVExporterSettings | None = None
