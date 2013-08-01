from unittest import TestCase
from mongoengine import connect
from enem.importer import GradeImporter
from enem.models import City, School, State, Grade

connect("geekie_test")

class TestGradeImporter(TestCase):
    def setUp(self):
        (self.state, _)  = State.objects.get_or_create(acronym="SP")
        (self.city, _)   = City.objects.get_or_create(name="Americana", state="SP", code=20)
        (self.school, _) = School.objects.get_or_create(name="Politec", state="SP", city_code=20, code=10)

        result = dict(year=2011,
                      school=10,
                      city=20,
                      state="SP",
                      nature_science_grade=40,
                      human_science_grade=300,
                      languages_grade=867,
                      math_grade=1000
                      )

        importer =GradeImporter()
        importer.process(result)

    def tearDown(self):
        self.state.delete()
        self.city.delete()
        self.school.delete()

    def test_school_grade(self):
        school = School.objects.get(code=10)

        self.assertEqual(school.grades["2011"].nature_science[0], 1)
        self.assertEqual(school.grades["2011"].human_science[3], 1)
        self.assertEqual(school.grades["2011"].languages[8], 1)
        self.assertEqual(school.grades["2011"].math[9], 1)

    def test_city_grade(self):
        city = City.objects.get(code=20)

        self.assertEqual(city.grades["2011"].nature_science[0], 1)
        self.assertEqual(city.grades["2011"].human_science[3], 1)
        self.assertEqual(city.grades["2011"].languages[8], 1)
        self.assertEqual(city.grades["2011"].math[9], 1)

    def test_state_grade(self):
        state = State.objects.get(acronym="SP")

        self.assertEqual(state.grades["2011"].nature_science[0], 1)
        self.assertEqual(state.grades["2011"].human_science[3], 1)
        self.assertEqual(state.grades["2011"].languages[8], 1)
        self.assertEqual(state.grades["2011"].math[9], 1)
