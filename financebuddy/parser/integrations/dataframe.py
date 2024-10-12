# stdlib
import datetime
import decimal
import json

# third party
import dateutil.parser
import pandas as pd

# package
from financebuddy import currencyutils
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.parser import helpers
from financebuddy.parser.integrations.base import Parser
from financebuddy.parserconfig.integrations.dataframe import DataframeParserConfig
from financebuddy.report.models import (
    Report,
    ReportError,
    ReportItem,
    ReportSummary,
    ReportTransaction,
    ReportTransactionField,
)


def pandas_serialize_json(v):
    if isinstance(v, pd.Timestamp):
        v = v.to_pydatetime().isoformat()
    elif isinstance(v, (int, float)):
        v = str(v)
    return v


class DataframeParser(Parser):
    def __init__(self, config: DataframeParserConfig) -> None:
        super().__init__(config)
        self.config = config

    def read_file(self, path: str) -> pd.DataFrame:
        raise NotImplementedError()

    def row_to_transaction(self, row: list[str]) -> ReportTransaction:
        raw_transaction: dict = {"src_bank_name": self.config.format}

        # raw
        raw_str = json.dumps(row)
        raw_transaction["raw"] = raw_str

        # hash
        raw_hash = helpers.hash_string(raw_str)
        raw_transaction["hash"] = raw_hash

        # field map parsing
        for field, column in self.config.settings.field_map.items():
            v = row[column]

            if field in [
                ReportTransactionField.SRC_ACCOUNT_NUMBER,
                ReportTransactionField.DST_ACCOUNT_NUMBER,
            ]:
                v = helpers.remove_whitespace(v)
            elif field == ReportTransactionField.DATE:
                if date_format := self.config.settings.date_format:
                    dt = datetime.datetime.strptime(v, date_format)
                else:
                    dt = dateutil.parser.parse(v)
                v = dt
            elif field == ReportTransactionField.VALUE:
                v = helpers.sanitize_value_string(v)
                v = decimal.Decimal(v)
            elif field == ReportTransactionField.CURRENCY:
                code = currencyutils.validate_currency(v)
                v = code

            raw_transaction[field] = v

        # currency
        currency = raw_transaction.get(ReportTransactionField.CURRENCY, self.config.settings.currency)
        if currency is None:
            raise FinanceBuddyException("no currency could be determined")

        # value
        value = raw_transaction.get(ReportTransactionField.VALUE, decimal.Decimal(0))
        value = currencyutils.calculate_smallest_value(value, currency)
        raw_transaction[ReportTransactionField.VALUE] = value

        # display
        display = currencyutils.format_value(value, currency)
        raw_transaction[ReportTransactionField.DISPLAY] = display

        transcation = ReportTransaction(**raw_transaction)
        return transcation

    def dataframe_to_items(self, df: pd.DataFrame) -> list[ReportItem]:
        df.fillna("", inplace=True)
        items: list[ReportItem] = []

        for t in df.itertuples(index=False):
            row: list[str] = list(map(pandas_serialize_json, t))

            transaction: ReportTransaction | None = None
            error: ReportError | None = None

            try:
                transaction = self.row_to_transaction(row)
            except Exception as e:
                error = ReportError(
                    raw=json.dumps(row),
                    message="",
                    exception=str(e),
                )

            item = ReportItem(transaction=transaction, error=error)
            items.append(item)

        return items

    def generate_report(self, path: str) -> Report:
        df = self.read_file(path)
        items = self.dataframe_to_items(df)

        nr_of_transactions = 0
        nr_of_errors = 0
        for item in items:
            if item.error:
                nr_of_errors += 1
            elif item.transaction:
                nr_of_transactions += 1

        report = Report(
            items=items,
            summary=ReportSummary(
                total=df.shape[0],
                parsed=nr_of_transactions,
                failed=nr_of_errors,
            ),
        )
        return report
