from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

from error.message import ERROR_OUT_OF_RANGE
from settings import MAX_ACCEPTED_VALUE


@dataclass()
class CapturedNumber:
    def __init__(self, value: int):
        """
        Initializes the captured number.
        """
        self.value: int = value
        self.less: int = 0
        self.greater: int = 0
        self.count: int = 0

    def __str__(self):
        """
        Returns a string representation of the CapturedNumber object.
        """
        return str(
            {
                "value": self.value,
                "less": self.less,
                "greater": self.greater,
                "count": self.count,
            }
        )

    def __repr__(self):
        """
        Returns a string representation of the CapturedNumber object.
        """
        return f"CapturedNumber(value={self.value}, less={self.less}, greater={self.greater}, count={self.count})"


@dataclass()
class CapturedCollection:
    def __init__(self) -> None:
        """
        Initializes the collection
        """
        self.collection: dict[int, CapturedNumber] = {}
        self.current_iteration: int = 0

    def __iter__(self) -> CapturedCollection:
        """
        Returns an iterator of the stats.
        """
        return self

    def __next__(self) -> CapturedNumber:
        """
        Returns the next iteration lower than MAX_ACCEPTED_VALUE.
        """
        while self.current_iteration < MAX_ACCEPTED_VALUE:
            self.current_iteration += 1
            if self.current_iteration not in self.collection:
                return CapturedNumber(self.current_iteration)
            else:
                return self.collection[self.current_iteration]

        self.current_iteration = 0
        raise StopIteration

    def __repr__(self) -> str:
        """
        Returns a string representation of the CapturedCollection object.
        """
        return repr(self.collection)

    def __setitem__(self, key: int, value: CapturedNumber) -> None:
        """
        Sets the value of the key to the value
        """
        if key < 1 or key > MAX_ACCEPTED_VALUE:
            raise ValueError(ERROR_OUT_OF_RANGE.format(number=key))
        self.collection[key] = value

    def __getitem__(self, key: int) -> CapturedNumber:
        """
        Returns the CapturedNumber associated with the key
        """
        if key < 1 or key > MAX_ACCEPTED_VALUE:
            raise ValueError(ERROR_OUT_OF_RANGE.format(number=key))
        if key not in self.collection:
            self.collection[key] = CapturedNumber(key)
        return self.collection[key]

    def __len__(self) -> int:
        """
        Returns the length of the collection
        """
        return len(self.collection)

    def items(self) -> Iterable[tuple[int, CapturedNumber]]:
        """
        Returns a list of tuples of the form (key, value)
        """
        return self.collection.items()

    def keys(self) -> Iterable[int]:
        """
        Returns a list of keys
        """
        return self.collection.keys()
