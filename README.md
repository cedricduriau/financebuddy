# financebuddy

FinanceBuddy is a tool that centralizes and parses data from diffent banks into a unified format, streamlining the process for analytics and reporting.

## Available sources

Consult the list of supported banks [here](https://github.com/cedricduriau/financebuddy-parsers/tree/main?tab=readme-ov-file#available-sources).

## How does it work?

1. Export the data from your bank
2. Parse the data from your bank generating a report
3. Export the parsed report
4. Feast

## Parsing

The exported bank data can be associated with a format and an extension.

- the `format` is driven by the bank the data is coming from
- the `extension` is driven by the file format the data is stored in

```sh
financebuddy-cli parsers parse -f FORMAT -e EXTENSION -i FILE
/tmp/financebuddy_report_TIMESTAMP.json
```

Once parsed, a report file will be generated and dumped to the file system. This report contains the details of every transactions, succesfully parsed or not, along with a summary.

## Exporting

The parsed reports can be exported in different formats and extensions.

```sh
financebuddy-cli exporters export -f FORMAT -e EXTENSION -i FILE
/tmp/financebuddy_export_TIMESTAMP.EXTENSION
```

The result is an exported file dumped to the file system. This file contains only the soccessfully parsed transactions from the provided report.

```json
{
    "items": [
        {
            "model": {...}
            "error": null,
        },
        {
            "model": null
            "error": "invalid date",
        }
    ],
    "summary": {
        "total": 2,
        "skipped": 0,
        "parsed": 1,
        "failed": 1,
    }
}
```

## Examples

```sh
# parse
financebuddy-cli parsers parse -f FORMAT -e EXTENSION -i FILE

# export
financebuddy-cli exporters export -f financebuddy -e json -i FILE

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
