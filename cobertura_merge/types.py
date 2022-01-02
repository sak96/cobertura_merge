"""Types for Coverage File

Spec: https://github.com/cobertura/web/blob/master/htdocs/xml/coverage-04.dtd

Some amount of liberty is added by allowing optionals
"""
from functools import reduce
from operator import add
from pathlib import Path
from time import time_ns
from typing import List, Optional

from pydantic import Field, validator
from xmltodict import parse, unparse

from cobertura_merge.types_helper import BaseOrderedModel, list_validator


class Condition(BaseOrderedModel):
    """Condition in code covered"""

    number: int = Field(alias="@number")
    type_: str = Field(alias="@type")
    coverage: str = Field(alias="@coverage")


class ConditionXml(BaseOrderedModel):
    """XML list of Conditions"""

    condition: List[Condition]

    _conditions_list_validator = validator("condition", allow_reuse=True, pre=True)(
        list_validator
    )


class Line(BaseOrderedModel):
    """Line in code covered"""

    hits: int = Field(alias="@hits")
    number: int = Field(alias="@number")
    branch: Optional[bool] = Field(alias="branch", default=None)
    condition_coverage: Optional[str] = Field(alias="@condition-coverage", default=None)
    conditions: Optional[ConditionXml] = None


class LineXml(BaseOrderedModel):
    """XML list of Lines"""

    line: List[Line]

    _lines_list_validator = validator("line", allow_reuse=True, pre=True)(
        list_validator
    )


class Method(BaseOrderedModel):
    """Method in code covered"""

    name: str = Field(alias="@name")
    signature: str = Field(alias="@signature")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)


class MethodXml(BaseOrderedModel):
    """XML list of Methods"""

    method: List[Method]

    _methods_list_validator = validator("method", allow_reuse=True, pre=True)(
        list_validator
    )


class Class(BaseOrderedModel):
    """Class in code covered"""

    name: str = Field(alias="@name")
    filename: str = Field(alias="@filename")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    methods: Optional[MethodXml] = None
    lines: Optional[LineXml] = None

    def rewrite_base_dir(self, source_dir: str) -> "Class":
        """Rewrite the base directory of the class

        Class base directory is rewritten relative to current working directory.

        Args:
            source_dir: the directory of the class as in package

        Returns:
            "Class": Class with fixed base dir
        """
        return self.copy(
            update={
                "@filename": str(
                    Path.cwd().relative_to(Path(source_dir).joinpath(self.filename))
                )
            }
        )


class ClassXml(BaseOrderedModel):
    """XML list of Classes"""

    class_: List[Class] = Field(alias="class")

    _class_list_validator = validator("class_", allow_reuse=True, pre=True)(
        list_validator
    )


class Package(BaseOrderedModel):
    """Package in code covered"""

    name: str = Field(alias="@name")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    classes: Optional[ClassXml] = None

    def fix_base_dir(self, source_dir: str) -> "Package":
        """Fix base directory in package.

        Package has classes which are fixed with proper directory.

        Args:
            source_dir: the directory of the class as in package

        Returns:
            "Package": Package with fixed base directory
        """
        if self.classes and self.classes.class_:
            return self.copy(
                update={
                    "classes": ClassXml(
                        **{
                            "class": list(
                                map(
                                    lambda cls_: cls_.rewrite_base_dir(source_dir),
                                    self.classes.class_,
                                )
                            )
                        }
                    )
                }
            )
        return self.copy()


class PackageXml(BaseOrderedModel):
    """XML list of Packages"""

    package: List[Package]

    _package_list_validator = validator("package", allow_reuse=True, pre=True)(
        list_validator
    )

    def __add__(self, other: "PackageXml") -> "PackageXml":
        return PackageXml(package=self.package + other.package)


class Source(BaseOrderedModel):
    """Source of code covered"""

    source: list[str]

    _source_list_validator = validator("source", allow_reuse=True, pre=True)(
        list_validator
    )


class Coverage(BaseOrderedModel):
    """Coverage of code"""

    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    lines_covered: int = Field(alias="@lines-covered")
    lines_valid: int = Field(alias="@lines-valid")
    branches_covered: int = Field(alias="@branches-covered")
    branches_valid: int = Field(alias="@branches-valid")
    complexity: float = Field(alias="@complexity")
    version: str = Field(alias="@version")
    timestamp: int = Field(alias="@timestamp")

    packages: PackageXml
    sources: Optional[Source] = None

    def __add__(self, other: "Coverage") -> "Coverage":
        branches_covered = self.branches_covered + other.branches_covered
        branches_valid = self.branches_valid + other.branches_valid
        branch_rate = (branches_covered / branches_valid) if branches_valid else 0

        lines_covered = self.lines_covered + other.lines_covered
        lines_valid = self.lines_valid + other.lines_valid
        line_rate = (lines_covered / lines_valid) if lines_valid else 0

        complexity = max(self.complexity, other.complexity)
        version = "1.0"
        timestamp = time_ns() // 1_000_000

        package_xml = PackageXml(
            **{"package": self._get_fixed_packages() + other._get_fixed_packages()}
        )

        return Coverage(
            branches_covered=branches_covered,
            branches_valid=branches_valid,
            branch_rate=branch_rate,
            lines_covered=lines_covered,
            lines_valid=lines_valid,
            line_rate=line_rate,
            complexity=complexity,
            version=version,
            timestamp=timestamp,
            sources=Source(source=[Path.cwd()]),
            packages=package_xml,
        )

    def _get_fixed_packages(self) -> List[Package]:
        if self.sources and self.sources.source:
            return [
                pkg.fix_base_dir(self.sources.source[0])
                for pkg in self.packages.package
            ]
        return self.packages.package


class CoverageXml(BaseOrderedModel):
    """Coverage XML File Content"""

    coverage: Coverage

    def __add__(self, other: "CoverageXml") -> "CoverageXml":
        return CoverageXml(coverage=self.coverage + other.coverage)

    @staticmethod
    def read_from_file(input_file: Path) -> "CoverageXml":
        """Read coverage from file.

        Args:
            input_file: coverage xml as Path object.

        Returns:
            "CoverageXml": Coverage object.
        """
        with open(input_file, "rb") as input_fd:
            coverage_dict = parse(input_fd)
            return CoverageXml.parse_obj(obj=coverage_dict)

    @staticmethod
    def merge(coverages: List["CoverageXml"]) -> "CoverageXml":
        """Merge given coverages return merged coverages.

        Args:
            coverages: coverage to be merged.

        Returns:
            CoverageXml: Merged output CoverageXml
        """
        return reduce(add, coverages)

    def output_to_file(self, output_file: Path):
        """Output coverage to output file.

        Args:
            output_file: output file as Path object.
        """
        output_dict = self.dict(exclude_unset=True, by_alias=True)
        with open(output_file, "w", encoding="utf-8") as output_fd:
            unparse(output_dict, output=output_fd, pretty=True)
