"""cobertura xml merge execution logic"""
from argparse import ArgumentParser
from pathlib import Path

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
    inputs = map(CoverageXml.read_from_file, args.input_files)
    output_coverage = CoverageXml.merge(list(inputs))
    output_coverage.output_to_file(args.output)


if __name__ == "__main__":
    main()
