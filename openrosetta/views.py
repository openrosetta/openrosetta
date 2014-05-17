""" Cornice services.
"""
from cornice import Service


hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


homer = Service(name='homer', path='/homer', description='Homer endpoint proxy')

@homer.get()
def homer(request):
    pass
