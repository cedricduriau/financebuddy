# stdlib
import datetime
import json
import os
import tempfile

# package
from financebuddy.report.models import Report


def load_report(path: str) -> Report:
    with open(path, "r") as fp:
        content = json.load(fp)
        report = Report.model_validate(content)
        return report


def dump_report(report: Report) -> str:
    directory = tempfile.gettempdir()
    timestamp = datetime.datetime.now(datetime.timezone.utc).timestamp()
    filename = f"financebuddy_report_{timestamp}.json"
    path = os.path.join(directory, filename)
    with open(path, "w") as fp:
        data = json.loads(report.model_dump_json())
        json.dump(data, fp, indent=4)
    return path
