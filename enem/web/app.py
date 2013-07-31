from flask import Flask, render_template, jsonify
from os import environ
from mongoengine import connect
from mongoengine.queryset import DoesNotExist
from ..models import State, City, School

connect("geekie_development", host=environ.get("MONGO_URL", "localhost"))

app = Flask(__name__, static_url_path="")

@app.route("/")
def histograms():
    return render_template("histograms.html.jinja2",
                           schools=School.objects.order_by("name"),
                           cities=City.objects.order_by("name"))

@app.route("/cities/<int:city_code>")
@app.route("/cities/<int:city_code>/<int:year>/area")
def city_histogram(city_code, year=2011, area="math"):
    try:
        city   = City.objects.get(code=city_code)
        grades = city.grades[str(year)][area]

        return jsonify(name=city.name,
                       grades=grades,
                       relativeGrades=[x * 100 / sum(grades) for x in grades])
    except DoesNotExist, KeyError:
        return "Not found", 404

@app.route("/schools/<int:school_code>")
@app.route("/schools/<int:school_code>/<int:year>/<area>")
def school_histogram(school_code, year=2011, area="math"):
    try:
      school = School.objects.get(code=school_code)
      grades = school.grades[str(year)][area]

      return jsonify(name=school.name,
                     grades=grades,
                     relativeGrades=[x * 100 / sum(grades) for x in grades])
    except DoesNotExist, KeyError:
        return "Not found", 404

if __name__ == "__main__":
    app.run()
