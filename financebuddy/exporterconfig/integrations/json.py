from financebuddy.exporterconfig.models import ExporterConfig, ExporterConfigSettings


class JSONExporterSettings(ExporterConfigSettings):
    indent: int | None = 2


class JSONExporterConfig(ExporterConfig):
    settings: JSONExporterSettings | None = None
