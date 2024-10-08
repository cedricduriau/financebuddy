# stdlib
import datetime
import decimal
import json

# third party
import dateutil.parser
import pandas as pd

# package
from financebuddy import currencyutils
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
        raw_model: dict = {"src_bank_name": self.config.format}

        # content
        raw_str = json.dumps(row)
        raw_model["raw"] = raw_str

        # hash
        raw_hash = helpers.hash_string(raw_str)
        raw_model["hash"] = raw_hash

        for name, column in self.config.settings.field_map.items():
            value = row[column]

            if name in [
                ReportTransactionField.SRC_ACCOUNT_NUMBER,
                ReportTransactionField.DST_ACCOUNT_NUMBER,
            ]:
                value = helpers.remove_whitespace(value)
            elif name == ReportTransactionField.DATE:
                if date_format := self.config.settings.date_format:
                    dt = datetime.datetime.strptime(value, date_format)
                else:
                    dt = dateutil.parser.parse(value)
                value = dt
            elif name == ReportTransactionField.VALUE:
                value = decimal.Decimal(helpers.sanitize_value_string(value))
            elif name == ReportTransactionField.CURRENCY:
                code = currencyutils.validate_currency(value)
                value = code

            raw_model[name] = value

        currency = raw_model.get(ReportTransactionField.CURRENCY, self.config.settings.currency)
        if currency is None:
            raise RuntimeError("no currency could be determined")

        value = raw_model.get(ReportTransactionField.VALUE)
        if value is not None:
            value = currencyutils.calculate_smallest_value(value, currency)
            raw_model[ReportTransactionField.VALUE] = value

            display = currencyutils.format_value(value, currency)
            raw_model[ReportTransactionField.DISPLAY] = display

        import_model = ReportTransaction(**raw_model)
        return import_model

    def dataframe_to_items(self, df: pd.DataFrame) -> list[ReportItem]:
        df.fillna("", inplace=True)
        items: list[ReportItem] = []

        for t in df.itertuples():
            row: list[str] = [pandas_serialize_json(i) for i in t[1:]]

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

        nr_of_items = 0
        nr_of_errors = 0
        for item in items:
            if item.error:
                nr_of_errors += 1
            else:
                nr_of_items += 1

        report = Report(
            items=items,
            summary=ReportSummary(
                total=df.shape[0],
                parsed=nr_of_items,
                failed=nr_of_errors,
            ),
        )
        return report
