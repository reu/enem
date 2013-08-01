from mongoengine import *

class _FrequenceField(ListField):
    """A custom mongoengine field which stores histogram frequencies."""

    def __init__(self, field=None, *args, **kwargs):
        empty_frequence = [0 for x in xrange(10)]
        super(_FrequenceField, self).__init__(field=field, default=empty_frequence, *args, **kwargs)

class Grade(EmbeddedDocument):
    nature_science = _FrequenceField(required=True)
    human_science = _FrequenceField(required=True)
    languages = _FrequenceField(required=True)
    math = _FrequenceField(required=True)

class _Gradeable(object):
    """
    Defines a gradeable object structure.

    Example:
        {
            grades: {
                "2009": {
                    nature_science: [100, 32, 43, 21, 344, 21, 332, 44, 543, 112],
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
