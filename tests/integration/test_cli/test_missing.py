# stdlib
import os

# package
from financebuddy import cli


def test_cli_missing_action(capfd):
    code = cli.run([])
    assert code == 1

    out, _ = capfd.readouterr()
    out = out.rstrip(os.linesep)

    assert out == "financebuddy-cli: error: missing or incomplete action, see -h/--help"
