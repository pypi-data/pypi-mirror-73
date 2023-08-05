#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""The command line interface to jsonflattifier"""

import argparse
import sys
import textwrap

import jsonflattifier
from jsonflattifier import flattify, flattifys
from jsonflattifier.errors import JsonflattifierError
from jsonflattifier.version import __version__


def print_version() -> None:
    print(__version__)


JSONFLATTIFIER_DESCRIPTION = textwrap.dedent(
    f"""
Convert JSON Document with nested objects and their parameters
to the JSON Document with Flat Denormalised Data.
"""
)


class LineWrapRawTextHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(" ", text).strip()
        return textwrap.wrap(text, width)


def run_jsonflattifier_command(args: argparse.Namespace):
    setup(args)

    if args.command:
        if args.path:
            flatjson = flattify(args.json_input, args.jsonpath_keys)
        else:
            flatjson = flattifys(args.json_input, args.jsonpath_keys)

        if args.json:
            print(flatjson)
        if args.csv:
            [print(row) for row in jsonflattifier.flatjson_to_csv(flatjson).split("\r")]
        if not args.no_table:
            jsonflattifier.flatjson_to_print(flatjson)
        return 0
    else:
        return 1


def _add_run(subparsers):
    p = subparsers.add_parser(
        "flattify",
        formatter_class=LineWrapRawTextHelpFormatter,
        help=(
            "Provide the JSON Document String or a Path to JSON File you want to flattify, "
            "and also specify the return and print options."
        ),
    )
    p.add_argument(
        "json_input",
        metavar="json-input",
        help="The JSON Document String or a Path to the JSON File you want to flattify.",
    )
    p.add_argument(
        "--path",
        "-p",
        help="Indicate that the path to the file was provided in the json-input parameter.",
        action="store_true",
    )
    p.add_argument(
        "--json",
        help="Generate JSON with Flat Denormalised Data.",
        action="store_true",
    )
    p.add_argument(
        "--jsonpath-keys",
        "-jk",
        help="Use the jsonpath Normalised Path for keys.",
        action="store_true",
    )
    p.add_argument(
        "--csv", help="Generate CSV with Flat Denormalised Data.", action="store_true",
    )
    p.add_argument(
        "--no-table",
        "-nt",
        help="Do NOT print Table with Denormalised Data.",
        action="store_true",
    )
    p.set_defaults(subparser=p)


def get_command_parser():
    parser = argparse.ArgumentParser(
        prog="jsonflattifier",
        formatter_class=LineWrapRawTextHelpFormatter,
        description=JSONFLATTIFIER_DESCRIPTION,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        description="Get help for specific command:\n> jsonflattifer flattify --help",
    )

    _add_run(subparsers)

    parser.add_argument("--version", action="store_true", help="Print version and exit")
    return parser


def setup(args):
    if "version" in args and args.version:
        print_version()
        sys.exit(0)


def cli() -> int:
    """Entry point from command line"""
    try:
        parser = get_command_parser()

        parsed_jsonflattifier_args = parser.parse_args()
        setup(parsed_jsonflattifier_args)

        if not parsed_jsonflattifier_args.command:
            parser.print_help()
            return 1
        return run_jsonflattifier_command(parsed_jsonflattifier_args)
    except JsonflattifierError as e:
        print(str(e), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(cli())
