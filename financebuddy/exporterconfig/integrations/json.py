from financebuddy.exporterconfig.models import ExporterConfig, JSONExporterSettings


class JSONExporterConfig(ExporterConfig):
    settings: JSONExporterSettings | None = None
