from mongoengine import *

class _FrequencyField(DictField):
    """A custom mongoengine field which stores histogram frequencies."""

    def __init__(self, field=None, *args, **kwargs):
        empty_frequency = { str(key): 0 for key in range(10) }
        super(_FrequencyField, self).__init__(field=field, default=empty_frequency, *args, **kwargs)

class Grade(EmbeddedDocument):
    nature_science = _FrequencyField(required=True)
    human_science = _FrequencyField(required=True)
    languages = _FrequencyField(required=True)
    math = _FrequencyField(required=True)

class _Gradeable(object):
    """
    Defines a gradeable object structure.

    Example:
        {
            grades: {
                "2009": {
                    nature_science: { "0": 10, "1": 4, "2": 5, "3": 10, "4": 100, "5": 150, "6": 30, "7": 50, "8": 90, "9": 1 }
                    ...
                },
                "2010": {
                    ...
                }
                ...
            }
        }
    """
    grades = MapField(field=EmbeddedDocumentField(Grade))

class State(Document, _Gradeable):
    acronym = StringField(required=True, unique=True)

    meta = {"indexes": [{"fields": ["acronym"], "unique": True }]}

class City(Document, _Gradeable):
    name = StringField(required=True)
    state = StringField(required=True)
    code = IntField(required=True, unique=True)

    meta = {"indexes": [{"fields": ["code"], "unique": True },
                        {"fields": ["state", "name"]}]}

class School(Document, _Gradeable):
    name = StringField(required=True)
    code = IntField(required=True, unique=True)
    city_code = IntField(required=True)
    state = StringField(required=True)

    meta = {"indexes": [{"fields": ["code"], "unique": True },
                        {"fields": ["state", "city_code", "name"]}]}
