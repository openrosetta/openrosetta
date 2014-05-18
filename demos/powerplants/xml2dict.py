from collections import defaultdict
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def etree_to_dict(t):
    d = {t.tag.split('}')[-1]: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag.split('}')[-1]: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag.split('}')[-1]].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag.split('}')[-1]]['#text'] = text
        else:
            d[t.tag.split('}')[-1]] = text
    return d


def xmlreader(f):
    tree = ET.ElementTree(file=f)
    return etree_to_dict(tree.getroot())
