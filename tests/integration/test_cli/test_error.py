# stdlib
import os

# third party
import pytest

# package
from financebuddy import cli
from financebuddy.exceptions import FinanceBuddyException


def test_cli_exception(capfd, monkeypatch):
    def mock_raise(*args, **kwargs):
        raise RuntimeError("crash")

    monkeypatch.setattr(cli, "list_parsers", mock_raise)

    with pytest.raises(RuntimeError):
        cli.run(["parsers", "list"])


def test_cli_exception_package(capfd, monkeypatch):
    def mock_raise(*args, **kwargs):
        raise FinanceBuddyException("oops!")

    monkeypatch.setattr(cli, "list_parsers", mock_raise)

    code = cli.run(["parsers", "list"])
    assert code == 1

    out, _ = capfd.readouterr()
    out = out.rstrip(os.linesep)

    assert out == "financebuddy-cli: error: oops!"
