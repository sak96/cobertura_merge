"""Types Helpers for Coverage File"""
from collections import OrderedDict
from typing import TYPE_CHECKING, List, Optional, TypeVar, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny


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


class BaseOrderedModel(BaseModel):
    """Base Ordered Model which returns ordered dict"""

    def dict(self, *args, by_alias: bool = False, **kwargs) -> "DictStrAny":
        """Order the dict keys in output dict.

        Ordered dict keys in output dict.
        The order is used as per order of fields definition.
        This order is fetched using __fields_set__.

        Args:
            *args: pass arguments to super dict.
            by_alias: use alias instead name.
            **kwargs: pass keyword arguments to super dict.

        Returns:
            "DictStrAny": dictionary with ordered keys.
        """
        return OrderedDict(
            sorted(
                super().dict(*args, by_alias=by_alias, **kwargs).items(),
                key=lambda item: list(
                    map(
                        lambda item: (by_alias and item[1].alias) or item[1].name,
                        self.__fields__.items(),
                    )
                ).index(item[0]),
            )
        )
