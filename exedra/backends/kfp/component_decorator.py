# Mypy doesn't use ``typing`` from the standard library; it uses the one
# from typeshed. ``_GenericAlias`` is missing from the .pyi in typeshed.
# To understand why, see https://github.com/python/typeshed/issues/4694.
from typing import Callable, _GenericAlias  # type: ignore[attr-defined]

import kfp.dsl
from kfp.components import python_component

from exedra.types import Dataset, Input, Output

TYPE_MAPPING = {
    Dataset: kfp.dsl.Dataset,
    Input: kfp.dsl.Input,
    Output: kfp.dsl.Output,
}


def _map_annotation(annotation: _GenericAlias) -> _GenericAlias:
    return TYPE_MAPPING[annotation.__origin__][TYPE_MAPPING[annotation.__args__[0]]]


def component(func: Callable) -> python_component.PythonComponent:
    func.__annotations__ = {
        name: _map_annotation(value) for name, value in func.__annotations__.items()
    }
    return kfp.dsl.component(func)
