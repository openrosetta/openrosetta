""" Cornice services.
"""
from bson import ObjectId
from bson.errors import InvalidId
from colander import MappingSchema, SchemaNode, String, OneOf, Integer
from openrosetta.config import RService
from openrosetta.homer import homer_adapter
from openrosetta.models import Dataset
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


class HomerSchema(MappingSchema):
    q = SchemaNode(String(), location='querystring')
    lang = SchemaNode(String(), location='querystring')
    wt = SchemaNode(String(), location='querystring', missing='json', validator=OneOf(['json']))
    start = SchemaNode(Integer(), location='querystring')
    rows = SchemaNode(Integer(), location='querystring')


class BabilonIdSchema(MappingSchema):
    id = SchemaNode(String(), location='path')


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'one': 'one', 'project': '{{project}}'}


homer = RService(name='homer', path='/homer', description='Homer endpoint proxy')


@homer.get(schema=HomerSchema)
def get_homer(request):
    return homer_adapter.proxy(**request.validated)


babylon = RService(name='babylon', path='/babylon/{id}', description='Babylon')


@babylon.get(schema=BabilonIdSchema)
def get_babylon(request):
    try:
        dataset = Dataset.query.get(_id=ObjectId(request.validated['id']))
        assert dataset is not None
    except (InvalidId, AssertionError):
        raise HTTPNotFound

    data = homer_adapter.data_from_meta(dataset.metadata_origin)

    return {'data': data}
