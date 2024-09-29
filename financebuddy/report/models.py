# stdlib
import datetime
import enum

# third party
from pydantic import BaseModel


class ReportTransactionField(enum.StrEnum):
    DATE = "date"
    VALUE = "value"
    CURRENCY = "currency"
    DISPLAY = "display"
    SRC_BANK_NAME = "src_bank_name"
    SRC_ACCOUNT_HOLDER = "src_account_holder"
    SRC_ACCOUNT_NUMBER = "src_account_number"
    DST_BANK_NAME = "dst_bank_name"
    DST_ACCOUNT_HOLDER = "dst_account_holder"
    DST_ACCOUNT_NUMBER = "dst_account_number"
    DESCRIPTION = "description"


class ReportTransaction(BaseModel):
    src_bank_name: str
    src_account_holder: str | None = None
    src_account_number: str | None = None
    dst_bank_name: str | None = None
    dst_account_holder: str | None = None
    dst_account_number: str | None = None
    date: datetime.datetime
    value: int
    display: str
    currency: str
    description: str | None = None
    raw: str
    hash: str


class ReportError(BaseModel):
    raw: str
    message: str
    exception: str


class ReportItem(BaseModel):
    model: ReportTransaction | None = None
    error: ReportError | None = None


class ReportSummary(BaseModel):
    total: int
    skipped: int
    parsed: int
    failed: int


class Report(BaseModel):
    items: list[ReportItem]
    summary: ReportSummary
