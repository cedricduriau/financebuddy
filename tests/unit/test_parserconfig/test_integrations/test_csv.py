# package
from financebuddy.parserconfig.integrations.csv import CSVParserConfig, CSVParserConfigSettings


def test_init_config_settings():
    settings = CSVParserConfigSettings(
        field_map={},
    )
    assert settings.skip_rows == [0]
    assert settings.delimiter == ","
    assert settings.decimal == "."
    assert settings.field_map == {}
    assert settings.currency is None
    assert settings.date_format is None


def test_init_config():
    config = CSVParserConfig(
        path="",
        format="unknown",
        extension="unknown",
        settings={"field_map": {}},
    )
    assert config.type == "csv"
