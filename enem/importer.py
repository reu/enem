import csv
import logging
import sys
from enem.parser import parse_file
from enem.models import City, School, State, Grade

class Importer(object):
    def __init__(self, logger=logging.getLogger("enem.importer")):
        # Initialize a stdout logger
        self.logger = logger
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

    def log(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

class SchoolImporter(Importer):
    def process(self, data):
        (state, created) = State.objects.get_or_create(acronym=data[0])
        (city, created) = City.objects.get_or_create(code=data[1], defaults={"name": data[2], "state": data[0]})
        (school, created) = School.objects.get_or_create(code=data[3], defaults={"name": data[4], "state": data[0], "city_code": data[1]})

    def import_file(self, file):
        self.log("Importing schools from file {}".format(file.name))

        count = 0
        for line in csv.reader(file, delimiter=","):
            self.process(line)
            count += 1

        self.log("{} schools imported.".format(count))

class GradeImporter(Importer):
    def process(self, data):
        # Warning: Naive non thread-safe code above
        school = self._get_school(data["school"])
        city   = self._get_city(data["city"])
        state  = self._get_state(data["state"])

        ns_range = self._range_for_grade(data["nature_science_grade"])
        hs_range = self._range_for_grade(data["human_science_grade"])
        ln_range = self._range_for_grade(data["languages_grade"])
        mt_range = self._range_for_grade(data["math_grade"])

        for gradeable in [school, city, state]:
            try:
                grade = gradeable.grades[str(data["year"])]
            except KeyError:
                grade = gradeable.grades[str(data["year"])] = Grade()

            grade.nature_science[ns_range] += 1
            grade.human_science[hs_range] += 1
            grade.languages[ln_range] += 1
            grade.math[mt_range] += 1

            gradeable.save()

    def import_file(self, file):
        self.log("Importing ENEM grades from file {}".format(file.name))

        count, fail = 0, 0
        for result in parse_file(file):
            try:
                self.process(result)
                self.debug("{} {} {} {} {} {} {}".format(result["state"],
                                                         result["city"],
                                                         result["school"],
                                                         result["nature_science_grade"],
                                                         result["human_science_grade"],
                                                         result["languages_grade"],
                                                         result["math_grade"]))
            except Exception:
                self.log("error importing line")
                fail += 1

            count += 1

        self.log("{} ENEM grades imported. {} failed.".format(count - fail, fail))

    def _get_school(self, school_code):
        return School.objects.get(code=school_code)

    def _get_city(self, city_code):
        return City.objects.get(code=city_code)

    def _get_state(self, acronym):
        return State.objects.get(acronym=acronym)

    def _range_for_grade(self, grade):
        # The geniuses who got 1000 are put in the same group of the
        # not-so-geniouses-but-yet-very-smart-people who got 900.01-999.99
        if grade < 1000:
            return int(grade) / 100
        else:
            return 9

if __name__ == "__main__":
    from os import environ
    from mongoengine import connect
    from optparse import OptionParser

    parser = OptionParser(usage="enem.importer [options] <filename>")
    parser.add_option("-s", "--schools", action="store_true", dest="schools", help="Import schools file")
    parser.add_option("-e", "--enem", action="store_true", dest="enem", help="Import ENEM grades file")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose mode")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")

    if options.schools and options.enem:
        parser.error("You can import a schools file OR a ENEM grade file")

    connect(environ.get("MONGO_URL", "geekie_development"))

    if options.schools: importer = SchoolImporter()
    if options.enem:    importer = GradeImporter()

    if options.verbose:
        importer.logger.level = logging.DEBUG
    else:
        importer.logger.level = logging.INFO

    with open(args[0]) as file: importer.import_file(file)
