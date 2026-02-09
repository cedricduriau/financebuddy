# Troubleshooting Guide

This guide helps you solve common problems and understand FinanceBuddy's error codes.

## Table of Contents

- [Error Code Reference](#error-code-reference)
- [Common Issues & Solutions](#common-issues--solutions)
- [Debug Techniques](#debug-techniques)
- [Getting Help](#getting-help)

---

## Error Code Reference

FinanceBuddy uses structured error codes to help you quickly identify and fix problems.

### Configuration Errors (1000-1999)

| Code | Error Type | Meaning | Common Cause | Solution |
|------|-----------|---------|--------------|----------|
| **1001** | ConfigurationError | Config file not found | Config file doesn't exist or wrong path | Check `~/.financebuddy/configs/` directory exists. See Configuration Guide. |
| **1002** | ConfigurationError | Invalid JSON syntax | Config file has malformed JSON | Validate JSON syntax. Use an online JSON validator if needed. |
| **1003** | ConfigurationError | Missing required field | Required field missing from config | Check that all required fields are present in config file. |
| **1004** | ConfigurationError | Invalid field value | Config field has unrecognized value | Check config values match expected types (e.g., "csv" not "CSV"). |

### Format Errors (2000-2999)

| Code | Error Type | Meaning | Common Cause | Solution |
|------|-----------|---------|--------------|----------|
| **2001** | UnsupportedFormatError | Unknown format | Bank format not recognized | Run `financebuddy parsers list` to see available formats. |
| **2002** | UnsupportedFormatError | Unknown extension | File extension not recognized | Run `financebuddy parsers list` or `financebuddy exporters list` to see available extensions. |

### Parsing Errors (3000-3999)

| Code | Error Type | Meaning | Common Cause | Solution |
|------|-----------|---------|--------------|----------|
| **3001** | ParsingError | Parsing failed | Invalid data format | Use `--verbose` flag to see which row failed and why. |

### Export Errors (4000-4999)

| Code | Error Type | Meaning | Common Cause | Solution |
|------|-----------|---------|--------------|----------|
| **4001** | ExportError | Export failed | Can't write to file | Check file permissions and disk space. |

---

## Common Issues & Solutions

### Issue: "Unsupported Format" Error

**Error Message:**
```
financebuddy-cli: error: parser config not supported for format/extension: mybank/csv
```

**Error Code:** 2001 (UnsupportedFormatError)

**What This Means:**

The format "mybank" isn't installed or recognized by FinanceBuddy.

**Solution:**

1. Check available formats:
   ```bash
   financebuddy parsers list
   ```

2. Use a supported format from the list. For example:
   ```bash
   financebuddy parsers parse -f financebuddy -e csv -i mybank.csv
   ```

3. If you need a custom format, check the [financebuddy-parsers](https://github.com/cedricduriau/financebuddy-parsers) documentation.

---

### Issue: "File Not Found" Error

**Error Message:**
```
financebuddy-cli: error: [Errno 2] No such file or directory: 'bank_data.csv'
```

**What This Means:**

The input file path doesn't exist or is incorrect.

**Solution:**

1. Check that the file exists:
   ```bash
   ls -la bank_data.csv
   ```

2. If using a relative path, make sure you're in the correct directory:
   ```bash
   pwd
   ls *.csv
   ```

3. Use absolute path if unsure:
   ```bash
   financebuddy parsers parse -f financebuddy -e csv -i ~/Downloads/bank_data.csv
   ```

4. Check for typos in the filename:
   ```bash
   # Wrong: extra underscore
   financebuddy parsers parse -f financebuddy -e csv -i bank_data_.csv
   
   # Correct: actual filename
   financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv
   ```

---

### Issue: "Permission Denied" Error

**Error Message:**
```
financebuddy-cli: error: export failed: permission denied
```

**Error Code:** 4001 (ExportError)

**What This Means:**

You don't have write permissions to the output directory.

**Solution:**

1. Check directory permissions:
   ```bash
   ls -la ./exports/
   ```

2. Create directory if it doesn't exist:
   ```bash
   mkdir -p ./exports
   ```

3. Fix permissions if needed:
   ```bash
   chmod 755 ./exports
   ```

4. Try export again:
   ```bash
   financebuddy exporters export -f financebuddy -e csv \
     -i report.json -o ./exports/transactions.csv
   ```

5. If using `/tmp/`, check disk space:
   ```bash
   df -h /tmp/
   ```

---

### Issue: "Parsing Failed" with No Details

**Error Message:**
```
financebuddy-cli: error: parsing failed: invalid date format
```

**Error Code:** 3001 (ParsingError)

**What This Means:**

One or more rows in your bank data couldn't be parsed, but you need more details.

**Solution:**

1. Run parsing again with `--verbose` flag:
   ```bash
   financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv --verbose
   ```

2. Look for `ERROR:` lines to see which rows failed:
   ```
   DEBUG: Processing row 1: OK
   DEBUG: Processing row 2: OK
   ERROR: Row 5: Invalid date format (expected YYYY-MM-DD, got 02/08/2026)
   ERROR: Row 7: Missing required field 'amount'
   ```

3. Fix the problematic rows in your source file and try again.

4. If you can't fix the data, see which transactions were successfully parsed:
   ```bash
   # Check report file
   cat /tmp/financebuddy_report_*.json | jq '.summary'
   ```

---

### Issue: Output File Not Found After Parsing

**Error Message:**

No error, but can't find where output file was saved.

**Solution:**

1. By default, files are saved to `/tmp/`:
   ```bash
   ls -lt /tmp/financebuddy_report_*.json | head -1
   ```

2. Get the full path:
   ```bash
   # After running parse command, capture the output
   REPORT=$(financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv)
   echo $REPORT
   ```

3. Or specify output location explicitly:
   ```bash
   financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv \
     -o ./my_report.json
   ```

---

### Issue: "Missing Arguments" Error

**Error Message:**
```
financebuddy-cli: error: the following arguments are required: -f/--format, -e/--extension, -i/--input
```

**What This Means:**

You didn't provide all required arguments for the command.

**Solution:**

1. Make sure you include all required flags:
   ```bash
   # Wrong: missing -e (extension)
   financebuddy parsers parse -f financebuddy -i bank_data.csv
   
   # Correct: all required flags
   financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv
   ```

2. Check command format:
   ```bash
   financebuddy parsers parse --help
   ```

---

### Issue: "Command Not Found"

**Error Message:**
```
bash: financebuddy: command not found
```

**Solution:**

1. Install FinanceBuddy:
   ```bash
   pip install financebuddy
   ```

2. If using a virtual environment, activate it:
   ```bash
   source .env/bin/activate
   pip install financebuddy
   financebuddy --version
   ```

3. Verify installation:
   ```bash
   which financebuddy
   financebuddy --version
   ```

---

### Issue: Configuration File Errors

**Error Message:**
```
financebuddy-cli: error: config file not found
```

**Error Code:** 1001 (ConfigurationError)

**Solution:**

1. Check if config directory exists:
   ```bash
   ls -la ~/.financebuddy/configs/
   ```

2. If not, create it:
   ```bash
   mkdir -p ~/.financebuddy/configs/
   ```

3. Check config files are present:
   ```bash
   ls -la ~/.financebuddy/configs/exporter_*.json
   ```

4. Validate config file JSON syntax:
   ```bash
   cat ~/.financebuddy/configs/exporter_financebuddy_csv_config.json | jq .
   ```

5. See Configuration Guide for setup instructions.

---

## Debug Techniques

### Technique 1: Use --verbose Flag

The `--verbose` flag shows detailed debug logs:

```bash
financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv --verbose
```

Look for:
- `DEBUG:` lines → what the tool is doing
- `ERROR:` lines → what went wrong
- `INFO:` lines → important events

### Technique 2: Check Recent Report Files

Find and examine the most recent report:

```bash
# List recent reports (newest first)
ls -lt /tmp/financebuddy_report_*.json | head -5

# Get the newest one
LATEST=$(ls -t /tmp/financebuddy_report_*.json | head -1)

# View it (pretty-printed)
cat $LATEST | jq .

# Count parsed vs failed
cat $LATEST | jq '.summary'

# See failed items
cat $LATEST | jq '.items[] | select(.error != null)'
```

### Technique 3: Validate Input File Format

Check your input file structure:

```bash
# For CSV files
head -5 bank_data.csv

# For Excel files, convert to CSV first to inspect
python -c "import openpyxl; wb=openpyxl.load_workbook('bank_data.xlsx'); print(wb.sheetnames)"
```

### Technique 4: Test with --dry-run

Preview export without writing:

```bash
financebuddy exporters export -f financebuddy -e csv \
  -i /tmp/financebuddy_report_*.json --dry-run | head -20
```

### Technique 5: Check Disk Space

Ensure you have enough disk space:

```bash
# Check /tmp/ space
df -h /tmp/

# Or wherever you're saving files
df -h ./exports/
```

### Technique 6: Pipeline Testing

Test each step separately:

```bash
# Step 1: Parse and capture output
echo "Step 1: Parsing..."
REPORT=$(financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv)
echo "Report saved to: $REPORT"

# Step 2: Verify report exists
echo "Step 2: Checking report..."
ls -lh $REPORT
cat $REPORT | jq '.summary'

# Step 3: Export
echo "Step 3: Exporting..."
financebuddy exporters export -f financebuddy -e csv -i $REPORT
```

---

## Getting Help

If you're still having issues:

1. **Check the documentation:**
   - [Command Reference](./COMMANDS.md) - All commands and options
   - [Configuration Guide](./CONFIGURATION.md) - How to configure FinanceBuddy
   - [README](../README.md) - General information

2. **Use --help:**
   ```bash
   financebuddy --help
   financebuddy parsers --help
   financebuddy parsers parse --help
   ```

3. **Enable verbose logging:**
   ```bash
   financebuddy parsers parse -f financebuddy -e csv -i bank_data.csv --verbose
   ```

4. **Report an issue:**
   Visit [GitHub Issues](https://github.com/cedricduriau/financebuddy/issues) with:
   - Error code and message
   - Command you ran (sanitize sensitive data)
   - Verbose output
   - Your environment (Python version, OS, FinanceBuddy version)

---

## Quick Reference: Error Codes

| Code | Type | Quick Fix |
|------|------|-----------|
| 1001 | Configuration | Check ~/.financebuddy/configs/ |
| 1002 | Configuration | Validate JSON syntax |
| 1003 | Configuration | Add missing config field |
| 1004 | Configuration | Fix invalid config value |
| 2001 | Format | Run: `financebuddy parsers list` |
| 2002 | Extension | Run: `financebuddy parsers list` |
| 3001 | Parsing | Add `--verbose` flag |
| 4001 | Export | Check permissions and disk space |
