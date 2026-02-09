import json
import os
from typing import Any

from financebuddy.exceptions import ConfigurationError, ErrorCode, UnsupportedFormatError
from financebuddy.exporterconfig import factory
from financebuddy.exporterconfig.models import ExporterConfig, ExporterExtension
from financebuddy.logging import get_logger

logger = get_logger(__name__)


def _get_config_dir() -> str:
    env_dir = os.environ.get("FINANCEBUDDY_CONFIG_DIR")
    if env_dir:
        return env_dir
    return os.path.expanduser("~/.financebuddy/configs")


def load_exporter_config(path: str) -> ExporterConfig:
    if not os.path.exists(path):
        raise ConfigurationError(f"exporter config file does not exist: {path}", ErrorCode.CONFIG_FILE_NOT_FOUND)

    try:
        with open(path, "r") as fp:
            content: dict[str, Any] = json.load(fp)
    except Exception:
        raise ConfigurationError(
            f"exporter config file does not contain a valid JSON object: {path}", ErrorCode.CONFIG_INVALID_JSON
        )

    raw_format = content.get("format")
    if not raw_format:
        raise ConfigurationError(
            f"exporter config file does not contain key 'format': {path}", ErrorCode.CONFIG_MISSING_FIELD
        )

    raw_extension = content.get("extension")
    if not raw_extension:
        raise ConfigurationError(
            f"exporter config file does not contain key 'extension': {path}", ErrorCode.CONFIG_MISSING_FIELD
        )

    extension = ExporterExtension(raw_extension)
    if extension == ExporterExtension.UNKNOWN:
        raise ConfigurationError(
            f"file contains an unknown extension '{raw_extension}': {path}", ErrorCode.CONFIG_UNKNOWN_VALUE
        )

    logger.debug(f"Loading exporter config from: {path}")
    configuration = factory.get_exporter_config(raw_format, extension, content)
    return configuration


def get_exporter_configs() -> list[ExporterConfig]:
    config_dir = _get_config_dir()
    if not os.path.exists(config_dir):
        logger.debug(f"Config directory does not exist: {config_dir}, returning empty list")
        return []

    configs = []
    for filename in sorted(os.listdir(config_dir)):
        if filename.startswith("exporter_") and filename.endswith("_config.json"):
            path = os.path.join(config_dir, filename)
            try:
                config = load_exporter_config(path)
                configs.append(config)
                logger.debug(f"Loaded exporter config: {config.format}/{config.extension}")
            except ConfigurationError as e:
                logger.error(f"Failed to load exporter config from {path}: {e}")
    return configs


def build_path(format: str, extension: str) -> str:
    basename = f"exporter_{format}_{extension}_config.json"
    path = os.path.join(_get_config_dir(), basename)
    return path


def find_exporter_config(format: str, extension: str) -> ExporterConfig:
    path = build_path(format, extension)
    try:
        config = load_exporter_config(path)
        return config
    except ConfigurationError:
        raise UnsupportedFormatError(
            f"no exporter found for format/extension: {format}/{extension}", ErrorCode.UNSUPPORTED_FORMAT
        )
