import os
from argparse import ArgumentParser

from tabulate import tabulate

from financebuddy import __version__
from financebuddy.exceptions import (
    ConfigurationError,
    ExportError,
    FinanceBuddyException,
    ParsingError,
    UnsupportedFormatError,
)
from financebuddy.export import api as exportapi
from financebuddy.exporterconfig import api as exporterconfigapi
from financebuddy.logging import get_logger, setup_logging
from financebuddy.parser import api as parserapi
from financebuddy.parserconfig import api as configapi
from financebuddy.report import api as reportapi

logger = get_logger(__name__)

OUT_ERROR_PREFIX = "financebuddy-cli: error:"


# ====================================================================================
# actions
# ====================================================================================
def list_parsers() -> None:
    configs = configapi.get_parser_configs()
    table_data = [[config.format, config.extension] for config in configs]
    print(tabulate(table_data, headers=["format", "extension"], tablefmt="rounded_grid"))


def parse_file(format: str, extension: str, input: str) -> None:
    logger.debug(f"Parsing file: {input} (format={format}, extension={extension})")
    config = configapi.find_parser_config(format, extension)
    report = parserapi.generate_report(input, config)
    report_path = reportapi.dump_report(report)
    logger.info(f"Report generated: {report_path}")
    print(report_path)


def list_exporters() -> None:
    configs = exporterconfigapi.get_exporter_configs()
    table_data = [[config.format, config.extension] for config in configs]
    print(tabulate(table_data, headers=["format", "extension"], tablefmt="rounded_grid"))


def export_report(format: str, extension: str, input: str) -> None:
    logger.debug(f"Exporting report: {input} (format={format}, extension={extension})")
    report = reportapi.load_report(input)
    config = exporterconfigapi.find_exporter_config(format, extension)
    export_path = exportapi.export_report(report, config)
    logger.info(f"Report exported: {export_path}")
    print(export_path)


# ====================================================================================
# parser
# ====================================================================================
def build_parser() -> ArgumentParser:
    description = (
        "FinanceBuddy is a tool that centralizes and parses data from different banks "
        "into a unified format, streamlining the process for analytics and reporting."
    )
    parser = ArgumentParser(description=description)
    subparsers = parser.add_subparsers()

    # root arguments
    parser.add_argument("-v", "--version", action="store_true", help="print the release version")

    # parsers
    p_parsers = subparsers.add_parser("parsers")
    p_parsers_sub = p_parsers.add_subparsers()

    # parsers - list
    p_parse_list = p_parsers_sub.add_parser("list", help="list the available parsers")
    p_parse_list.set_defaults(func=list_parsers)

    # parsers - parse
    p_parse = p_parsers_sub.add_parser("parse", help="parses a bank file to a report file")
    p_parse.add_argument("-f", "--format", required=True, help="format of the bank file")
    p_parse.add_argument("-e", "--extension", required=True, help="extension of the bank file")
    p_parse.add_argument("-i", "--input", required=True, help="path of the bank file")
    p_parse.set_defaults(func=parse_file)

    # exporters
    p_exporters = subparsers.add_parser("exporters")
    p_exporters_sub = p_exporters.add_subparsers()

    # export - list
    p_export_list = p_exporters_sub.add_parser("list", help="list the available exporters")
    p_export_list.set_defaults(func=list_exporters)

    # exporters - export
    p_export = p_exporters_sub.add_parser("export", help="exports a report file")
    p_export.add_argument("-f", "--format", required=True, help="format of the export file")
    p_export.add_argument("-e", "--extension", required=True, help="extension of the export file")
    p_export.add_argument("-i", "--input", required=True, help="path of the report file")
    p_export.add_argument("--dry-run", action="store_true", help="print output to stdout instead of writing to file")
    p_export.set_defaults(func=export_report)

    return parser


# ====================================================================================
# main
# ====================================================================================
def run(args: list[str] | None = None) -> int:
    setup_logging(level=os.getenv("LOGLEVEL") or "WARNING")

    parser = build_parser()
    namespace = parser.parse_args(args)
    kwargs = vars(namespace)

    version = kwargs.pop("version")
    if version:
        print(__version__)
        return 0

    try:
        func = kwargs.pop("func")
    except KeyError:
        logger.error("Missing or incomplete action")
        print(f"{OUT_ERROR_PREFIX} missing or incomplete action, see -h/--help")
        return 1

    try:
        func(**kwargs)
    except UnsupportedFormatError as e:
        logger.error(f"Unsupported format: {e}")
        print(f"{OUT_ERROR_PREFIX} {e}")
        return 1
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        print(f"{OUT_ERROR_PREFIX} {e}")
        return 1
    except ParsingError as e:
        logger.error(f"Parsing error: {e}")
        print(f"{OUT_ERROR_PREFIX} {e}")
        return 1
    except ExportError as e:
        logger.error(f"Export error: {e}")
        print(f"{OUT_ERROR_PREFIX} {e}")
        return 1
    except FinanceBuddyException as e:
        print(f"{OUT_ERROR_PREFIX} {e.stdout()}")
        return 1

    return 0


if __name__ == "__main__":
    code = run()
    exit(code)
