from xml.etree import ElementTree
from cStringIO import StringIO
from openrosetta.models import Dataset, HomerQ
from openrosetta.plugins.csv_plugin import dictify
from pyramid.httpexceptions import HTTPNotFound
from pyramid.threadlocal import get_current_request
import requests
import simplejson as json


class IDataUrl(object):
    def get_urls(self, meta):
        raise NotImplementedError


class XmlDataUrl(IDataUrl):
    def get_urls(self, meta):
        urls = []
        root = ElementTree.fromstring(meta)
        for resource in root.find('resources').findall('resource'):
            urls.append(resource.find('url').text)
        return urls


class JsonDataUrl(IDataUrl):
    def get_urls(self, meta):
        meta = json.loads(meta)
        resources = meta.get('resources', [])
        return [r.get('url') for r in resources]


mime_mapping = {
    'json': JsonDataUrl,
    'xml': XmlDataUrl
}


class HomerAdapter(object):
    base_url = 'http://opendata-federation.csi.it/fed-homer/documents/select/'

    @property
    def request(self):
        return get_current_request()

    def proxy(self, **query):
        r = requests.get(self.base_url, params=query)
        try:
            r = r.json()
        except:
            raise HTTPNotFound
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

    def data_from_meta(self, metadata_origin):
        urls = None
        r = requests.get(metadata_origin)
        for ct in mime_mapping:
            if ct in r.headers.get('content-type', ''):
                urls = mime_mapping[ct]().get_urls(r.text.encode('utf-8'))
        if not urls:
            return []

        data = []
        for url in urls:
            r = requests.get(url)
            if 'csv' in r.headers.get('content-type', ''):
                data.append(dictify(StringIO(r.content)))
        return data


homer_adapter = HomerAdapter()
