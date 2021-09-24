"""Types for Coverage File

Spec: https://github.com/cobertura/web/blob/master/htdocs/xml/coverage-04.dtd

Some amount of liberty is added by allowing optionals
"""
from typing import List, Optional, TypeVar, Union

from pydantic import BaseModel, Field, validator

ListContent = TypeVar("ListContent")


def list_validator(
    input_value: Optional[Union[List[ListContent], ListContent]]
) -> List[ListContent]:
    """Add list validation for XML fields

    xmltodict library captures list in various ways:
        - null if nothing is provided
        - content if only one content is provided
        - list in other cases

    To fix this list validator convert the value in to appropriate type.

    Args:
        input_value: input as extracted from xmltodict

    Returns:
        List[ListContent]: corrected list
    """

    if input_value is None:
        output_value = []
    elif not isinstance(input_value, list):
        output_value = [input_value]
    else:
        output_value = input_value
    return output_value


class Condition(BaseModel):
    """Condition in code covered"""

    number: int = Field(alias="@number")
    type_: str = Field(alias="@type")
    coverage: str = Field(alias="@coverage")


class ConditionXml(BaseModel):
    """XML list of Conditions"""

    condition: List[Condition]

    _conditions_list_validator = validator("condition", allow_reuse=True, pre=True)(
        list_validator
    )


class Line(BaseModel):
    """Line in code covered"""

    hits: int = Field(alias="@hits")
    number: int = Field(alias="@number")
    branch: Optional[bool] = Field(alias="branch", default=None)
    condition_coverage: Optional[str] = Field(alias="@condition-coverage", default=None)
    conditions: Optional[ConditionXml] = None


class LineXml(BaseModel):
    """XML list of Lines"""

    line: List[Line]

    _lines_list_validator = validator("line", allow_reuse=True, pre=True)(
        list_validator
    )


class Method(BaseModel):
    """Method in code covered"""

    name: str = Field(alias="@name")
    signature: str = Field(alias="@signature")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)


class MethodXml(BaseModel):
    """XML list of Methods"""

    method: List[Method]

    _methods_list_validator = validator("method", allow_reuse=True, pre=True)(
        list_validator
    )


class Class(BaseModel):
    """Class in code covered"""

    name: str = Field(alias="@name")
    filename: str = Field(alias="@filename")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    methods: Optional[MethodXml] = None
    lines: Optional[LineXml] = None


class ClassXml(BaseModel):
    """XML list of Classes"""

    class_: List[Class] = Field(alias="class")

    _class_list_validator = validator("class_", allow_reuse=True, pre=True)(
        list_validator
    )


class Package(BaseModel):
    """Package in code covered"""

    name: str = Field(alias="@name")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    classes: Optional[ClassXml] = None


class PackageXml(BaseModel):
    """XML list of Packages"""

    package: List[Package]

    _package_list_validator = validator("package", allow_reuse=True, pre=True)(
        list_validator
    )


class Source(BaseModel):
    """Source of code covered"""

    source: list[str]

    _source_list_validator = validator("source", allow_reuse=True, pre=True)(
        list_validator
    )


class Coverage(BaseModel):
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


class CoverageXml(BaseModel):
    """Coverage XML File Content"""

    coverage: Coverage
