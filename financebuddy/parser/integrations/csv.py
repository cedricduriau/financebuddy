# stdlib
import csv
import datetime
import decimal
import io
import json

# third party
import chardet
import dateutil.parser

# package
from financebuddy import currencyutils
from financebuddy.parser import helpers
from financebuddy.parser.integrations.base import Parser
from financebuddy.parserconfig.integrations.csv import CSVParserConfig
from financebuddy.parserconfig.models import ParserExtension
from financebuddy.report.models import (
    Report,
    ReportError,
    ReportItem,
    ReportSummary,
    ReportTransaction,
    ReportTransactionField,
)


def read_csv(path: str, config: CSVParserConfig):
    with open(path, "rb") as fp:
        # detect encoding
        sample_bytes = fp.read(1024)
        scan: dict[str, str] = chardet.detect(sample_bytes)
        encoding: str = scan["encoding"]

        # detect csv dialect
        sample_str = str(fp.readline(), encoding=encoding)
        dialect = csv.Sniffer().sniff(sample_str)
        delimiter = config.settings.delimiter or dialect.delimiter

        # read csv file contents
        fp.seek(0)
        content = io.StringIO(str(fp.read(), encoding=encoding))

        reader = csv.reader(content, dialect, delimiter=delimiter)
        return reader


def csv_row_to_model(row: int, content: list, config: CSVParserConfig) -> ReportTransaction:
    raw_model: dict = {"src_bank_name": config.format}

    # content
    raw_str = json.dumps(content)
    raw_model["raw"] = raw_str

    # hash
    raw_hash = helpers.hash_string(raw_str)
    raw_model["hash"] = raw_hash

    for name, column in config.settings.field_map.items():
        try:
            value = content[column]
        except IndexError:
            raise RuntimeError(f"row {row} does not have column {column}")

        if name == ReportTransactionField.DATE:
            if config.settings.date_format:
                value = datetime.datetime.strptime(value, config.settings.date_format)
            else:
                value = dateutil.parser.parse(value)
        elif name == ReportTransactionField.VALUE:
            value = decimal.Decimal(helpers.fix_value_string(value))
        elif name == ReportTransactionField.CURRENCY:
            code = currencyutils.validate_currency(value)
            value = code

        raw_model[name] = value

    currency = raw_model.get(ReportTransactionField.CURRENCY, config.settings.currency)
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


class CSVParser(Parser):
    extension: ParserExtension = ParserExtension.CSV

    def __init__(self, config: CSVParserConfig) -> None:
        self.config = config

    def generate_report(self, path: str) -> Report:
        reader = read_csv(path, self.config)
        total_items: int = 0
        total_skipped: int = 0
        parsed_items: list[ReportItem] = []
        errors: list[ReportError] = []

        for row, content in enumerate(reader):
            total_items += 1

            # skip row
            if row in self.config.settings.skip_rows:
                total_skipped += 1
                continue

            # parse row
            model: ReportTransaction | None = None
            error: ReportError | None = None

            try:
                model = csv_row_to_model(row, content, self.config)
            except Exception as e:
                error = ReportError(
                    raw=json.dumps(content),
                    message=f"failed to parse row {row}",
                    exception=str(e),
                )
                errors.append(error)

            parsed_item = ReportItem(model=model, error=error)
            parsed_items.append(parsed_item)

        report = Report(
            items=parsed_items,
            summary=ReportSummary(
                total=total_items,
                skipped=total_skipped,
                parsed=len(parsed_items) - len(errors),
                failed=len(errors),
            ),
        )
        return report
