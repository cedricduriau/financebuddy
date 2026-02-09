import pytest

from financebuddy.exceptions import (
    ConfigurationError,
    ErrorCode,
    ExportError,
    FinanceBuddyException,
    ParsingError,
    UnsupportedFormatError,
)


def test_base_exception():
    with pytest.raises(FinanceBuddyException):
        raise FinanceBuddyException("base error")


def test_base_exception_with_error_code():
    exc = FinanceBuddyException("test", ErrorCode.UNKNOWN)
    assert exc.message == "test"
    assert exc.error_code == ErrorCode.UNKNOWN


def test_configuration_error():
    with pytest.raises(ConfigurationError):
        raise ConfigurationError("config error")


def test_configuration_error_with_code():
    exc = ConfigurationError("config error", ErrorCode.CONFIG_FILE_NOT_FOUND)
    assert exc.error_code == ErrorCode.CONFIG_FILE_NOT_FOUND


def test_unsupported_format_error():
    with pytest.raises(UnsupportedFormatError):
        raise UnsupportedFormatError("format error")


def test_unsupported_format_error_default_code():
    exc = UnsupportedFormatError("format error")
    assert exc.error_code == ErrorCode.UNSUPPORTED_FORMAT


def test_parsing_error():
    with pytest.raises(ParsingError):
        raise ParsingError("parse error")


def test_parsing_error_default_code():
    exc = ParsingError("parse error")
    assert exc.error_code == ErrorCode.PARSING_FAILED


def test_export_error():
    with pytest.raises(ExportError):
        raise ExportError("export error")


def test_export_error_default_code():
    exc = ExportError("export error")
    assert exc.error_code == ErrorCode.EXPORT_FAILED
