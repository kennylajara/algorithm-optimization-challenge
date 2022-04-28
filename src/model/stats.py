import re
from typing import Iterable

from datatype.captured import CapturedNumber, CapturedCollection
from settings import MAX_ACCEPTED_VALUE


class Stats:
    def __init__(self, count: int) -> None:
        """
        Initializes the stats.
        """
        self._data: CapturedCollection = CapturedCollection()
        self._count: int = count

    def __repr__(self) -> str:
        """
        Returns the stats as a string.
        """
        return f"Stats(stats={[repr(self._data)]}, count={self._count})"

    def __setitem__(self, key: int, item: CapturedNumber) -> None:
        """
        Sets the captured number for the given key.
        """
        self._data[key] = item

    def __getitem__(self, key: int) -> CapturedNumber:
        """
        Returns the captured number for the given key.
        """
        return self._data[key]

    @property
    def count(self) -> int:
        """
        Returns the number of numbers captured.
        """
        return self._count

    @property
    def data(self) -> CapturedCollection:
        """
        Returns the stats.
        """
        return self._data

    def between(self, a: int, b: int) -> int:
        """
        Returns the number of numbers between the two given numbers.
        """
        if a < b:
            lowest, highest = a, b
        else:
            lowest, highest = b, a

        return self._count - self._data[lowest].less - self._data[highest].greater

    def greater(self, number: int) -> int:
        """
        Returns the number of numbers greater than the given number.
        """
        return self._data[number].greater

    def keys(self) -> Iterable[int]:
        """
        Returns a list of all the keys in the stats.
        """
        return self._data.keys()

    def less(self, number: int) -> int:
        """
        Returns the number of numbers less than the given number.
        """
        return self._data[number].less


class DataCapture:
    def __init__(self):
        """
        Initializes the data capture.
        """
        self.count: int = 0
        self.data: CapturedCollection = CapturedCollection()

    def add(self, number: int) -> None:
        """
        Adds the given number to the data capture.
        """
        if number not in self.data.keys():
            self.data[number] = CapturedNumber(number)
        self.data[number].count += 1
        self.count += 1

    def build_stats(self) -> Stats:
        """
        Builds the stats from the data capture.
        """
        stats: Stats = Stats(self.count)
        less: int = 0
        greater: int = self.count

        for captured_number in self.data:
            stats[captured_number.value].count = captured_number.count
            stats[captured_number.value].less = less
            stats[captured_number.value].greater = greater - captured_number.count
            less += captured_number.count
            greater -= captured_number.count

        return stats
