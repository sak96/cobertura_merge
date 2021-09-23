from pydantic import BaseModel, Field, validator
from typing import List, Optional, Any, Union, TypeVar

ListContent = TypeVar("ListContent")


def list_validator(value: Union[List[ListContent], ListContent]) -> List[ListContent]:
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


class Condition(BaseModel):
    number: int = Field(alias="@number")
    type_: str = Field(alias="@type")
    coverage: str = Field(alias="@coverage")


class ConditionXml(BaseModel):
    condition: List[Condition]

    _conditions_list_validator = validator("condition", allow_reuse=True, pre=True)(
        list_validator
    )


class Line(BaseModel):
    hits: int = Field(alias="@hits")
    number: int = Field(alias="@number")
    branch: Optional[bool] = Field(alias="branch", default=None)
    conditon_coverage: Optional[str] = Field(alias="@conditon-coverage", default=None)
    conditions: Optional[ConditionXml] = None


class LineXml(BaseModel):
    line: List[Line]

    _lines_list_validator = validator("line", allow_reuse=True, pre=True)(
        list_validator
    )


class Method(BaseModel):
    name: str = Field(alias="@name")
    signature: str = Field(alias="@signature")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)


class MethodXml(BaseModel):
    method: List[Method]

    _methods_list_validator = validator("method", allow_reuse=True, pre=True)(
        list_validator
    )


class Class(BaseModel):
    name: str = Field(alias="@name")
    filename: str = Field(alias="@filename")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    methods: Optional[MethodXml] = None
    lines: Optional[LineXml] = None


class ClassXml(BaseModel):
    class_: List[Class] = Field(alias="class")

    _class_list_validator = validator("class_", allow_reuse=True, pre=True)(
        list_validator
    )


class Package(BaseModel):
    name: str = Field(alias="@name")
    line_rate: float = Field(alias="@line-rate")
    branch_rate: float = Field(alias="@branch-rate")
    complexity: Optional[float] = Field(alias="@complexity", default=None)
    classes: Optional[ClassXml] = None


class PackageXml(BaseModel):
    package: List[Package]

    _package_list_validator = validator("package", allow_reuse=True, pre=True)(
        list_validator
    )


class Source(BaseModel):
    source: list[str]

    _source_list_validator = validator("source", allow_reuse=True, pre=True)(
        list_validator
    )


class Coverage(BaseModel):
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
    coverage: Coverage
