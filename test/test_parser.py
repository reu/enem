from unittest import TestCase
from enem.parser import parse_line, parse_file

class TestParseValidLine(TestCase):
    def setUp(self):
        with open("./test/ENEM_fixture.txt") as file:
            first_line = file.readline()
            self.result = parse_line(first_line)

    def test_year(self):
        self.assertEqual(self.result["year"], 2011)

    def test_school(self):
        self.assertEqual(self.result["school"], 35058836)

    def test_city_code(self):
        self.assertEqual(self.result["city"], 3552403)

    def test_city_name(self):
        self.assertEqual(self.result["city_name"], "SUMARE")

    def test_state(self):
        self.assertEqual(self.result["state"], "SP")

    def test_nature_science_grade(self):
        self.assertEqual(self.result["nature_science_grade"], 543.3)

    def test_human_science_grade(self):
        self.assertEqual(self.result["human_science_grade"], 542.8)

    def test_languages_grade(self):
        self.assertEqual(self.result["languages_grade"], 585.0)

    def test_math_grade(self):
        self.assertEqual(self.result["math_grade"], 559.2)

class TestParseInvalidLine(TestCase):
    def test_year(self):
        with self.assertRaises(Exception):
            parse_line("invalid")

class TestParseFile(TestCase):
    def test_parses_the_first_line(self):
        with open("./test/ENEM_fixture.txt") as file:
            for result in parse_file(file):
                self.assertIsInstance(result, dict)

    # TODO: find a way to use mocks in python 2
    def test_ignores_invalid_lines(self):
        count = 0

        # Second line is invalid
        with open("./test/ENEM_fixture.txt") as file:
            for result in parse_file(file):
                count += 1

        # The iterator should only yield data one time
        self.assertEqual(count, 1)
