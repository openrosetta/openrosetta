""" Cornice services.
"""
from colander import MappingSchema, SchemaNode, String, OneOf, Integer
from cornice import Service
from openrosetta.homer import homer_adapter


class HomerSchema(MappingSchema):
    q = SchemaNode(String(), location='querystring')
    lang = SchemaNode(String(), location='querystring')
    wt = SchemaNode(String(), location='querystring', missing='json', validator=OneOf(['json']))
    start = SchemaNode(Integer(), location='querystring')
    rows = SchemaNode(Integer(), location='querystring')


hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


homer = Service(name='homer', path='/homer', description='Homer endpoint proxy')


@homer.get(schema=HomerSchema)
def get_homer(request):
    return homer_adapter.proxy(params=request.validated)
