import json
import os
import tempfile

import pytest

from financebuddy.exceptions import ConfigurationError, UnsupportedFormatError
from financebuddy.exporterconfig.api import (
    find_exporter_config,
    get_exporter_configs,
    load_exporter_config,
)
from financebuddy.exporterconfig.models import ExporterExtension


def test_load_exporter_config():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fp:
        config_data = {
            "format": "financebuddy",
            "extension": "csv",
            "settings": {"delimiter": ",", "lineterminator": "\n"},
        }
        json.dump(config_data, fp)
        fp.flush()

        try:
            config = load_exporter_config(fp.name)
            assert config.format == "financebuddy"
            assert config.extension == ExporterExtension.CSV
            assert config.settings.delimiter == ","
            assert config.settings.lineterminator == "\n"
        finally:
            os.unlink(fp.name)


def test_load_exporter_config_file_not_found():
    with pytest.raises(ConfigurationError) as exc_info:
        load_exporter_config("/nonexistent/path/config.json")
    assert "does not exist" in str(exc_info.value)


def test_load_exporter_config_invalid_json():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fp:
        fp.write("not valid json {")
        fp.flush()

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                load_exporter_config(fp.name)
            assert "not contain a valid JSON object" in str(exc_info.value)
        finally:
            os.unlink(fp.name)


def test_load_exporter_config_missing_format():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fp:
        config_data = {"extension": "csv"}
        json.dump(config_data, fp)
        fp.flush()

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                load_exporter_config(fp.name)
            assert "does not contain key 'format'" in str(exc_info.value)
        finally:
            os.unlink(fp.name)


def test_load_exporter_config_missing_extension():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fp:
        config_data = {"format": "financebuddy"}
        json.dump(config_data, fp)
        fp.flush()

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                load_exporter_config(fp.name)
            assert "does not contain key 'extension'" in str(exc_info.value)
        finally:
            os.unlink(fp.name)


def test_load_exporter_config_unknown_extension():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as fp:
        config_data = {"format": "financebuddy", "extension": "xml"}
        json.dump(config_data, fp)
        fp.flush()

        try:
            with pytest.raises(ConfigurationError) as exc_info:
                load_exporter_config(fp.name)
            assert "unknown extension" in str(exc_info.value)
        finally:
            os.unlink(fp.name)


def test_find_exporter_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "exporter_financebuddy_json_config.json")
        config_data = {"format": "financebuddy", "extension": "json", "settings": {"indent": 2}}
        with open(config_path, "w") as fp:
            json.dump(config_data, fp)

        # Mock the _get_config_dir to return tmpdir
        import financebuddy.exporterconfig.api as api_module

        original_get_config_dir = api_module._get_config_dir
        api_module._get_config_dir = lambda: tmpdir

        try:
            config = find_exporter_config("financebuddy", "json")
            assert config.format == "financebuddy"
            assert config.extension == ExporterExtension.JSON
            assert config.settings.indent == 2
        finally:
            api_module._get_config_dir = original_get_config_dir


def test_find_exporter_config_not_found():
    with tempfile.TemporaryDirectory() as tmpdir:
        import financebuddy.exporterconfig.api as api_module

        original_get_config_dir = api_module._get_config_dir
        api_module._get_config_dir = lambda: tmpdir

        try:
            with pytest.raises(UnsupportedFormatError) as exc_info:
                find_exporter_config("financebuddy", "xml")
            assert "no exporter found" in str(exc_info.value)
        finally:
            api_module._get_config_dir = original_get_config_dir


def test_get_exporter_configs():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two config files
        config1_path = os.path.join(tmpdir, "exporter_financebuddy_csv_config.json")
        config1_data = {"format": "financebuddy", "extension": "csv", "settings": {"delimiter": ","}}
        with open(config1_path, "w") as fp:
            json.dump(config1_data, fp)

        config2_path = os.path.join(tmpdir, "exporter_financebuddy_json_config.json")
        config2_data = {"format": "financebuddy", "extension": "json", "settings": {"indent": 2}}
        with open(config2_path, "w") as fp:
            json.dump(config2_data, fp)

        # Mock the _get_config_dir to return tmpdir
        import financebuddy.exporterconfig.api as api_module

        original_get_config_dir = api_module._get_config_dir
        api_module._get_config_dir = lambda: tmpdir

        try:
            configs = get_exporter_configs()
            assert len(configs) == 2
            assert configs[0].extension == ExporterExtension.CSV
            assert configs[1].extension == ExporterExtension.JSON
        finally:
            api_module._get_config_dir = original_get_config_dir


def test_get_exporter_configs_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        import financebuddy.exporterconfig.api as api_module

        original_get_config_dir = api_module._get_config_dir
        api_module._get_config_dir = lambda: tmpdir

        try:
            configs = get_exporter_configs()
            assert len(configs) == 0
        finally:
            api_module._get_config_dir = original_get_config_dir


def test_get_exporter_configs_nonexistent_directory():
    import financebuddy.exporterconfig.api as api_module

    original_get_config_dir = api_module._get_config_dir
    api_module._get_config_dir = lambda: "/nonexistent/path"

    try:
        configs = get_exporter_configs()
        assert len(configs) == 0
    finally:
        api_module._get_config_dir = original_get_config_dir
