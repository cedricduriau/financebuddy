# package
from financebuddy.parserconfig.integrations.csv import CSVParserConfig, CSVParserConfigSettings
from financebuddy.parserconfig.models import ParserExtension


def test_init_config_settings():
    settings = CSVParserConfigSettings(
        field_map={},
    )
    assert settings.field_map == {}
    assert settings.date_format is None
    assert settings.currency is None
    assert settings.delimiter == ","


def test_init_config():
    config = CSVParserConfig(
        path="",
        format="unknown",
        extension=ParserExtension.UNKNOWN,
        settings=CSVParserConfigSettings(field_map={}),
    )
    assert config.type == "csv"
