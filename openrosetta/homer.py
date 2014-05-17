import requests


class HomerAdapter(object):
    base_url = 'http://opendata-federation.csi.it/fed-homer/documents/select/'

    def proxy(self, **query):
        r = requests.get(self.base_url, **query)
        return r.json()

homer_adapter = HomerAdapter()
