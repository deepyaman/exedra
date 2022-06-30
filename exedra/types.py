from typing import Generic, TypeVar

T = TypeVar("T")


class Dataset:
    ...


class Input(Generic[T]):
    ...


class Output(Generic[T]):
    ...
