from .pq import Pipeline
import json, sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='pq is a Python command-line JSON processor')
    parser.add_argument('expression', nargs='?')

    args = parser.parse_args()

    json_data = json.loads(sys.stdin.read())

    pipeline = Pipeline(json_data, args.expression)
    pipeline.run()