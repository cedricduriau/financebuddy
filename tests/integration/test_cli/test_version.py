# stdlib
import os

# package
from financebuddy import cli


def test_cli_version(capfd):
    code = cli.run(["--version"])
    assert code == 0

    out, _ = capfd.readouterr()
    out = out.rstrip(os.linesep)

    assert out == "0.3.0"
