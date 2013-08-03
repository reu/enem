import csv
import logging
import sys
from multiprocessing.queues import Queue
from multiprocessing import Process
from enem.parser import parse_line
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
    def __init__(self, workers_count=10):
        self.workers_count = workers_count

    def import_file(self, file):
        self._import_schools(file)
        self._import_cities()
        self._import_states()

    def _import_schools(self, file):
        data_queue = Queue(100)
        workers = list()

        for i in range(self.workers_count):
            worker = Process(target=self._process_schools, args=(data_queue, ))
            workers.append(worker)
            worker.start()

        for line in file: data_queue.put(line)

        while True:
            if data_queue.empty():
                for worker in workers:
                    worker.terminate()
                break

    def _process_schools(self, queue):
        while True:
            data = parse_line(queue.get())
            if data is None: continue

            year = data["year"]

            ns_range = self._range_for_grade(data["nature_science_grade"])
            hs_range = self._range_for_grade(data["human_science_grade"])
            ln_range = self._range_for_grade(data["languages_grade"])
            mt_range = self._range_for_grade(data["math_grade"])

            School.objects(code=data["school"]).update(**{
                      "inc__grades__{}__nature_science__{}".format(year, ns_range): 1,
                      "inc__grades__{}__human_science__{}".format(year, hs_range): 1,
                      "inc__grades__{}__languages__{}".format(year, ln_range): 1,
                      "inc__grades__{}__math__{}".format(year, mt_range): 1
                  })

    def _import_cities(self):
        for city in City.objects:
            for school in School.objects(city_code=city.code):
                for subject in ["nature_science", "human_science", "languages", "math"]:
                    try:
                      grades = school.grades["2011"][subject]
                      for range in grades.keys():
                          city.update(**{"inc__grades__2011__{}__{}".format(subject, range): grades[range]})
                    except KeyError:
                        continue

    def _import_states(self):
        for state in State.objects:
            for city in City.objects(state=state.acronym):
                for subject in ["nature_science", "human_science", "languages", "math"]:
                    try:
                      grades = city.grades["2011"][subject]
                      for range in grades.keys():
                          state.update(**{"inc__grades__2011__{}__{}".format(subject, range): grades[range]})
                    except KeyError:
                        continue

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

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")

    if options.schools and options.enem:
        parser.error("You can import a schools file OR a ENEM grade file")

    connect("geekie_development", host=environ.get("MONGO_URL", "localhost"))

    if options.schools: importer = SchoolImporter()
    if options.enem:    importer = MultiProcessSchoolImporter(10)

    with open(args[0]) as file: importer.import_file(file)
