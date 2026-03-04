import json
import os
from typing import Any

import financebuddy_parsers

from financebuddy.exceptions import ConfigurationError, ErrorCode, UnsupportedFormatError
from financebuddy.parserconfig import factory
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


def _get_config_dir() -> str:
    env_dir = os.environ.get("FINANCEBUDDY_CONFIG_DIR")
    if env_dir:
        return env_dir
    return financebuddy_parsers.DIR_CONFIGS


def load_parser_config(path: str) -> ParserConfig:
    if not os.path.exists(path):
        raise ConfigurationError(
            f"parser config file does not exist: {path}",
            ErrorCode.CONFIG_FILE_NOT_FOUND,
        )

    try:
        with open(path, "r") as fp:
            content: dict[str, Any] = json.load(fp)
    except Exception:
        raise ConfigurationError(
            f"parser config file does not contain a valid JSON object: {path}",
            ErrorCode.CONFIG_INVALID_JSON,
        )

    raw_extension = content.get("extension")
    if not raw_extension:
        raise ConfigurationError(
            f"parser config file does not contain key 'extension': {path}",
            ErrorCode.CONFIG_MISSING_FIELD,
        )

    extension = ParserExtension(raw_extension)
    if extension == ParserExtension.UNKNOWN:
        raise ConfigurationError(
            f"file contains an unknown extension '{raw_extension}': {path}",
            ErrorCode.CONFIG_UNKNOWN_VALUE,
        )

    format: str | None = None
    if extension not in [ParserExtension.CSV, ParserExtension.XLSX]:
        format = content.get("format")

    configuration = factory.get_parser_config(path, format, extension, content)
    return configuration


def get_parser_configs() -> list[ParserConfig]:
    configs = list(map(load_parser_config, financebuddy_parsers.PARSER_CONFIGS))
    return configs


def build_path(format: str, extension: str) -> str:
    basename = f"parser_{format}_{extension}_config.json"
    config_dir = _get_config_dir()
    path = os.path.join(config_dir, basename)
    return path


def find_parser_config(format: str, extension: str) -> ParserConfig:
    path = build_path(format, extension)
    try:
        config = load_parser_config(path)
        return config
    except ConfigurationError:
        raise UnsupportedFormatError(f"no parser found for format/extension: {format}/{extension}")
