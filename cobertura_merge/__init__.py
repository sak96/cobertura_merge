"""cobertura xml merge execution logic"""
from argparse import ArgumentParser
from functools import reduce
from operator import add
from pathlib import Path

from xmltodict import parse, unparse

from cobertura_merge.types import CoverageXml


def main():
    """Main Function for cobertura xml merge executable

    Executable takes Following Arguments:
        -o/--output: output file paths, defaults to "coverage.xml"
        unnamed variable length arguments: input file paths.
    Merges input files paths to produce output file
    """
    parser = ArgumentParser(
        description="Utility to merge multiple cobertura xml files into one."
    )
    parser.add_argument(
        dest="input_files",
        metavar="input.xml",
        type=Path,
        nargs="+",
        help="input cobertura xml to be merged",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="coverage.xml",
        type=Path,
        help="output cobertura xml to be merged",
        default="coverage.xml",
    )

    args = parser.parse_args()
    inputs = []
    for input_file in args.input_files:
        with open(input_file, "rb") as input_fd:
            coverage_dict = parse(input_fd)
            coverage = CoverageXml.parse_obj(obj=coverage_dict)
            inputs.append(coverage)

    output_coverage = reduce(add, inputs)
    output_dict = output_coverage.dict(exclude_unset=True, by_alias=True)

    with open(args.output, "w", encoding="utf-8") as output_fd:
        unparse(output_dict, output=output_fd, pretty=True)


if __name__ == "__main__":
    main()
