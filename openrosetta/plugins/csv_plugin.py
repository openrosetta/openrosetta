import codecs
import csv
from openrosetta.exceptions import InvalidFileFormat


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'cp1252')) for key, value in row.iteritems()])

def dictify(file_=None):
    try:
        dialect = csv.Sniffer().sniff(file_.read(), delimiters=';,')
        file_.seek(0)
        data = UnicodeDictReader(file_, dialect=dialect)
        data = list(data)
    except:
        raise InvalidFileFormat
    return data

