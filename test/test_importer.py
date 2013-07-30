from unittest import TestCase
from mongoengine import connect
from enem.importer import GradeImporter
from enem.models import City, School, State, Grade

class TestGradeImporter(TestCase):
    def setUp(self):
        self.connection = connect("geekie_test")

        self.state  = State(acronym="SP").save()
        self.city   = City(name="Americana", state="SP", code=20).save()
        self.school = School(name="Politec", state="SP", city_code=20, code=10).save()

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
        self.connection.close()

    def test_school_grade(self):
        school = School.objects.get(code=35058836)

        assertEqual(school.grades["2011"].nature_science[4], 1)
        assertEqual(school.grades["2011"].human_science[4], 1)
        assertEqual(school.grades["2011"].languages[4], 1)
        assertEqual(school.grades["2011"].math[4], 1)

    def test_city_grade(self):
        city = City.objects.get(code=3552403)

        assertEqual(city.grades["2011"].nature_science[4], 1)
        assertEqual(city.grades["2011"].human_science[4], 1)
        assertEqual(city.grades["2011"].languages[4], 1)
        assertEqual(city.grades["2011"].math[4], 1)

    def test_state_grade(self):
        state = State.objects.get(acronym="SP")

        assertEqual(state.grades["2011"].nature_science[4], 1)
        assertEqual(state.grades["2011"].human_science[4], 1)
        assertEqual(state.grades["2011"].languages[4], 1)
        assertEqual(state.grades["2011"].math[4], 1)
