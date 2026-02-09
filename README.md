![](https://img.shields.io/badge/pypi-0.8.0-blue)
![](https://img.shields.io/badge/python-3.12-blue)
![](https://img.shields.io/badge/license-GPLv3.0-blue)

# financebuddy

`financebuddy` is a tool that centralizes and parses data from different banks into a unified format, streamlining the process for analytics and reporting.

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

## Quick Start

Get up and running in 2 minutes:

### 1. Parse your bank export

```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_export.csv
```

Output:
```
/tmp/financebuddy_report_20260208T143000.json
```

The report contains all parsed transactions with a summary (total, parsed, failed counts).

### 2. Export as JSON for analysis

```bash
financebuddy exporters export -f financebuddy -e json \
  -i /tmp/financebuddy_report_20260208T143000.json
```

Output:
```
/tmp/financebuddy_export_20260208T143005.json
```

Done! Your data is now in a standardized format ready for analysis.

### 3. Or use in a pipeline

Parse and export in one command:

```bash
REPORT=$(financebuddy parsers parse -f financebuddy -e csv -i bank_export.csv)
financebuddy exporters export -f financebuddy -e json -i $REPORT
```

**Next steps:** See [docs/COMMANDS.md](./docs/COMMANDS.md) for complete command reference and [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) if something goes wrong.

## Parsing

See [docs/COMMANDS.md](./docs/COMMANDS.md) for complete parsing reference.

```sh
# list the supported formats and extensions
financebuddy parsers list

# parse exported bank data
financebuddy parsers parse -f FORMAT -e EXTENSION -i FILE
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

See [docs/COMMANDS.md](./docs/COMMANDS.md) for complete export reference.

```sh
# list the supported formats and extensions
financebuddy exporters list

# export parsed report
financebuddy exporters export -f FORMAT -e EXTENSION -i FILE [--dry-run]
```

The parsed reports can be exported in different formats and extensions.

The result is an exported file dumped to the file system. This file contains only the successfully parsed transactions from the provided report.

**Optional flags:**
- `--dry-run`: Preview the export output without writing to file
- `--verbose`: Show debug logs

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

**Q: What's the difference between format and extension?**

A: The **format** is the bank or data source (e.g., `financebuddy`), while the **extension** is the file type (e.g., `csv`, `xlsx`). Together they identify how to parse your data.

**Q: Where does the output file go?**

A: By default, files are saved to `/tmp/financebuddy_report_TIMESTAMP.json` and `/tmp/financebuddy_export_TIMESTAMP.csv` (depending on format). You can specify a custom location with the `-o` flag.

**Q: What if parsing fails?**

A: Run with `--verbose` flag to see which rows failed and why:
```bash
financebuddy parsers parse -f financebuddy -e csv -i data.csv --verbose
```
See [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) for error code reference and solutions.

**Q: Can I preview the export before writing?**

A: Yes! Use `--dry-run` to preview without creating files:
```bash
financebuddy exporters export -f financebuddy -e csv -i report.json --dry-run
```

**Q: Can I parse bank data and export it straight away in one go?**

A: Yes. Pipelines are friends of ours here.

```sh
# parse + export
financebuddy parsers parse -f FORMAT -e EXTENSION -i FILE | \
  xargs -I{} financebuddy exporters export -f financebuddy -e json -i {}
```

**Q: What if I get an error code like "2001"?**

A: Error codes help identify the problem. See [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) for detailed explanation and recovery steps for each error code.

**Q: I can't find my output file. Where is it?**

A: Check `/tmp/` for `financebuddy_*` files. Or specify where you want it with the `-o` option.

**Q: Does this work on macOS/Windows/Linux?**

A: Yes! FinanceBuddy works on all platforms. Just make sure you have Python 3.12+ installed.

**Q: What bank formats are supported?**

A: Run `financebuddy parsers list` to see available formats. See the [financebuddy-parsers](https://github.com/cedricduriau/financebuddy-parsers?tab=readme-ov-file#available-parsers) documentation for details on each format.

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
