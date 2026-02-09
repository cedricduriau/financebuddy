# Command Reference

Complete reference for all `financebuddy` commands, options, and examples.

## Table of Contents

- [Global Options](#global-options)
- [parsers list](#parsers-list)
- [parsers parse](#parsers-parse)
- [exporters list](#exporters-list)
- [exporters export](#exporters-export)
- [Common Patterns](#common-patterns)
- [Error Handling](#error-handling)

---

## Global Options

These options work with all commands.

### `-v, --version`

Print the FinanceBuddy version and exit.

**Usage:**
```bash
financebuddy --version
```

**Output:**
```
0.8.0
```

---

## parsers list

List all available parsers (bank formats and file extensions).

**Usage:**
```bash
financebuddy parsers list
```

**Description:**

Shows all supported parser formats and their file extensions. Each row represents a format/extension combination that can be used with the `parsers parse` command.

**Output Example:**
```
╭──────────┬───────────╮
│ format   │ extension │
├──────────┼───────────┤
│ financebuddy │ csv       │
│ financebuddy │ xlsx      │
╰──────────┴───────────╯
```

**How to Use:**

Run this command first to see what parsers are available, then use the format/extension in your parse command:

```bash
# List available parsers
financebuddy parsers list

# Use one of the listed combinations
financebuddy parsers parse -f financebuddy -e csv -i mybank.csv
```

---

## parsers parse

Parse a bank data file into a standardized report format.

**Usage:**
```bash
financebuddy parsers parse -f FORMAT -e EXTENSION -i FILE
```

**Required Arguments:**

| Argument | Short | Long | Description |
|----------|-------|------|-------------|
| Format | `-f` | `--format` | Bank format (e.g., `financebuddy`) - see `parsers list` for available formats |
| Extension | `-e` | `--extension` | File extension (e.g., `csv`, `xlsx`) - see `parsers list` for available extensions |
| Input File | `-i` | `--input` | Path to the bank data file to parse |

**Optional Arguments:**

| Argument | Short | Long | Description |
|----------|-------|------|-------------|
| Output File | `-o` | `--output` | Output file path. If not specified, saves to `/tmp/financebuddy_report_TIMESTAMP.json` |
| Verbose | `-v` | `--verbose` | Show debug logs to help troubleshoot parsing issues |

**Output:**

When successful, prints the path to the generated report file:
```
/tmp/financebuddy_report_20260208T143000.json
```

---

### Basic Examples

**Parse a CSV file (default output location):**
```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_export.csv
```

Output:
```
/tmp/financebuddy_report_20260208T143000.json
```

The report file contains:
- All parsed transactions with details (date, amount, description, etc.)
- Failed transactions with error messages
- Summary (total rows, parsed count, failed count)

**Parse an Excel file:**
```bash
financebuddy parsers parse -f financebuddy -e xlsx -i bank_export.xlsx
```

**Parse with custom output location:**
```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_export.csv \
  -o ./my_reports/bank_report.json
```

Output:
```
./my_reports/bank_report.json
```

**Debug parsing issues (see detailed logs):**
```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_export.csv --verbose
```

Output:
```
DEBUG: Starting parse...
DEBUG: Processing row 1: parsed transaction
DEBUG: Processing row 2: parsed transaction
ERROR: Row 5: Invalid date format (Expected YYYY-MM-DD, got: 08/02/2026)
DEBUG: Processing complete. Total: 5, Parsed: 4, Failed: 1
/tmp/financebuddy_report_20260208T143000.json
```

---

### Report File Format

The generated report is a JSON file with this structure:

```json
{
  "items": [
    {
      "transaction": {
        "src_bank_name": "ACME Bank",
        "src_account_holder": "John Doe",
        "src_account_number": "AA11223344",
        "dst_bank_name": "ACME Bank",
        "dst_account_holder": "Jane Doe",
        "dst_account_number": "BB55667788",
        "date": "2026-02-08T00:00:00",
        "value": 100.50,
        "display": "100.50",
        "currency": "USD",
        "description": "Transfer payment",
        "raw": "original raw line from bank file",
        "hash": "a1b2c3d4e5f6..."
      },
      "error": null
    },
    {
      "transaction": null,
      "error": "Invalid date format in row 5"
    }
  ],
  "summary": {
    "total": 10,
    "parsed": 9,
    "failed": 1
  }
}
```

---

## exporters list

List all available exporters (formats and file extensions).

**Usage:**
```bash
financebuddy exporters list
```

**Description:**

Shows all supported export formats and their file extensions. Each row represents a format/extension combination that can be used with the `exporters export` command.

**Output Example:**
```
╭──────────┬───────────╮
│ format   │ extension │
├──────────┼───────────┤
│ financebuddy │ csv       │
│ financebuddy │ json      │
╰──────────┴───────────╯
```

**How to Use:**

```bash
# List available exporters
financebuddy exporters list

# Export report using one of the listed combinations
financebuddy exporters export -f financebuddy -e csv -i report.json
```

---

## exporters export

Export a parsed report into a specific format.

**Usage:**
```bash
financebuddy exporters export -f FORMAT -e EXTENSION -i FILE [OPTIONS]
```

**Required Arguments:**

| Argument | Short | Long | Description |
|----------|-------|------|-------------|
| Format | `-f` | `--format` | Export format (e.g., `financebuddy`) - see `exporters list` for available formats |
| Extension | `-e` | `--extension` | Export file extension (e.g., `csv`, `json`) - see `exporters list` for available extensions |
| Input File | `-i` | `--input` | Path to the parsed report file (generated by `parsers parse`) |

**Optional Arguments:**

| Argument | Short | Long | Description |
|----------|-------|------|-------------|
| Output File | `-o` | `--output` | Output file path. If not specified, saves to `/tmp/financebuddy_export_TIMESTAMP.{ext}` |
| Dry Run | | `--dry-run` | Preview output to terminal instead of writing to file |
| Verbose | `-v` | `--verbose` | Show debug logs |

**Output:**

When successful, prints the path to the generated export file:
```
/tmp/financebuddy_export_20260208T143005.csv
```

With `--dry-run`, prints the export contents to terminal instead.

---

### Basic Examples

**Export as CSV (default output location):**
```bash
financebuddy exporters export -f financebuddy -e csv \
  -i /tmp/financebuddy_report_20260208T143000.json
```

Output:
```
/tmp/financebuddy_export_20260208T143005.csv
```

**Export as JSON:**
```bash
financebuddy exporters export -f financebuddy -e json \
  -i /tmp/financebuddy_report_20260208T143000.json
```

**Export with custom output location:**
```bash
financebuddy exporters export -f financebuddy -e csv \
  -i /tmp/financebuddy_report_20260208T143000.json \
  -o ./exports/transactions.csv
```

**Preview export (dry-run mode):**
```bash
financebuddy exporters export -f financebuddy -e csv \
  -i /tmp/financebuddy_report_20260208T143000.json \
  --dry-run
```

Output:
```
src_bank_name,src_account_holder,src_account_number,dst_bank_name,...
ACME Bank,John Doe,AA11223344,ACME Bank,...
ACME Bank,Jane Doe,BB55667788,ACME Bank,...
```

**Export with verbose logging:**
```bash
financebuddy exporters export -f financebuddy -e json \
  -i /tmp/financebuddy_report_20260208T143000.json --verbose
```

---

### Export File Formats

#### CSV Export

Human-readable format with one transaction per row:

```csv
src_bank_name,src_account_holder,src_account_number,dst_bank_name,dst_account_holder,dst_account_number,date,value,display,currency,description,raw,hash
ACME Bank,John Doe,AA11223344,ACME Bank,Jane Doe,BB55667788,2026-02-08T00:00:00,100.50,100.50,USD,Transfer payment,original_raw_data,a1b2c3d4e5f6...
```

Use when:
- You need to open the data in Excel or spreadsheet software
- You're sharing data with non-technical stakeholders
- You want human-readable format

#### JSON Export

Structured format, useful for programmatic processing:

```json
{
  "transactions": [
    {
      "src_bank_name": "ACME Bank",
      "src_account_holder": "John Doe",
      "src_account_number": "AA11223344",
      "dst_bank_name": "ACME Bank",
      "dst_account_holder": "Jane Doe",
      "dst_account_number": "BB55667788",
      "date": "2026-02-08T00:00:00",
      "value": 100.50,
      "display": "100.50",
      "currency": "USD",
      "description": "Transfer payment",
      "raw": "original_raw_data",
      "hash": "a1b2c3d4e5f6..."
    }
  ]
}
```

Use when:
- You're processing data programmatically
- You need structured, typed data
- Integration with other JSON-based tools

---

## Common Patterns

### Pattern 1: Parse and Export in One Pipeline

Parse a bank file and immediately export it:

```bash
# Step 1: Parse the file
REPORT=$(financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv)

# Step 2: Export the report
financebuddy exporters export -f financebuddy -e json -i $REPORT
```

Or as a one-liner:

```bash
financebuddy exporters export -f financebuddy -e json \
  -i $(financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv)
```

### Pattern 2: Batch Processing Multiple Files

Parse multiple bank files and export them:

```bash
for file in bank_exports/*.csv; do
  echo "Processing $file..."
  REPORT=$(financebuddy parsers parse -f financebuddy -e csv -i "$file")
  financebuddy exporters export -f financebuddy -e csv -i "$REPORT" \
    -o "./processed/$(basename "$file")"
  echo "✓ $file processed"
done
```

### Pattern 3: Debug Parsing Issues

Check what's failing in your bank export:

```bash
# Step 1: Try with verbose output
financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv --verbose

# Step 2: Check the report file
cat /tmp/financebuddy_report_*.json | jq '.items[] | select(.error != null)'

# Step 3: Preview what will be exported
financebuddy exporters export -f financebuddy -e csv \
  -i /tmp/financebuddy_report_*.json --dry-run | head -10
```

### Pattern 4: Find Latest Report File

Always use the most recent report:

```bash
# Get the latest report file
LATEST=$(ls -t /tmp/financebuddy_report_*.json | head -1)

# Export it
financebuddy exporters export -f financebuddy -e json -i "$LATEST"
```

---

## Error Handling

### Command Not Found

**Error:**
```
bash: financebuddy: command not found
```

**Solution:**

Make sure FinanceBuddy is installed:
```bash
pip install financebuddy
```

Or if using a virtual environment, activate it:
```bash
source .env/bin/activate
pip install financebuddy
```

### Missing Required Arguments

**Error:**
```
financebuddy-cli: error: the following arguments are required: -f/--format, -e/--extension, -i/--input
```

**Solution:**

You forgot to provide all required arguments. Check the command format:
```bash
# Wrong: missing -e and -i
financebuddy parsers parse -f financebuddy

# Correct:
financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv
```

### Unsupported Format Error (Code 2001)

**Error:**
```
financebuddy-cli: error: parser config not supported for format/extension: unknown/csv
```

**Solution:**

The format you specified isn't recognized. Check available formats:
```bash
financebuddy parsers list
```

Then use one of the listed formats:
```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv
```

### Configuration Error (Code 1001-1004)

**Error:**
```
financebuddy-cli: error: config file not found: /path/to/config.json
```

**Solution:**

Check that the configuration file exists. See [Configuration Guide](./CONFIGURATION.md) for details on where configs are stored.

### File Not Found

**Error:**
```
financebuddy-cli: error: [Errno 2] No such file or directory: 'nonexistent.csv'
```

**Solution:**

The input file path doesn't exist. Check the path:
```bash
# Wrong: file doesn't exist
financebuddy parsers parse -f financebuddy -e csv -i nonexistent.csv

# Correct: use actual file path
financebuddy parsers parse -f financebuddy -e csv -i ~/Downloads/bank_export.csv

# Or list files first
ls -la bank_export*
```

### Parsing Failed (Code 3001)

**Error:**
```
financebuddy-cli: error: parsing failed: invalid date format
```

**Solution:**

Use `--verbose` flag to see exactly which row failed:
```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv --verbose
```

Look for `ERROR:` lines in the output. See [Troubleshooting Guide](./TROUBLESHOOTING.md) for detailed recovery steps.

### Export Failed (Code 4001)

**Error:**
```
financebuddy-cli: error: export failed: permission denied
```

**Solution:**

The output directory doesn't exist or you don't have write permissions. Check:
```bash
# Check if directory exists
ls -la /tmp/

# Create output directory if needed
mkdir -p ./exports

# Ensure you have write permissions
chmod 755 ./exports

# Try export again
financebuddy exporters export -f financebuddy -e csv -i report.json -o ./exports/data.csv
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| See all available parsers | `financebuddy parsers list` |
| Parse a CSV file | `financebuddy parsers parse -f financebuddy -e csv -i file.csv` |
| Parse an Excel file | `financebuddy parsers parse -f financebuddy -e xlsx -i file.xlsx` |
| Debug parsing | Add `--verbose` flag to see detailed logs |
| See all available exporters | `financebuddy exporters list` |
| Export as CSV | `financebuddy exporters export -f financebuddy -e csv -i report.json` |
| Export as JSON | `financebuddy exporters export -f financebuddy -e json -i report.json` |
| Preview export (no file write) | Add `--dry-run` flag |
| Custom output location | Add `-o /path/to/output.csv` |
| Show version | `financebuddy --version` |
