# package
from financebuddy.parserconfig.integrations.csv import CSVParserConfig, CSVParserConfigSettings


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
        extension="unknown",
        settings={"field_map": {}},
    )
    assert config.type == "csv"
