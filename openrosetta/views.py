""" Cornice services.
"""
from cornice import Service
from openrosetta.plugins.csv_plugin import dictify
from openrosetta.plugins.smeagol.data_fetcher import DataFetcher

hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    #dictify()
    df = DataFetcher("sqlite:///test", "/files/")
    df.test()# do not cal test call self.fetch_data([list of urls to download])

    return {'Hello': 'World'}
