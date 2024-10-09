# stdlib
from enum import StrEnum

# third party
from pydantic import BaseModel


class ParserExtension(StrEnum):
    UNKNOWN = "unknown"
    CSV = "csv"
    XLSX = "xlsx"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ParserConfigSettings(BaseModel):
    pass


class ParserConfig(BaseModel):
    path: str
    format: str
    extension: ParserExtension
    settings: ParserConfigSettings | None = None
