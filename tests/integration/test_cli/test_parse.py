# stdlib
import datetime
import os

# third party
import pytest
from financebuddy_parsers import MAP_SAMPLE_FILES

# package
from financebuddy import cli
from financebuddy.report import api as reportapi

values = []
for k, v in MAP_SAMPLE_FILES.items():
    format, extension = k
    for path in v:
        values.append((format, extension, path))


@pytest.mark.parametrize(["format", "extension", "path"], values)
def test_parse_file(format: str, extension: str, path: str, capfd):
    code = cli.run(["parsers", "parse", "-f", format, "-e", extension, "-i", path])
    assert code == 0

    out, _ = capfd.readouterr()
    out = out.rstrip(os.linesep)

    report = reportapi.load_report(out)
    assert report.summary.parsed == 3
    assert report.summary.failed == 0

    i0 = report.items[0]
    assert i0.error is None
    assert i0.transaction is not None
    t0 = i0.transaction
    assert t0.src_bank_name == format
    assert t0.date == datetime.datetime(1970, 1, 1)
    assert t0.currency == "EUR"
    assert t0.value == -100000

    i1 = report.items[1]
    assert i1.error is None
    assert i1.transaction is not None
    t1 = i1.transaction
    assert t1.src_bank_name == format
    assert t1.date == datetime.datetime(1970, 1, 1)
    assert t1.currency == "EUR"
    assert t1.value == 0

    i2 = report.items[2]
    assert i2.error is None
    assert i2.transaction is not None
    t2 = i2.transaction
    assert t2.src_bank_name == format
    assert t2.date == datetime.datetime(1970, 1, 1)
    assert t2.currency == "EUR"
    assert t2.value == 100000
