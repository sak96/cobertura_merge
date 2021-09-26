"""Types for Coverage File

Spec: https://github.com/cobertura/web/blob/master/htdocs/xml/coverage-04.dtd

Some amount of liberty is added by allowing optionals
"""
from typing import List, Optional

from pydantic import Field, validator

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


class PackageXml(BaseOrderedModel):
    """XML list of Packages"""

    package: List[Package]

    _package_list_validator = validator("package", allow_reuse=True, pre=True)(
        list_validator
    )


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


class CoverageXml(BaseOrderedModel):
    """Coverage XML File Content"""

    coverage: Coverage
