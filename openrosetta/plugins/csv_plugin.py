import csv
from openrosetta.exceptions import InvalidFileFormat


def dictify(file_=None):
    if file_ is None:
        file_ = open("/home/gas/Desktop/elenco_MMG_PLS_OPENDATA.csv", "r")
    try:
        dialect = csv.Sniffer().sniff(file_.read(), delimiters=';,')
    except:
        raise InvalidFileFormat
    file_.seek(0)
    data = csv.DictReader(file_, dialect)
    return data