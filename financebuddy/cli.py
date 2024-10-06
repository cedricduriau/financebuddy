# stdlib
from argparse import ArgumentParser

# third party
from tabulate import tabulate

# package
from financebuddy import __version__
from financebuddy.exceptions import FinanceBuddyException
from financebuddy.export import api as exportapi
from financebuddy.parser import api as parserapi
from financebuddy.parserconfig import api as configapi
from financebuddy.report import api as reportapi

OUT_ERROR_PREFIX = "financebuddy-cli: error:"


# ==============================================================================
# actions
# ==============================================================================
def list_parsers() -> None:
    configs = configapi.get_parser_configs()
    table_data = [[config.format, config.extension] for config in configs]
    print(tabulate(table_data, headers=["format", "extension"], tablefmt="rounded_grid"))


def parse_file(format: str, extension: str, input: str) -> None:
    config = configapi.find_parser_config(format, extension)
    report = parserapi.generate_report(input, config)
    report_path = reportapi.dump_report(report)
    print(report_path)


def list_exporters() -> None:
    exporter_types = exportapi.get_exporters()
    table_data = [[Exporter.format, Exporter.extension] for Exporter in exporter_types]
    print(tabulate(table_data, headers=["format", "extension"], tablefmt="rounded_grid"))


def export_report(format: str, extension: str, input: str) -> None:
    report = reportapi.load_report(input)
    export_path = exportapi.export_report(report, format, extension)
    print(export_path)


# ==============================================================================
# parser
# ==============================================================================
def build_parser() -> ArgumentParser:
    description = "FinanceBuddy is a tool that centralizes and parses data from diffent banks into a unified format, streamlining the process for analytics and reporting."
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
    p_export.set_defaults(func=export_report)

    return parser


# ==============================================================================
# main
# ==============================================================================
def run(args: list[str] | None = None) -> int:
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
        print(f"{OUT_ERROR_PREFIX} missing or incomplete action, see -h/--help")
        return 1

    try:
        func(**kwargs)
    except FinanceBuddyException as e:
        print(f"{OUT_ERROR_PREFIX} {e}")
        return 1

    return 0


if __name__ == "__main__":
    code = run()
    exit(code)
