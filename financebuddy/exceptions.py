from enum import IntEnum


class ErrorCode(IntEnum):
    UNKNOWN = 0
    CONFIG_FILE_NOT_FOUND = 1001
    CONFIG_INVALID_JSON = 1002
    CONFIG_MISSING_FIELD = 1003
    CONFIG_UNKNOWN_VALUE = 1004
    UNSUPPORTED_FORMAT = 2001
    UNSUPPORTED_EXTENSION = 2002
    PARSING_FAILED = 3001
    EXPORT_FAILED = 4001


class FinanceBuddyException(Exception):
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.UNKNOWN) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class ConfigurationError(FinanceBuddyException):
    pass


class UnsupportedFormatError(FinanceBuddyException):
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.UNSUPPORTED_FORMAT) -> None:
        super().__init__(message, error_code)


class ParsingError(FinanceBuddyException):
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.PARSING_FAILED) -> None:
        super().__init__(message, error_code)


class ExportError(FinanceBuddyException):
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.EXPORT_FAILED) -> None:
        super().__init__(message, error_code)
