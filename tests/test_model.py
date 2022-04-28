from unittest import TestCase

from datatype.captured import CapturedCollection, CapturedNumber
from model.stats import DataCapture, Stats
from settings import MAX_ACCEPTED_VALUE


class TestDataCapture(TestCase):
    def test_init(self):
        datacapture = DataCapture()
        self.assertIsInstance(datacapture, DataCapture)
        self.assertIsInstance(datacapture.count, int)
        self.assertIsInstance(datacapture.data, CapturedCollection)
        self.assertEqual(datacapture.count, 0)
        self.assertEqual(len(datacapture.data), 0)

    def test_add(self):
        for i in range(1, MAX_ACCEPTED_VALUE + 1):
            datacapture = DataCapture()
            datacapture.add(i)
            self.assertEqual(datacapture.count, 1)
            self.assertEqual(len(datacapture.data), 1)
            self.assertEqual(datacapture.data[i].value, i)

    def test_build_stats(self):
        datacapture = DataCapture()
        for i in range(1, MAX_ACCEPTED_VALUE + 1):
            datacapture.add(i)
        stats = datacapture.build_stats()
        self.assertIsInstance(stats, Stats)


class TestStats(TestCase):
    def test_init(self):
        stats = Stats(10)
        self.assertIsInstance(stats, Stats)
        self.assertIsInstance(stats.count, int)
        self.assertIsInstance(stats.data, CapturedCollection)
        self.assertEqual(stats.count, 10)
        self.assertEqual(len(stats.data), 0)

    def test_setitem(self):
        stats = Stats(10)
        stats[1] = CapturedNumber(1)
        self.assertEqual(len(stats.data), 1)
        self.assertEqual(stats.data[1].value, 1)

    def test_getitem(self):
        stats = Stats(10)
        stats[1] = CapturedNumber(1)
        self.assertEqual(stats[1].value, 1)

    def test_keys(self):
        stats = Stats(10)
        stats[1] = CapturedNumber(1)
        stats[2] = CapturedNumber(2)
        self.assertEqual(list(stats.keys()), [1, 2])

    def test_less(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests_and_results": (
                    (4, 2),
                    (5, 3),  # Note: 5 is not in the list
                    (6, 3),
                    (9, 4),
                ),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            with self.subTest(
                test=test["tests_and_results"][0], result=test["tests_and_results"][1]
            ):
                for number, result in test["tests_and_results"]:
                    self.assertEqual(stats.less(number), result)

    def test_less_error(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests": (-5, 0, 1000, 9999),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            for number in test["tests"]:
                with self.subTest(test=number):
                    with self.assertRaises(ValueError):
                        stats.less(number)

    def test_greater(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests_and_results": (
                    (4, 2),
                    (5, 2),  # Note: 5 is not in the list
                    (6, 1),
                    (9, 0),
                ),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            with self.subTest(
                test=test["tests_and_results"][0], result=test["tests_and_results"][1]
            ):
                for number, result in test["tests_and_results"]:
                    self.assertEqual(stats.greater(number), result)

    def test_greater_error(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests": (-5, 0, 1000, 9999),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            for number in test["tests"]:
                with self.subTest(test=number):
                    with self.assertRaises(ValueError):
                        stats.greater(number)

    def test_between(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests_and_results": (
                    ((3, 6), 4),
                    ((4, 8), 2),
                    ((1, 2), 0),
                    ((5, 2), 3),  # Note: the highest number comes first
                ),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            with self.subTest(
                test=test["tests_and_results"][0], result=test["tests_and_results"][1]
            ):
                for numbers, result in test["tests_and_results"]:
                    self.assertEqual(stats.between(*numbers), result)

    def test_between_error(self):
        tests = [
            {
                "numbers": (3, 9, 3, 4, 6),
                "tests": ((-5, 5), (5, 0), (11, 1000), (1001, 300), (0, 1000)),
            },
        ]

        for test in tests:
            stats = self._prepare_stats(test["numbers"])
            for numbers in test["tests"]:
                with self.subTest(test=numbers):
                    with self.assertRaises(ValueError):
                        stats.between(*numbers)

    def _prepare_stats(self, numbers):
        datacapture = DataCapture()
        for number in numbers:
            datacapture.add(number)

        return datacapture.build_stats()
