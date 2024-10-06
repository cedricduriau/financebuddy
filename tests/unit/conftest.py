# stdlib
import os

# package
import financebuddy_parsers

# third party
import pytest


@pytest.fixture
def fix_dir_data() -> str:
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(current_dir, "..", "data"))
    return data_dir


@pytest.fixture
def fix_financebuddy_parsers_dir_configs(fix_dir_data) -> str:
    dir_config = os.path.join(fix_dir_data, "configs")
    return dir_config


@pytest.fixture
def mock_financebuddy_parsers_dir_configs(fix_financebuddy_parsers_dir_configs, monkeypatch):
    monkeypatch.setattr(financebuddy_parsers, "DIR_CONFIGS", fix_financebuddy_parsers_dir_configs)
