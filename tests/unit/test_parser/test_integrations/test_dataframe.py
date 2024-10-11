# stdlib
import datetime

# third party
import pandas as pd
import pytest

# package
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parser.integrations.dataframe import DataframeParser, pandas_serialize_json
from financebuddy.report.models import ReportTransactionField


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        ("foo", "foo"),
        (pd.Timestamp(datetime.datetime(1970, 1, 1)), datetime.datetime(1970, 1, 1).isoformat()),
        (1, "1"),
        (1.0, "1.0"),
    ],
)
def test_pandas_serialize_json(value, expected):
    assert pandas_serialize_json(value) == expected


def test_read_file(fix_parser_dataframe: DataframeParser):
    with pytest.raises(NotImplementedError):
        fix_parser_dataframe.read_file("")


def test_row_to_transaction(fix_parser_dataframe: DataframeParser):
    date = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    row = [
        " foo ",
        " bar ",
        date.isoformat(),
        "1.00",
        "EUR",
    ]
    fix_parser_dataframe.config.settings.field_map = {
        ReportTransactionField.SRC_ACCOUNT_NUMBER: 0,
        ReportTransactionField.DST_ACCOUNT_NUMBER: 1,
        ReportTransactionField.DATE: 2,
        ReportTransactionField.VALUE: 3,
        ReportTransactionField.CURRENCY: 4,
    }
    transaction = fix_parser_dataframe.row_to_transaction(row)
    assert transaction.src_account_number == "foo"
    assert transaction.dst_account_number == "bar"
    assert transaction.date == date
    assert transaction.value == 100
    assert transaction.display == "1.00"
    assert transaction.currency == "EUR"


def test_test_row_to_transaction_fail_no_currency(fix_parser_dataframe: DataframeParser):
    row: list[str] = ["1.00"]
    fix_parser_dataframe.config.settings.field_map = {ReportTransactionField.VALUE: 0}
    with pytest.raises(FinanceBuddyException):
        fix_parser_dataframe.row_to_transaction(row)


def test_test_row_to_transaction_no_value(fix_parser_dataframe: DataframeParser):
    date = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    row: list[str] = [date.isoformat(), "EUR"]
    fix_parser_dataframe.config.settings.field_map = {
        ReportTransactionField.DATE: 0,
        ReportTransactionField.CURRENCY: 1,
    }
    transction = fix_parser_dataframe.row_to_transaction(row)
    assert transction.date == date
    assert transction.value == 0
    assert transction.display == "0.00"
    assert transction.currency == "EUR"
