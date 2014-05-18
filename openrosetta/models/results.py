from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass
from openrosetta.models import DBSession

__author__ = 'simock85'


class Result(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'results'

    _id = FieldProperty(s.ObjectId)
    url = FieldProperty(s.String)
    result = FieldProperty(s.String)
