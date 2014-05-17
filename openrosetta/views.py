""" Cornice services.
"""
from cornice import Service
from openrosetta.plugins.xls_plugin import dictify


hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}
