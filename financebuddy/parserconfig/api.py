# stdlib
import json
import os
from typing import Any

# third party
import financebuddy_parsers

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parserconfig import factory
from financebuddy.parserconfig.models import ParserConfig, ParserExtension


def load_parser_config(path: str) -> ParserConfig:
    if not os.path.exists(path):
        raise FinanceBuddyException(f"parser config file does not exist: {path}")

    try:
        with open(path, "r") as fp:
            content: dict[str, Any] = json.load(fp)
    except Exception:
        raise FinanceBuddyException(f"parser config file does not contain a valid JSON object: {path}")

    raw_extension = content.get("extension")
    if not raw_extension:
        raise FinanceBuddyException(f"parser config file does not contain key 'extension': {path}")

    extension = ParserExtension(raw_extension)
    if extension == ParserExtension.UNKNOWN:
        raise FinanceBuddyException(f"file contains an unknown extension '{raw_extension}': {path}")

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
    path = os.path.join(financebuddy_parsers.DIR_CONFIGS, basename)
    return path


def find_parser_config(format: str, extension: str) -> ParserConfig:
    path = build_path(format, extension)
    try:
        config = load_parser_config(path)
        return config
    except FinanceBuddyException:
        raise FinanceBuddyException(f"no parser found for format/extension: {format}/{extension}")
