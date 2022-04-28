from typing import Iterable
from unittest import TestCase
from itertools import chain

from settings import MAX_ACCEPTED_VALUE
from datatype.captured import CapturedNumber, CapturedCollection


class TestCapturedNumber(TestCase):
    def test_captured_number_default_values(self):
        tests = range(1, MAX_ACCEPTED_VALUE + 1)

        for test in tests:
            captured_number = CapturedNumber(test)
            self.assertIsInstance(captured_number.value, int)
            self.assertEqual(captured_number.value, test)
            self.assertIsInstance(captured_number.count, int)
            self.assertEqual(captured_number.count, 0)
            self.assertIsInstance(captured_number.less, int)
            self.assertEqual(captured_number.less, 0)
            self.assertIsInstance(captured_number.greater, int)
            self.assertEqual(captured_number.greater, 0)


class TestCapturedCollection(TestCase):
    def test_captured_collection_default_values(self):
        captured_collection = CapturedCollection()
        self.assertIsInstance(captured_collection.collection, dict)
        for i in range(1, MAX_ACCEPTED_VALUE + 1):
            self.assertIsInstance(captured_collection[i], CapturedNumber)
            self.assertEqual(captured_collection[i].value, i)

    def test_captured_collection_setitem(self):
        captured_collection = CapturedCollection()
        captured_collection[1] = CapturedNumber(1)
        self.assertIsInstance(captured_collection.collection[1], CapturedNumber)
        self.assertEqual(captured_collection.collection[1].value, 1)

    def test_captured_collection_getitem(self):
        captured_collection = CapturedCollection()
        captured_collection[1] = CapturedNumber(1)
        self.assertIsInstance(captured_collection[1], CapturedNumber)
        self.assertEqual(captured_collection[1].value, 1)

    def test_captured_collection_getitem_error(self):
        captured_collection = CapturedCollection()
        tests = chain(
            range(0, -10, -1),  # Negative numbers
            range(MAX_ACCEPTED_VALUE + 1, MAX_ACCEPTED_VALUE + 10),  # out of range
        )

        for test in tests:
            with self.assertRaises(ValueError):
                captured_collection[test]

    def test_captured_collection_items(self):
        captured_collection = CapturedCollection()
        items = captured_collection.items()

        self.assertIsInstance(items, Iterable)
        for item in items:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], int)
            self.assertIsInstance(item[1], CapturedNumber)
            self.assertEqual(item[0], item[1].value)

    def test_captured_collection_keys(self):
        captured_collection = CapturedCollection()
        keys = captured_collection.keys()

        self.assertIsInstance(keys, Iterable)
        for key in keys:
            self.assertIsInstance(key, int)
            self.assertEqual(key, captured_collection[key].value)
