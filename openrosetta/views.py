""" Cornice services.
"""
from bson import ObjectId
from bson.errors import InvalidId
from colander import MappingSchema, SchemaNode, String, OneOf, Integer
from openrosetta.config import RService
from openrosetta.homer import homer_adapter
from openrosetta.models import Dataset
from pyramid.httpexceptions import HTTPNotFound
from openrosetta.plugins.smeagol.data_fetcher import DataFetcher


class HomerSchema(MappingSchema):
    q = SchemaNode(String(), location='querystring')
    lang = SchemaNode(String(), location='querystring')
    wt = SchemaNode(String(), location='querystring', missing='json', validator=OneOf(['json']))
    start = SchemaNode(Integer(), location='querystring')
    rows = SchemaNode(Integer(), location='querystring')


class BabilonIdSchema(MappingSchema):
    id = SchemaNode(String(), location='path')


hello = RService(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""

    #dictify()
    df = DataFetcher()
    df.test()  # do not cal test call self.fetch_data([list of urls to download])


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
