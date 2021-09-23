from argparse import ArgumentParser
from pathlib import Path

from xmltodict import parse, unparse

from cobertura_merge.types import CoverageXml


def main():
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
        with open(input_file, "rb") as f:
            coverage_dict = parse(f)
            coverage = CoverageXml.parse_obj(obj=coverage_dict)
            inputs.append(coverage)

    output_coverage = inputs[0]
    output_dict = output_coverage.dict(exclude_unset=True, by_alias=True)

    with open(args.output, "w") as f:
        unparse(output_dict, output=f, pretty=True)


if __name__ == "__main__":
    main()
