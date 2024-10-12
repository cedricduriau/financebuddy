![](https://img.shields.io/badge/pypi-0.8.0-blue)
![](https://img.shields.io/badge/python-3.12-blue)
![](https://img.shields.io/badge/license-GPLv3.0-blue)

# financebuddy

`financebuddy` is a tool that centralizes and parses data from diffent banks into a unified format, streamlining the process for analytics and reporting.

## Installing

`financebuddy` can be installed using [pip](https://pypi.org/project/pip/).

```sh
pip install financebuddy
```

To test that installation was successful, try:

```sh
financebuddy-cli --help
```

## How does it work?

1. Export the data from your bank
2. Parse the data from your bank generating a report
3. Export the parsed report
4. Feast

## Parsing

```sh
# list the supported formats and extensions
financebuddy-cli parsers list

# parse exported bank data
financebuddy-cli parsers parse -f FORMAT -e EXTENSION -i FILE
```

The exported bank data can be associated with a format and an extension.

- the `format` is driven by the bank the data is coming from
- the `extension` is driven by the file format the data is stored in
- the `file` is the path of the exported bank data

Once parsed, a report file will be generated and dumped to the file system. This report contains the details of every transactions, succesfully parsed or not, along with a summary.

### Available parser formats & extensions

See `financebuddy-parser` [README](https://github.com/cedricduriau/financebuddy-parsers?tab=readme-ov-file#available-parsers).

### Example
```json
// example: /tmp/financebuddy_report_TIMESTAMP.json
{
    "items": [
        {
            "transaction": {
                "src_bank_name": "ACME",
                "src_account_holder": "JOHN DOE",
                "src_account_number": "AA11223344",
                "dst_bank_name": "ACME",
                "dst_account_holder": "JANE ROE",
                "dst_account_number": "BB55667788",
                "date": "1970-01-01T00:00:00",
                "value": 100,
                "display": "1.00",
                "currency": "EUR",
                "description": "A symbolic euro.",
                "raw": "...",
                "hash": "dad5b1989edc50lel31243236213097f"
            },
            "error": null,
        },
        {
            "transaction": null,
            "error": "invalid date",
        }
    ],
    "summary": {
        "total": 2,
        "parsed": 1,
        "failed": 1,
    }
}
```

## Exporting

```sh
# list the supported formats and extensions
financebuddy-cli exporters list

# export parsed report
financebuddy-cli exporters export -f FORMAT -e EXTENSION -i FILE
```

The parsed reports can be exported in different formats and extensions.

The result is an exported file dumped to the file system. This file contains only the soccessfully parsed transactions from the provided report.

### Available exporter formats

| Format        | Extension   |
|---------------|-------------|
| financebuddy  | csv         |
| financebuddy  | json        |

### Example
```json
// example: /tmp/financebuddy_export_TIMESTAMP.json
{
    "transactions": [
        {
            "src_bank_name": "ACME",
            "src_account_holder": "JOHN DOE",
            "src_account_number": "AA11223344",
            "dst_bank_name": "ACME",
            "dst_account_holder": "JANE ROE",
            "dst_account_number": "BB55667788",
            "date": "1970-01-01T00:00:00",
            "value": 100,
            "display": "1.00",
            "currency": "EUR",
            "description": "A symbolic euro.",
            "raw": "...",
            "hash": "dad5b1989edc50lel31243236213097f"
        }
    ]
}
```

## FAQ

### Can I parse bank data and export it straight away in one go?

Yes. Pipelines are friends of ours here.

```sh
# parse + export
financebuddy-cli parsers parse -f FORMAT -e EXTENSION -i FILE | xargs -I{} financebuddy-cli exporters export -f financebuddy -e json -i {}
```

## Development

### Install
```sh
python -m venv .env
source .env/bin/activate
make install-dev
```

### Test
```sh
make test
```
