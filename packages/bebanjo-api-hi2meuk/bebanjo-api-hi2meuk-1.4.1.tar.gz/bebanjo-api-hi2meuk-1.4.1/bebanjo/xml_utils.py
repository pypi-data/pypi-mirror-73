import re
from datetime import datetime
import xml.etree.ElementTree as ET  # nosec (trused source)


def bebanjo_xml_from_dict(r: str, data: dict):
    e = ET.Element(r)
    _append_elements(e, data)
    return e


def _append_element(branch, k, v):
    '''Called by _append_elements, deals with individual metadata which could be an array item
    '''
    k = k.replace('_', '-')
    e = ET.Element(k)
    branch.append(e)
    if v is None:
        e.set('nil', 'true')
    elif isinstance(v, bool):  # before int!
        e.set('type', 'boolean')
        e.text = 'true' if v else 'false'
    elif isinstance(v, int):
        e.set('type', 'integer')
        e.text = str(v)
    elif isinstance(v, list):
        e.set('type', 'array')
        inner_name = k[0:-1]
        for _v in v:
            _append_element(e, inner_name, _v)
    elif isinstance(v, datetime):
        e.text = v.isoformat(timespec='seconds')
        e.set('type', 'datetime')
    elif isinstance(v, str):
        e.text = str(v)
    else:
        print(f'got attribute {k} with value {v} of type {type(v)}')
        raise NotImplementedError


def _append_elements(branch, data: dict):
    '''Appends XML branch with the dict representing a Bebanjo object.
    '''
    for k, v in data.items():
        if callable(v):      # support lazy determination of a metadata value via a function
            v = v()
        if isinstance(v, dict):
            continue
        if v is None:
            continue
        _append_element(branch, k, v)


def _append_links(te, links):
    '''Add links to object. Links must be full URLs or begin "api/"
    '''
    for rel, href in links.items():
        if re.search('api/', href) and not href.startswith('/'):
            ET.SubElement(te, 'link', attrib={'rel': rel, 'href': href})
        else:
            raise ValueError


def as_xml(te, data: dict, links=None):
    '''Pass a tree element to have metadata added to it in bebanjo format from given dict
    '''
    if data:
        _append_elements(te, data)
    if links:
        _append_links(te, links)
    return ET.tostring(te)
