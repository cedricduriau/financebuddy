# stdlib
import os

# third party
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parserconfig import api


@pytest.mark.parametrize(
    ["basename", "format", "extension"],
    [
        ("parser_foo_csv_config.json", "foo", "csv"),
    ],
)
def test_load_parser_config(
    basename: str,
    format: str,
    extension: str,
    fix_financebuddy_parsers_dir_configs: str,
):
    path = os.path.join(fix_financebuddy_parsers_dir_configs, basename)
    config = api.load_parser_config(path)
    assert config.format == format
    assert config.extension == extension


def test_load_parser_config_fail_path_does_not_exist():
    with pytest.raises(FinanceBuddyException):
        api.load_parser_config("")


@pytest.mark.parametrize(
    "basename",
    [
        "not_a_json.txt",
        "missing_extension.json",
        "invalid_extension.json",
    ],
)
def test_load_parser_config_fail(
    basename: str,
    fix_financebuddy_parsers_dir_configs: str,
    mock_financebuddy_parsers_dir_configs: None,
):
    path = os.path.join(fix_financebuddy_parsers_dir_configs, basename)
    with pytest.raises(FinanceBuddyException):
        api.load_parser_config(path)


def test_build_path(
    fix_financebuddy_parsers_dir_configs: str,
    mock_financebuddy_parsers_dir_configs: None,
):
    path = api.build_path("unknown", "unknown")
    dirname, basename = os.path.split(path)
    assert dirname == fix_financebuddy_parsers_dir_configs
    assert basename == "parser_unknown_unknown_config.json"


def test_find_parser_config(mock_financebuddy_parsers_dir_configs: None):
    config = api.find_parser_config("foo", "csv")
    assert config.format == "foo"
    assert config.extension == "csv"


def test_find_parser_config_fail():
    with pytest.raises(FinanceBuddyException):
        api.find_parser_config("?", "?")
