from openrosetta.models import Dataset, HomerQ
from pyramid.threadlocal import get_current_request
import requests


class HomerAdapter(object):
    base_url = 'http://opendata-federation.csi.it/fed-homer/documents/select/'

    @property
    def request(self):
        return get_current_request()

    def proxy(self, **query):
        r = requests.get(self.base_url, params=query)
        r = r.json()
        homer_q = HomerQ.query.find({'q': query}).first()
        if homer_q is None:
            homer_q = HomerQ(q=query)
        for i, ds in enumerate(r['response'].get('docs', [])):
            r['response']['docs'][i]['babylon_url'] = self.babylon_ds(ds, homer_q)
        return r

    def babylon_ds(self, dataset, homer_q):
        metadata_origin = dataset.get('metadata_origin')
        if not metadata_origin:
            return None
        stored_ds = Dataset.query.find({'metadata_origin': metadata_origin}).first()
        if stored_ds is None:
            stored_ds = Dataset(metadata_origin=metadata_origin, homer_q_id=homer_q._id)
        return '/'.join([self.request.application_url, 'babylon', str(stored_ds._id)])


homer_adapter = HomerAdapter()
