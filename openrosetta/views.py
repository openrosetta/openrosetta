""" Cornice services.
"""
from cornice import Service
from openrosetta.plugins.csv_plugin import dictify


hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    dictify()
    return {'Hello': 'World'}
