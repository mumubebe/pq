from .pq import Pipeline, _import_global
import json, sys, os
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="pq is a Python command-line JSON processor"
    )
    parser.add_argument("expression", nargs="?")
    parser.add_argument(
        "-i",
        "--imports",
        help='Additional import modules separated with semicolon. --imports "import datetime as dt"',
    )

    if os.isatty(0):
        parser.print_help()
        return

    args = parser.parse_args()

    if args.imports:
        _import_global(args.imports)

    json_data = json.loads(sys.stdin.read())

    pipeline = Pipeline(jsondata=json_data, str_input=args.expression)

    pipeline.run()
