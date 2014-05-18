from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from openrosetta.models import DBSession


class HomerQ(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'homer_q'

    _id = FieldProperty(s.ObjectId)
    q = FieldProperty(s.Anything, index=True)
    datasets = RelationProperty('Dataset')


class Dataset(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'datasets'

    _id = FieldProperty(s.ObjectId)
    homer_q_id = ForeignIdProperty(HomerQ)
    homer_q = RelationProperty(HomerQ)
    metadata_origin = FieldProperty(s.String, index=True)