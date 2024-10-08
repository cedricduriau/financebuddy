# stdlib
import datetime

# third party
import pytest

# package
from financebuddy.report.models import Report, ReportError, ReportItem, ReportSummary, ReportTransaction


@pytest.fixture
def fix_report_transaction() -> ReportTransaction:
    transaction = ReportTransaction(
        src_bank_name="bank1",
        src_account_holder="bank1_holder1",
        src_account_number="bank1_holder1_account_1",
        dst_bank_name="bank2",
        dst_account_holder="bank2_holder1",
        dst_account_number="bank2_holder1_account_1",
        date=datetime.datetime.now(tz=datetime.timezone.utc),
        value=100,
        currency="EUR",
        display="1.00",
        description="foo",
        raw="[]",
        hash="foo",
    )
    return transaction


@pytest.fixture
def fix_report_error() -> ReportError:
    error = ReportError(raw="[]", message="", exception="")
    return error


@pytest.fixture
def fix_report(fix_report_transaction, fix_report_error) -> Report:
    report = Report(
        items=[
            ReportItem(transaction=fix_report_transaction),
            ReportItem(error=fix_report_error),
        ],
        summary=ReportSummary(
            total=2,
            parsed=1,
            failed=1,
        ),
    )
    return report
